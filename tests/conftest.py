import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "sqlite:///./app.db")
os.environ.setdefault("API_KEY", "change-me")

from app.main import app  # noqa: E402
from app.core.config import settings  # noqa: E402


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(scope="session")
def api_key():
    # Pull from the actual app settings so tests match whatever you configured (.env etc.)
    return settings.api_key


@pytest.fixture(scope="session")
def auth_headers(api_key):
    return {"X-API-Key": api_key}