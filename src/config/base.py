from typing import Literal, Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Antiquarium Service"
    environment: Literal["local", "dev", "prod"] = "local"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    database_url: str = Field(..., alias="DATABASE_URL")

    # External services
    museum_api_base: str = Field("https://api.antiquarium-museum.ru", alias="MUSEUM_API_BASE")
    catalog_api_base: str = Field("https://catalog.antiquarium-museum.ru", alias="CATALOG_API_BASE")

    # HTTP client
    http_timeout: float = Field(10.0, alias="HTTP_TIMEOUT")

    # Broker
    broker_url: str = Field(..., alias="BROKER_URL")  # e.g. amqp://guest:guest@localhost:5672/
    broker_new_artifact_queue: str = Field("new_artifacts", alias="BROKER_NEW_ARTIFACT_QUEUE")

    # Publish retries
    publish_retries: int = Field(3, alias="PUBLISH_RETRIES")
    publish_retry_backoff: float = Field(0.5, alias="PUBLISH_RETRY_BACKOFF")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"