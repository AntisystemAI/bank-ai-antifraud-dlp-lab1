from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_dashboard_is_available() -> None:
    response = client.get("/dashboard")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith(
        "text/html"
    )
    assert "Bank AI Security Dashboard" in response.text


def test_required_openapi_paths_exist() -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200

    schema = response.json()
    paths = set(schema["paths"])

    required_paths = {
        "/",
        "/health",
        "/dashboard",
        "/v1/agents",
        "/v1/security/evaluate",
        "/v1/scenarios",
        "/v1/scenarios/{scenario_id}/run",
        "/v1/demo/run-all",
        "/v1/audit",
        "/v1/incidents",
        "/v1/metrics",
    }

    missing_paths = required_paths - paths

    assert not missing_paths, (
        f"Missing OpenAPI paths: {sorted(missing_paths)}"
    )


def test_health_response_does_not_expose_secrets() -> None:
    response = client.get("/health")

    assert response.status_code == 200

    body = response.text.lower()

    assert "password" not in body
    assert "database_url" not in body
    assert "postgresql://" not in body
    assert "db_password" not in body


def test_agents_catalog_is_available() -> None:
    response = client.get("/v1/agents")

    assert response.status_code == 200

    payload = response.json()

    assert isinstance(payload, list)
    assert len(payload) >= 5


def test_scenarios_catalog_is_available() -> None:
    response = client.get("/v1/scenarios")

    assert response.status_code == 200

    payload = response.json()

    assert isinstance(payload, list)
    assert len(payload) == 11