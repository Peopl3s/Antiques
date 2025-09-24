from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from faststream.kafka import KafkaBroker
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.application.mappers import ArtifactMapper
from src.application.use_cases.get_artifact import GetArtifactUseCase
from src.config.base import Settings
from src.infrastructures.broker.publisher import KafkaPublisher
from src.infrastructures.db.repositories.artifact import ArtifactRepositorySQLAlchemy
from src.infrastructures.db.session import get_session_factory
from src.infrastructures.http.clients import (
    ExternalMuseumAPIClient,
    PublicCatalogAPIClient,
)


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return Settings()


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_engine(self, settings: Settings) -> async_sessionmaker[AsyncSession]:
        engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
        return get_session_factory(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, factory: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AsyncSession]:
        async with factory() as session:
            yield session


class HTTPClientProvider(Provider):
    @provide(scope=Scope.APP)
    def get_http_client(self, settings: Settings) -> AsyncClient:
        return AsyncClient(timeout=settings.HTTP_TIMEOUT)


class BrokerProvider(Provider):
    @provide(scope=Scope.APP)
    def get_broker(self, settings: Settings) -> KafkaBroker:
        return KafkaBroker(settings.KAFKA_URL)


class RepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_artifact_repository(
        self, session: AsyncSession
    ) -> ArtifactRepositorySQLAlchemy:
        return ArtifactRepositorySQLAlchemy(session=session)


class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_external_museum_api_client(
        self,
        client: AsyncClient,
        settings: Settings,
    ) -> ExternalMuseumAPIClient:
        return ExternalMuseumAPIClient(
            base_url=settings.EXTERNAL_API_BASE_URL, client=client
        )

    @provide(scope=Scope.REQUEST)
    def get_public_catalog_api_client(
        self, client: AsyncClient, settings: Settings
    ) -> PublicCatalogAPIClient:
        return PublicCatalogAPIClient(
            base_url=settings.CATALOG_API_BASE_URL, client=client
        )

    @provide(scope=Scope.REQUEST)
    def get_message_broker(self, broker: KafkaBroker) -> KafkaPublisher:
        return KafkaPublisher(broker=broker)


class UseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_register_artifact_use_case(
        self,
        repository: ArtifactRepositorySQLAlchemy,
        museum_api_client: ExternalMuseumAPIClient,
        catalog_api_client: PublicCatalogAPIClient,
        message_broker: KafkaPublisher,
        artifact_mapper: ArtifactMapper,
    ) -> GetArtifactUseCase:
        return GetArtifactUseCase(
            repository=repository,
            museum_api_client=museum_api_client,
            catalog_api_client=catalog_api_client,
            message_broker=message_broker,
            artifact_mapper=artifact_mapper,
        )
