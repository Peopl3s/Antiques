from src.config.ioc.providers import (
    SettingsProvider,
    DatabaseProvider,
    HTTPClientProvider,
    BrokerProvider,
    RepositoryProvider,
    ServiceProvider,
    UseCaseProvider,
)


def get_providers():
    return [
        SettingsProvider(),
        DatabaseProvider(),
        HTTPClientProvider(),
        BrokerProvider(),
        RepositoryProvider(),
        ServiceProvider(),
        UseCaseProvider(),
    ]