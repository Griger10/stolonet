from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent.parent
ROOT_DIR = BACKEND_DIR.parent


ENV_FILES = (
    BACKEND_DIR / ".env",
    ROOT_DIR / ".env",
)


class MQTTConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MQTT_",
        case_sensitive=False,
        env_file=ENV_FILES,
        extra="ignore",
    )
    host: str
    port: int


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_",
        case_sensitive=False,
        env_file=ENV_FILES,
        extra="ignore",
    )
    host: str
    port: int
    user: str
    password: SecretStr
    db: str

    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"


class APIConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="API_",
        case_sensitive=False,
        env_file=ENV_FILES,
        extra="ignore",
    )
    host: str
    port: int
    debug: bool = True


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILES,
        extra="ignore",
    )
    mqtt_config: MQTTConfig = MQTTConfig()
    database_config: DatabaseConfig = DatabaseConfig()
    api_config: APIConfig = APIConfig()


def load_config() -> Config:
    return Config()
