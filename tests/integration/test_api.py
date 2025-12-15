import pytest
from fastapi import status
from app.routes import item_service


class TestAPIIntegration:
    def test_full_item_lifecycle(self, client):
        item_data = {
            "name": "Integration Test Item",
            "description": "Testing full lifecycle",
            "price": 50.0
        }

        create_response = client.post("/api/items/", json=item_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        created_item = create_response.json()
        item_id = created_item["id"]

        get_response = client.get(f"/api/items/{item_id}")
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json()["name"] == item_data["name"]

        all_items_response = client.get("/api/items/")
        assert all_items_response.status_code == status.HTTP_200_OK
        assert len(all_items_response.json()) >= 1

        delete_response = client.delete(f"/api/items/{item_id}")
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        get_after_delete = client.get(f"/api/items/{item_id}")
        assert get_after_delete.status_code == status.HTTP_404_NOT_FOUND

    def test_multiple_items_creation(self, client):
        items_data = [
            {"name": f"Item {i}", "price": float(i * 10)}
            for i in range(1, 6)
        ]

        created_ids = []
        for item_data in items_data:
            response = client.post("/api/items/", json=item_data)
            assert response.status_code == status.HTTP_201_CREATED
            created_ids.append(response.json()["id"])

        all_items = client.get("/api/items/").json()
        assert len(all_items) == 5

        for item_id in created_ids:
            response = client.get(f"/api/items/{item_id}")
            assert response.status_code == status.HTTP_200_OK

    def test_health_endpoints(self, client):
        root_response = client.get("/")
        assert root_response.status_code == status.HTTP_200_OK
        assert root_response.json()["status"] == "healthy"

        health_response = client.get("/health")
        assert health_response.status_code == status.HTTP_200_OK
        assert health_response.json()["status"] == "ok"

    @pytest.fixture(autouse=True)
    def reset_service(self):
        item_service.items = []
        item_service.next_id = 1
        yield
        item_service.items = []
        item_service.next_id = 1
