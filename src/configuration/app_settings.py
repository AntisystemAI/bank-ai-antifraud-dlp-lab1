from __future__ import annotations

from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Bank AI Antifraud DLP Lab"
    app_version: str = "0.3.0"

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "bank_ai_lab"
    db_user: str = "bank_ai_user"
    db_password: str = "change_me"

    database_url: str | None = None

    security_policy_path: str = "config/security_policy.yml"
    persist_decisions: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def postgres_dsn(self) -> str:
        if self.database_url:
            return self.database_url

        encoded_user = quote_plus(self.db_user)
        encoded_password = quote_plus(self.db_password)

        return (
            f"postgresql://{encoded_user}:{encoded_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()