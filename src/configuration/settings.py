from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Bank AI Antifraud DLP Lab"
    app_version: str = "0.1.0"

    database_url: str
    security_policy_path: str = "config/security_policy.yml"
    persist_decisions: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()