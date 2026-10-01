from pathlib import Path
from typing import Any

import yaml
from fastapi import FastAPI


ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = ROOT / "config" / "security_policy.yml"


def load_security_policy() -> dict[str, Any]:
    if not POLICY_PATH.exists():
        raise RuntimeError(
            f"Файл политики не найден: {POLICY_PATH}"
        )

    with POLICY_PATH.open("r", encoding="utf-8") as file:
        policy = yaml.safe_load(file)

    if not isinstance(policy, dict):
        raise RuntimeError(
            "Политика безопасности должна быть YAML-объектом."
        )

    if "policy_version" not in policy:
        raise RuntimeError(
            "В политике отсутствует policy_version."
        )

    return policy


policy = load_security_policy()

app = FastAPI(
    title="Bank AI Antifraud DLP Lab",
    version="0.1.0",
    description=(
        "Учебный API для проверки синтетических "
        "банковских событий."
    ),
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Bank AI Antifraud DLP Lab API",
        "documentation": "/docs",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "application": "Bank AI Antifraud DLP Lab",
        "version": "0.1.0",
        "policy_version": str(policy["policy_version"]),
    }