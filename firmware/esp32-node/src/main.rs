use bme280::i2c::BME280;
use esp_idf_svc::hal::adc::oneshot::config;
use esp_idf_svc::hal::adc::{
    oneshot::{AdcChannelDriver, AdcDriver},
    ADC1,
};
use esp_idf_svc::hal::{
    delay,
    i2c::{I2cConfig, I2cDriver},
    peripherals::Peripherals,
    units::FromValueType,
};

fn main() {
    esp_idf_svc::sys::link_patches();
    esp_idf_svc::log::EspLogger::initialize_default();

    let peripherals = Peripherals::take().unwrap();
    let sda = peripherals.pins.gpio21;
    let scl = peripherals.pins.gpio22;
    let config = I2cConfig::new().baudrate(100_u32.kHz().into());
    let i2c = I2cDriver::new(peripherals.i2c0, sda, scl, &config).unwrap();

    let mut bme280 = BME280::new_primary(i2c);
    let mut delay = delay::Ets;
    bme280.init(&mut delay).unwrap();

    let adc = AdcDriver::new(peripherals.adc1).unwrap();
    let mut adc_pin = AdcChannelDriver::new(
        &adc,
        peripherals.pins.gpio34,
        &config::AdcChannelConfig::default(),
    )
    .unwrap();

    loop {
        let measurements = bme280.measure(&mut delay).unwrap();
        log::info!("Temperature = {} °C", measurements.temperature);
        log::info!("Humidity = {} %", measurements.humidity);
        log::info!("Pressure = {} Pa", measurements.pressure);
        let raw_value = adc.read(&mut adc_pin).unwrap();
        log::info!("Soil moisture raw = {}", raw_value);
        delay::FreeRtos::delay_ms(5000);
    }
}
