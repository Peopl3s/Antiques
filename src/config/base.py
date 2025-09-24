from typing import Literal, cast, final

from pydantic import Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings


@final
class Settings(BaseSettings):
    app_name: str = "Antiquarium Service"
    environment: Literal["local", "dev", "prod"] = "local"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    postgres_user: str = Field(..., alias="POSTGRES_USER")
    postgres_password: str = Field(..., alias="POSTGRES_PASSWORD")
    postgres_server: str = Field(..., alias="POSTGRES_SERVER")
    postgres_port: int = Field(5432, alias="POSTGRES_PORT")
    postgres_db: str = Field(..., alias="POSTGRES_DB")

    museum_api_base: str = Field(
        "https://api.antiquarium-museum.ru", alias="MUSEUM_API_BASE"
    )
    catalog_api_base: str = Field(
        "https://catalog.antiquarium-museum.ru", alias="CATALOG_API_BASE"
    )

    http_timeout: float = Field(10.0, alias="HTTP_TIMEOUT")

    broker_url: str = Field(
        ..., alias="BROKER_URL"
    )  # e.g. amqp://guest:guest@localhost:5672/
    broker_new_artifact_queue: str = Field(
        "new_artifacts", alias="BROKER_NEW_ARTIFACT_QUEUE"
    )

    publish_retries: int = Field(3, alias="PUBLISH_RETRIES")
    publish_retry_backoff: float = Field(0.5, alias="PUBLISH_RETRY_BACKOFF")

    @computed_field
    def database_url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_server,
            port=self.postgres_port,
            path=self.postgres_db,
        )

    @computed_field
    def sqlalchemy_database_uri(self) -> PostgresDsn:
        return cast("PostgresDsn", self.database_url)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
