"""Application settings, read from environment variables (12-factor config)."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings loaded from the environment, falling back to a local-dev default.

    pydantic-settings reads each field from an env var of the same name
    (case-insensitive), or from a .env file if present.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql://validationops:validationops@localhost:5432/validationops"
    redis_url: str = "redis://localhost:6379/0"


settings = Settings()
