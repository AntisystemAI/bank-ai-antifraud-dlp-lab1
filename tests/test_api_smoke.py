from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_health_response() -> None:
    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "ok"
    assert body["version"] == "0.3.0"
    assert body["policy_version"] == "1.0.0"
    assert body["agents_loaded"] == 5
    assert body["scenarios_loaded"] == 11
    assert body["synthetic_environment"] is True


def test_agents_endpoint() -> None:
    response = client.get("/v1/agents")

    assert response.status_code == 200

    agents = response.json()

    assert len(agents) == 5
    assert all(
        "allowed_tools" in agent
        for agent in agents
    )


def test_scenarios_endpoint() -> None:
    response = client.get("/v1/scenarios")

    assert response.status_code == 200

    scenarios = response.json()

    assert len(scenarios) == 11
    assert all(
        "scenario_id" in scenario
        for scenario in scenarios
    )
    assert all(
        "expected_decision" in scenario
        for scenario in scenarios
    )


def test_safe_scenario() -> None:
    response = client.post(
        "/v1/scenarios/aggregated_report/run"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["passed"] is True
    assert body["actual_decision"] == "ALLOW"
    assert len(body["decision"]["layers"]) == 8


def test_combined_incident() -> None:
    response = client.post(
        "/v1/scenarios/combined_incident/run"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["passed"] is True
    assert body["actual_decision"] == "BLOCK"
    assert body["decision"]["incident_created"] is True
    assert body["decision"]["incident_id"] is not None
    assert len(body["decision"]["layers"]) == 8


def test_unknown_scenario_returns_404() -> None:
    response = client.post(
        "/v1/scenarios/unknown_scenario/run"
    )

    assert response.status_code == 404


def test_dashboard_endpoint() -> None:
    response = client.get("/dashboard")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith(
        "text/html"
    )
    assert "Bank AI Security Dashboard" in response.text
    assert "/v1/demo/run-all" in response.text
    assert "/v1/metrics" in response.text


def test_openapi_contract() -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200

    schema = response.json()
    paths = set(schema["paths"])

    required_paths = {
        "/health",
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
        "В OpenAPI отсутствуют маршруты: "
        f"{sorted(missing_paths)}"
    )

    assert (
        schema["info"]["title"]
        == "Bank AI Antifraud DLP Lab"
    )
    assert schema["info"]["version"] == "0.3.0"


def test_health_does_not_expose_secrets() -> None:
    response = client.get("/health")

    assert response.status_code == 200

    serialized = response.text.lower()

    forbidden_fragments = {
        "db_password",
        "database_url",
        "postgresql://",
        "password",
    }

    for fragment in forbidden_fragments:
        assert fragment not in serialized
