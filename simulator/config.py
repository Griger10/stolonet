from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SIMULATOR_MQTT_", case_sensitive=False)
    host: str
    port: int
    topic: str


def load_config() -> Config:
    return Config()
