from fastapi import FastAPI

from src.api.main import app, health


def test_fastapi_application_exists() -> None:
    assert isinstance(app, FastAPI)
    assert app.title == "Bank AI Antifraud DLP Lab"


def test_health_response() -> None:
    response = health()

    assert response["status"] == "ok"
    assert response["application"] == (
        "Bank AI Antifraud DLP Lab"
    )
    assert response["version"] == "0.1.0"
    assert response["policy_version"] == "1.0.0"