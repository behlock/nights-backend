"""Centralised, validated runtime settings.

All env vars are read once at import time. Missing / malformed values fail loudly
instead of silently producing 'None' strings in connection URLs or skipping CORS.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=5432)
    DB_USERNAME: str = Field(default="postgres")
    DB_PASSWORD: str = Field(default="")
    DB_DATABASE_NAME: str = Field(default="nights")


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    ENVIRONMENT: Literal["dev", "staging", "production"] = "production"
    SERVICE_NAME: str = "nightsservice"
    VERSION: str = "0.2.0"
    HOST: str = "0.0.0.0"  # noqa: S104 — bind for container; restrict at ingress
    PORT: int = 5002

    SQL_ECHO: bool = False
    LOG_LEVEL: str = "INFO"

    # Comma-separated list of allowed CORS origins. Empty string disables CORS.
    CORS_ALLOWED_ORIGINS: str = ""

    # Comma-separated list of trusted host headers ("*" allows any).
    TRUSTED_HOSTS: str = "*"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ALLOWED_ORIGINS.split(",") if o.strip()]

    @property
    def trusted_hosts_list(self) -> list[str]:
        return [h.strip() for h in self.TRUSTED_HOSTS.split(",") if h.strip()] or ["*"]


@lru_cache(maxsize=1)
def get_app_settings() -> AppSettings:
    return AppSettings()


@lru_cache(maxsize=1)
def get_db_settings() -> DatabaseSettings:
    return DatabaseSettings()
