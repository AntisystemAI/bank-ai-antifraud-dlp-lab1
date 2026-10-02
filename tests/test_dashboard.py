from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_dashboard_route_exists() -> None:
    routes = {
        getattr(route, "path", None)
        for route in app.routes
    }

    assert "/dashboard" in routes


def test_dashboard_returns_html() -> None:
    response = client.get("/dashboard")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Bank AI Antifraud DLP Lab" in response.text
    assert "Eight Security Layers" in response.text
