import pytest
from fastapi import status
from app.routes import item_service


class TestItemRoutes:
    def test_get_all_items_empty(self, client):
        response = client.get("/api/items/")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_create_item_success(self, client, sample_item_data):
        response = client.post("/api/items/", json=sample_item_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == sample_item_data["name"]
        assert data["description"] == sample_item_data["description"]
        assert data["price"] == sample_item_data["price"]
        assert "id" in data
        assert "created_at" in data

    def test_get_item_by_id_success(self, client, sample_item_data):
        create_response = client.post("/api/items/", json=sample_item_data)
        item_id = create_response.json()["id"]

        response = client.get(f"/api/items/{item_id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == item_id
        assert data["name"] == sample_item_data["name"]

    def test_get_item_by_id_not_found(self, client):
        response = client.get("/api/items/999")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"].lower()

    def test_delete_item_success(self, client, sample_item_data):
        create_response = client.post("/api/items/", json=sample_item_data)
        item_id = create_response.json()["id"]

        response = client.delete(f"/api/items/{item_id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        get_response = client.get(f"/api/items/{item_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_item_not_found(self, client):
        response = client.delete("/api/items/999")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_item_validation_error(self, client):
        invalid_data = {"name": "Test"}

        response = client.post("/api/items/", json=invalid_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.fixture(autouse=True)
    def reset_service(self):
        item_service.items = []
        item_service.next_id = 1
        yield
        item_service.items = []
        item_service.next_id = 1
