from pydantic_settings import BaseSettings, SettingsConfigDict


class MQTTConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MQTT_", case_sensitive=False)
    host: str
    port: int
    topic: str


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_", case_sensitive=False)
    host: str
    port: int
    user: str
    password: str
    database: str


class Config(BaseSettings):
    mqtt_config: MQTTConfig = MQTTConfig()


def load_config() -> Config:
    return Config()
