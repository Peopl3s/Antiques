from fastapi.testclient import TestClient
import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from src.main import create_app


@pytest.fixture
async def test_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync()
    yield engine
    await engine.dispose()


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)
