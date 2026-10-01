from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = ROOT_DIR / ".env"

load_dotenv(ENV_FILE)


@dataclass(frozen=True)
class Settings:
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    required_variables = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    ]

    missing_variables = [
        variable
        for variable in required_variables
        if not os.getenv(variable)
    ]

    if missing_variables:
        raise RuntimeError(
            "В файле .env отсутствуют переменные: "
            + ", ".join(missing_variables)
        )

    try:
        db_port = int(os.environ["DB_PORT"])
    except ValueError as error:
        raise RuntimeError(
            "DB_PORT в файле .env должен быть числом."
        ) from error

    return Settings(
        db_host=os.environ["DB_HOST"],
        db_port=db_port,
        db_name=os.environ["DB_NAME"],
        db_user=os.environ["DB_USER"],
        db_password=os.environ["DB_PASSWORD"],
    )