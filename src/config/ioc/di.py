from dishka import Provider

from src.config.ioc.providers import (
    SettingsProvider,
    DatabaseProvider,
    HTTPClientProvider,
    BrokerProvider,
    RepositoryProvider,
    ServiceProvider,
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