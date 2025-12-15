import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_item_data():
    return {
        "name": "Test Item",
        "description": "Test Description",
        "price": 99.99,
    }
