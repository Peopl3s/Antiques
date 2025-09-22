import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from src.config.ioc.di import get_providers
from src.presentation.api.rest.v1.routers import api_v1_router
from src.config.logging import setup_logging


setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Приложение запускается")
    yield
    logging.info("Приложение останавливается")


app = FastAPI(title="Антиквариум API", version="1.0.0", lifespan=lifespan)

# DI
container = make_async_container(*get_providers())
setup_dishka(container, app)

# Routes
app.include_router(api_v1_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn # replace granian
    uvicorn.run(app, host="0.0.0.0", port=8000)