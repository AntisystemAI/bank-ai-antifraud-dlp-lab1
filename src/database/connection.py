from __future__ import annotations

import psycopg
from psycopg import Connection

from src.configuration.app_settings import settings


def get_connection() -> Connection:
    return psycopg.connect(
        settings.postgres_dsn,
        connect_timeout=5,
        application_name="bank_ai_antifraud_dlp_lab",
    )