"""
Shared pytest fixtures available to every test file automatically.

Contains:
- init_test_db  → Initializes in-memory MongoDB mock before each test
- client        → Async HTTP test client wired to the FastAPI app
"""

import pytest
from httpx import AsyncClient, ASGITransport
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient
from src.main import app as main_app
from src.models.users import User


@pytest.fixture(autouse=True)
async def init_test_db():
    """
    Spins up a fresh in-memory MongoDB mock before every test.
    """
    mock_client = AsyncMongoMockClient()
    await init_beanie(
        database=mock_client.test_db,
        document_models=[User]
    )
    yield


@pytest.fixture
async def client():
    """
    Async HTTP client wired directly to the FastAPI app.
    Defined here so every test file can use it without re-declaring it.
    """
    async with AsyncClient(
        transport=ASGITransport(app=main_app),
        base_url="http://test"
    ) as ac:
        yield ac