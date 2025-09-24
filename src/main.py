from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import logging

from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.config.ioc.di import get_providers
from src.config.logging import setup_logging
from src.presentation.api.rest.v1.routers import api_v1_router

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    logger.info("Starting application...")
    yield
    logger.info("Shutting down application...")


def create_app() -> FastAPI:
    """Фабрика приложения для лучшей тестируемости и гибкости."""
    app = FastAPI(
        title="Антиквариум API",
        version="1.0.0",
        description="API для управления артефактами в музее",
        lifespan=lifespan,
        docs_url="/api/docs",  # Swagger UI
        redoc_url="/api/redoc",  # ReDoc
        openapi_url="/api/openapi.json",
    )

    container: AsyncContainer = make_async_container(*get_providers())
    setup_dishka(container, app)

    app.include_router(api_v1_router, prefix="/api")

    return app


app = create_app()


if __name__ == "__main__":
    from granian import Granian
    from granian.log import LogLevels

    server = Granian(
        target="main:app",
        host="0.0.0.0",  # noqa: S104
        port=8000,
        reload=True,
        log_level=LogLevels.info,
        workers=1,
    )
    server.serve()
