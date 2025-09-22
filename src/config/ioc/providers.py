from dishka import Provider, provide, Scope
from faststream.kafka import KafkaBroker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from httpx import AsyncClient

from src.infrastructures.broker.publisher import KafkaPublisher
from src.infrastructures.db.repositories.artifact import ArtifactRepositorySQLAlchemy
from src.infrastructures.db.session import get_session_factory

from src.application.use_cases.register_artifact import RegisterArtifactUseCase
from src.config.base import Settings
from src.infrastructures.http.clients import ExternalMuseumAPIClient, PublicCatalogAPIClient


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
    async def get_session(self, factory: async_sessionmaker[AsyncSession]) -> AsyncSession:
        async with factory() as session:
            yield session # type: ignore


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
    def get_artifact_repository(self, session: AsyncSession) -> ArtifactRepositorySQLAlchemy:
        return ArtifactRepositorySQLAlchemy(session)


class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_external_museum_api_client(
        self, client: AsyncClient, settings: Settings
    ) -> ExternalMuseumAPIClient:
        return ExternalMuseumAPIClient(settings.EXTERNAL_API_BASE_URL, client)

    @provide(scope=Scope.REQUEST)
    def get_public_catalog_api_client(self, client: AsyncClient, settings: Settings) -> PublicCatalogAPIClient:
        return PublicCatalogAPIClient(settings.CATALOG_API_BASE_URL, client)

    @provide(scope=Scope.REQUEST)
    def get_message_broker(self, broker: KafkaBroker) -> KafkaPublisher:
        return KafkaPublisher(broker)


class UseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_register_artifact_use_case(
        self,
        repository: ArtifactRepositorySQLAlchemy,
        museum_api_client: ExternalMuseumAPIClient,
        catalog_api_client: PublicCatalogAPIClient,
        message_broker: KafkaPublisher,
    ) -> RegisterArtifactUseCase:
        return RegisterArtifactUseCase(
            repository=repository,
            museum_api_client=museum_api_client,
            catalog_api_client=catalog_api_client,
            message_broker=message_broker,
        )