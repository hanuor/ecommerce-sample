import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.redis import redis_client

client = TestClient(app)


@pytest.fixture(scope="session")
def test_client():
    return client


@pytest.fixture(autouse=True)
def clean_redis():
    """
    Clear Redis before and after every test to ensure
    test isolation.
    """
    redis_client.flushdb()

    yield

    redis_client.flushdb()