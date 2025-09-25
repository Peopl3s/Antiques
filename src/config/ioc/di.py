from dishka import Provider

from src.config.ioc.providers import (
    BrokerProvider,
    DatabaseProvider,
    HTTPClientProvider,
    MapperProvider,
    RepositoryProvider,
    ServiceProvider,
    SettingsProvider,
    UseCaseProvider,
)


def get_providers() -> list[Provider]:
    return [
        SettingsProvider(),
        DatabaseProvider(),
        HTTPClientProvider(),
        BrokerProvider(),
        RepositoryProvider(),
        ServiceProvider(),
        MapperProvider(),
        UseCaseProvider(),
    ]
