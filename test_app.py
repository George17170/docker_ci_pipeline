import pytest
from app.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestIndexEndpoint:
    def test_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_returns_json(self, client):
        response = client.get("/")
        assert response.content_type == "application/json"

    def test_status_is_ok(self, client):
        data = client.get("/").get_json()
        assert data["status"] == "ok"

    def test_service_name_present(self, client):
        data = client.get("/").get_json()
        assert data["service"] == "docker-ci-pipeline"

    def test_version_present(self, client):
        data = client.get("/").get_json()
        assert "version" in data

    def test_environment_present(self, client):
        data = client.get("/").get_json()
        assert "environment" in data


class TestHealthEndpoint:
    def test_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_status_is_healthy(self, client):
        data = client.get("/health").get_json()
        assert data["status"] == "healthy"

    def test_uptime_is_non_negative(self, client):
        data = client.get("/health").get_json()
        assert data["uptime_seconds"] >= 0

    def test_timestamp_present(self, client):
        data = client.get("/health").get_json()
        assert "timestamp" in data

    def test_python_version_present(self, client):
        data = client.get("/health").get_json()
        assert "python" in data

    def test_host_present(self, client):
        data = client.get("/health").get_json()
        assert "host" in data


class TestPipelineEndpoint:
    def test_returns_200(self, client):
        response = client.get("/pipeline")
        assert response.status_code == 200

    def test_build_info_present(self, client):
        data = client.get("/pipeline").get_json()
        assert "build" in data

    def test_image_info_present(self, client):
        data = client.get("/pipeline").get_json()
        assert "image" in data

    def test_build_has_required_fields(self, client):
        data = client.get("/pipeline").get_json()
        build = data["build"]
        assert "commit_sha" in build
        assert "build_number" in build
        assert "branch" in build

    def test_image_has_required_fields(self, client):
        data = client.get("/pipeline").get_json()
        image = data["image"]
        assert "name" in image
        assert "version" in image


class TestNotFound:
    def test_unknown_route_returns_404(self, client):
        response = client.get("/nonexistent")
        assert response.status_code == 404
