from __future__ import annotations

import psycopg
from psycopg import Connection

from src.configuration.settings import get_settings


def get_connection() -> Connection:
    settings = get_settings()

    return psycopg.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
        connect_timeout=5,
        application_name="bank_ai_lab",
    )