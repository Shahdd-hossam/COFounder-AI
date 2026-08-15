from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CoFounder AI API"
    app_version: str = "0.2.0"
    api_prefix: str = "/api/v1"
    debug: bool = False
    allowed_origins: list[str] = ["http://localhost:3000"]
    database_url: str = Field(default="sqlite:///./cofounder_ai.db", validation_alias="DATABASE_URL")
    db_pool_size: int = Field(default=5, validation_alias="DB_POOL_SIZE")
    db_max_overflow: int = Field(default=5, validation_alias="DB_MAX_OVERFLOW")
    db_pool_recycle: int = Field(default=1800, validation_alias="DB_POOL_RECYCLE")
    db_echo: bool = Field(default=False, validation_alias="DB_ECHO")
    demo_owner_id: str = Field(default="demo-owner", validation_alias="DEMO_OWNER_ID")
    mcp_enabled: bool = Field(default=False, validation_alias="MCP_ENABLED")
    gmail_enabled: bool = Field(default=False, validation_alias="GMAIL_ENABLED")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
