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
    mcp_server_name: str = Field(default="Tavily", validation_alias="MCP_SERVER_NAME")
    mcp_research_tool: str = Field(default="tavily_research", validation_alias="MCP_RESEARCH_TOOL")
    mcp_cli_path: str = Field(default="manus-mcp-cli", validation_alias="MCP_CLI_PATH")
    mcp_timeout_seconds: int = Field(default=90, validation_alias="MCP_TIMEOUT_SECONDS")
    manus_enabled: bool = Field(default=False, validation_alias="MANUS_ENABLED")
    manus_api_key: str | None = Field(default=None, validation_alias="MANUS_API_KEY")
    manus_api_base_url: str = Field(default="https://api.manus.ai", validation_alias="MANUS_API_BASE_URL")
    manus_timeout_seconds: int = Field(default=180, validation_alias="MANUS_TIMEOUT_SECONDS")
    manus_poll_interval_seconds: int = Field(default=4, validation_alias="MANUS_POLL_INTERVAL_SECONDS")
    llm_enabled: bool = Field(default=False, validation_alias="LLM_ENABLED")
    llm_api_key: str | None = Field(default=None, validation_alias="LLM_API_KEY")
    llm_base_url: str | None = Field(default=None, validation_alias="LLM_BASE_URL")
    llm_model: str = Field(default="gpt-5", validation_alias="LLM_MODEL")
    llm_timeout_seconds: int = Field(default=90, validation_alias="LLM_TIMEOUT_SECONDS")
    llm_reasoning_effort: str = Field(default="medium", validation_alias="LLM_REASONING_EFFORT")
    mock_profiles_enabled: bool = Field(default=True, validation_alias="MOCK_PROFILES_ENABLED")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
