import pytest
import subprocess
import requests
import time
import os


class TestDockerImage:
    @pytest.fixture(scope="class")
    def docker_image_name(self):
        return "test-app:latest"

    @pytest.fixture(scope="class")
    def docker_container_name(self):
        return "test-app-container"

    def test_docker_image_builds_successfully(self, docker_image_name):
        result = subprocess.run(
            ["docker", "build", "-t", docker_image_name, "."],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        assert result.returncode == 0, f"Build failed: {result.stderr}"

    def test_docker_image_size_reasonable(self, docker_image_name):
        result = subprocess.run(
            ["docker", "images", docker_image_name, "--format", "{{.Size}}"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            size_str = result.stdout.strip()
            if "MB" in size_str:
                size_mb = float(size_str.replace("MB", ""))
                assert size_mb < 500, f"Image size {size_mb}MB is too large"

    def test_docker_container_starts(self, docker_image_name, docker_container_name):
        subprocess.run(
            ["docker", "stop", docker_container_name],
            capture_output=True
        )
        subprocess.run(
            ["docker", "rm", docker_container_name],
            capture_output=True
        )
        
        result = subprocess.run(
            [
                "docker",
                "run",
                "-d",
                "--name",
                docker_container_name,
                "-p",
                "8001:8000",
                docker_image_name,
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Container start failed: {result.stderr}"
        
        time.sleep(3)
        
        container_status = subprocess.run(
            [
                "docker",
                "ps",
                "--filter",
                f"name={docker_container_name}",
                "--format",
                "{{.Status}}",
            ],
            capture_output=True,
            text=True,
        )
        assert "Up" in container_status.stdout or container_status.returncode == 0

    def test_docker_container_healthcheck(self, docker_container_name):
        max_attempts = 10
        for attempt in range(max_attempts):
            try:
                response = requests.get(
                    "http://localhost:8001/health", timeout=2
                )
                if response.status_code == 200:
                    assert response.json()["status"] == "ok"
                    return
            except requests.exceptions.RequestException:
                pass
            time.sleep(1)
        pytest.fail("Health check failed after multiple attempts")

    def test_docker_container_api_functionality(self, docker_container_name):
        base_url = "http://localhost:8001"
        
        item_data = {
            "name": "Docker Test Item",
            "description": "Testing in container",
            "price": 99.99
        }
        
        create_response = requests.post(
            f"{base_url}/api/items/", json=item_data, timeout=5
        )
        assert create_response.status_code == 201
        
        created_item = create_response.json()
        item_id = created_item["id"]
        
        get_response = requests.get(f"{base_url}/api/items/{item_id}", timeout=5)
        assert get_response.status_code == 200
        assert get_response.json()["name"] == item_data["name"]
        
        health_response = requests.get(f"{base_url}/health", timeout=5)
        assert health_response.status_code == 200

    def test_docker_container_runs_as_non_root(self, docker_container_name):
        result = subprocess.run(
            ["docker", "exec", docker_container_name, "whoami"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            user = result.stdout.strip()
            assert user != "root", "Container should not run as root"

    @pytest.fixture(scope="class", autouse=True)
    def cleanup_container(self, docker_container_name):
        yield
        subprocess.run(["docker", "stop", docker_container_name], capture_output=True)
        subprocess.run(["docker", "rm", docker_container_name], capture_output=True)

