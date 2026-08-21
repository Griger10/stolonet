use bme280::i2c::BME280;
use chrono::Utc;
use esp_idf_svc::eventloop::EspSystemEventLoop;
use esp_idf_svc::hal::adc::oneshot::config;
use esp_idf_svc::hal::adc::oneshot::{AdcChannelDriver, AdcDriver};
use esp_idf_svc::hal::{
    delay,
    i2c::{I2cConfig, I2cDriver},
    peripherals::Peripherals,
    units::FromValueType,
};
use esp_idf_svc::mqtt::client::{EspMqttClient, MqttClientConfiguration, QoS};
use esp_idf_svc::nvs::EspDefaultNvsPartition;
use esp_idf_svc::sntp::{EspSntp, SyncStatus};
use esp_idf_svc::wifi::{AuthMethod, BlockingWifi, ClientConfiguration, Configuration, EspWifi};

#[toml_cfg::toml_config]
pub struct Config {
    #[default("")]
    wifi_ssid: &'static str,
    #[default("")]
    wifi_password: &'static str,
    #[default("")]
    mqtt_broker_url: &'static str,
}

const SOIL_DRY_RAW: u16 = 950;
const SOIL_WET_RAW: u16 = 400;

fn calibrate_soil_moisture(raw: u16, dry_value: u16, wet_value: u16) -> f32 {
    let clamped = raw.clamp(wet_value, dry_value);
    let percent = (dry_value - clamped) as f32 / (dry_value - wet_value) as f32 * 100.0;
    percent.clamp(0.0, 100.0)
}

fn main() {
    esp_idf_svc::sys::link_patches();
    esp_idf_svc::log::EspLogger::initialize_default();

    let peripherals = Peripherals::take().unwrap();

    let i2c_config = I2cConfig::new().baudrate(100_u32.kHz().into());
    let i2c = I2cDriver::new(
        peripherals.i2c0,
        peripherals.pins.gpio21,
        peripherals.pins.gpio22,
        &i2c_config,
    )
    .unwrap();
    let mut bme280 = BME280::new_primary(i2c);
    let mut delay = delay::Ets;
    bme280.init(&mut delay).unwrap();

    let adc = AdcDriver::new(peripherals.adc1).unwrap();
    let mut adc_pin = AdcChannelDriver::new(
        &adc,
        peripherals.pins.gpio35,
        &config::AdcChannelConfig::default(),
    )
    .unwrap();

    let sys_loop = EspSystemEventLoop::take().unwrap();
    let nvs = EspDefaultNvsPartition::take().unwrap();
    let mut wifi = BlockingWifi::wrap(
        EspWifi::new(peripherals.modem, sys_loop.clone(), Some(nvs)).unwrap(),
        sys_loop,
    )
    .unwrap();

    wifi.set_configuration(&Configuration::Client(ClientConfiguration {
        ssid: CONFIG.wifi_ssid.try_into().unwrap(),
        password: CONFIG.wifi_password.try_into().unwrap(),
        auth_method: AuthMethod::WPA2Personal,
        ..Default::default()
    }))
    .unwrap();

    wifi.start().unwrap();
    wifi.connect().unwrap();
    wifi.wait_netif_up().unwrap();
    log::info!(
        "WiFi connected, IP: {:?}",
        wifi.wifi().sta_netif().get_ip_info().unwrap()
    );

    let sntp = EspSntp::new_default().unwrap();
    while sntp.get_sync_status() != SyncStatus::Completed {
        delay::FreeRtos::delay_ms(100);
    }
    log::info!("Time synchronized");

    let mqtt_config = MqttClientConfiguration::default();
    let (mut client, mut connection) =
        EspMqttClient::new(CONFIG.mqtt_broker_url, &mqtt_config).unwrap();

    std::thread::spawn(move || {
        while let Ok(event) = connection.next() {
            log::info!("MQTT event: {:?}", event.payload());
        }
    });

    loop {
        let measurements = bme280.measure(&mut delay).unwrap();
        let soil_raw = adc.read(&mut adc_pin).unwrap();
        let soil_percent = calibrate_soil_moisture(soil_raw, SOIL_DRY_RAW, SOIL_WET_RAW);
        let timestamp = Utc::now().to_rfc3339();
        log::info!("Soil moisture raw = {}", soil_raw);

        let payload = format!(
            r#"{{"node_id":"esp32-node-1","timestamp":"{}","readings":[{{"metric":"air_temperature","value":{:.2},"unit":"C"}},{{"metric":"soil_moisture","value":{:.1},"unit":"%"}}]}}"#,
            timestamp, measurements.temperature, soil_percent,
        );

        if let Err(e) = client.publish(
            "stolonet/telemetry/esp32-node-1",
            QoS::AtLeastOnce,
            false,
            payload.as_bytes(),
        ) {
            log::error!("MQTT publish failed: {:?}", e);
        }

        delay::FreeRtos::delay_ms(5000);
    }
}
