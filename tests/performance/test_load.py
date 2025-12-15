import pytest
import time
from fastapi import status


class TestPerformance:
    def test_single_request_response_time(self, client, benchmark):
        item_data = {"name": "Performance Test", "price": 10.0}
        
        def create_item():
            return client.post("/api/items/", json=item_data)
        
        result = benchmark(create_item)
        assert result.status_code == status.HTTP_201_CREATED

    def test_multiple_sequential_requests(self, client):
        item_data = {"name": "Load Test", "price": 10.0}
        start_time = time.time()
        
        for _ in range(10):
            response = client.post("/api/items/", json=item_data)
            assert response.status_code == status.HTTP_201_CREATED
        
        elapsed_time = time.time() - start_time
        assert elapsed_time < 5.0

    def test_get_all_items_performance(self, client, benchmark):
        for i in range(20):
            client.post(
                "/api/items/", json={"name": f"Item {i}", "price": float(i)}
            )
        
        def get_all():
            return client.get("/api/items/")
        
        result = benchmark(get_all)
        assert result.status_code == status.HTTP_200_OK
        assert len(result.json()) >= 20

    def test_health_endpoint_performance(self, client, benchmark):
        def check_health():
            return client.get("/health")
        
        result = benchmark(check_health)
        assert result.status_code == status.HTTP_200_OK

    def test_concurrent_operations(self, client):
        import concurrent.futures
        
        def create_item(index):
            return client.post(
                "/api/items/",
                json={"name": f"Concurrent {index}", "price": float(index)},
            )

        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(create_item, i) for i in range(10)]
            results = [
                future.result()
                for future in concurrent.futures.as_completed(futures)
            ]
        
        elapsed_time = time.time() - start_time
        assert elapsed_time < 3.0
        assert all(r.status_code == status.HTTP_201_CREATED for r in results)

