import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator

# Read values from .env into the process environment before Settings is created.
load_dotenv()


class Settings(BaseModel):
    """Central place for application configuration."""

    APP_NAME: str = "AI Research Agent"
    APP_VERSION: str = "0.1.0"
    LOG_LEVEL: str = "INFO"
    TAVILY_API_KEY: str | None = None
    DEFAULT_SEARCH_RESULTS: int = Field(default=5, ge=1, le=10)
    TAVILY_SEARCH_DEPTH: str = "advanced"
    EXTRACTION_TIMEOUT_SECONDS: int = Field(default=10, ge=1, le=30)

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        allowed_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        normalized = value.upper()
        if normalized not in allowed_levels:
            raise ValueError(f"LOG_LEVEL must be one of: {', '.join(sorted(allowed_levels))}")
        return normalized

    @field_validator("TAVILY_SEARCH_DEPTH")
    @classmethod
    def validate_search_depth(cls, value: str) -> str:
        allowed_depths = {"basic", "advanced"}
        normalized = value.lower()
        if normalized not in allowed_depths:
            raise ValueError("TAVILY_SEARCH_DEPTH must be either 'basic' or 'advanced'.")
        return normalized

    def validate_required_secrets(self) -> None:
        """Fail fast when required runtime secrets are missing."""
        if not self.TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY is missing. Add it to your .env file.")


settings = Settings(
    APP_NAME=os.getenv("APP_NAME", "AI Research Agent"),
    APP_VERSION=os.getenv("APP_VERSION", "0.1.0"),
    LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO"),
    TAVILY_API_KEY=os.getenv("TAVILY_API_KEY"),
    DEFAULT_SEARCH_RESULTS=os.getenv("DEFAULT_SEARCH_RESULTS", "5"),
    TAVILY_SEARCH_DEPTH=os.getenv("TAVILY_SEARCH_DEPTH", "advanced"),
    EXTRACTION_TIMEOUT_SECONDS=os.getenv("EXTRACTION_TIMEOUT_SECONDS", "10"),
)
