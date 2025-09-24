from dishka import Provider

from src.config.ioc.providers import (
    BrokerProvider,
    DatabaseProvider,
    HTTPClientProvider,
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
        UseCaseProvider(),
    ]
