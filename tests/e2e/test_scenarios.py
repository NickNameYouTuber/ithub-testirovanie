from fastapi import status


class TestEndToEndScenarios:
    def test_user_creates_and_manages_items(self, client):
        initial_items = client.get("/api/items/").json()
        initial_count = len(initial_items)

        new_item = {
            "name": "E2E Test Item",
            "description": "End-to-end test scenario",
            "price": 75.99,
        }

        create_response = client.post("/api/items/", json=new_item)
        assert create_response.status_code == status.HTTP_201_CREATED
        created_item = create_response.json()

        all_items_after_create = client.get("/api/items/").json()
        assert len(all_items_after_create) == initial_count + 1

        retrieved_item = client.get(f"/api/items/{created_item['id']}").json()
        assert retrieved_item["name"] == new_item["name"]
        assert retrieved_item["price"] == new_item["price"]

        client.delete(f"/api/items/{created_item['id']}")

        final_items = client.get("/api/items/").json()
        assert len(final_items) == initial_count

    def test_user_browses_catalog(self, client):
        items_to_create = [
            {"name": "Product A", "price": 10.0},
            {"name": "Product B", "price": 20.0},
            {"name": "Product C", "price": 30.0},
        ]

        for item_data in items_to_create:
            client.post("/api/items/", json=item_data)

        catalog = client.get("/api/items/").json()
        assert len(catalog) >= 3

        product_names = [item["name"] for item in catalog]
        assert "Product A" in product_names
        assert "Product B" in product_names
        assert "Product C" in product_names

    def test_user_searches_specific_item(self, client):
        item_data = {
            "name": "Unique Search Item",
            "description": "This should be findable",
            "price": 42.0,
        }

        created = client.post("/api/items/", json=item_data).json()

        found_item = client.get(f"/api/items/{created['id']}").json()
        assert found_item["name"] == "Unique Search Item"
        assert found_item["description"] == "This should be findable"

    def test_user_handles_error_scenarios(self, client):
        non_existent_response = client.get("/api/items/99999")
        assert non_existent_response.status_code == status.HTTP_404_NOT_FOUND

        invalid_delete = client.delete("/api/items/99999")
        assert invalid_delete.status_code == status.HTTP_404_NOT_FOUND

        invalid_create = client.post(
            "/api/items/", json={"invalid": "data"}
        )
        assert invalid_create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_application_health_monitoring(self, client):
        health_check = client.get("/health")
        assert health_check.status_code == status.HTTP_200_OK

        root_check = client.get("/")
        assert root_check.status_code == status.HTTP_200_OK
        assert "status" in root_check.json()
