from pydantic_settings import BaseSettings, SettingsConfigDict


class MQTTConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MQTT_", case_sensitive=False)
    host: str
    port: int


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_", case_sensitive=False)
    host: str
    port: int
    user: str
    password: str
    database: str


class APIConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="API_", case_sensitive=False)
    host: str
    port: int
    debug: bool = True


class Config(BaseSettings):
    mqtt_config: MQTTConfig = MQTTConfig()
    database_config: DatabaseConfig = DatabaseConfig()
    api_config: APIConfig = APIConfig()


def load_config() -> Config:
    return Config()
