import os

from dotenv import load_dotenv

# Read values from .env into the process environment before Settings is created.
load_dotenv()


class Settings:
    """Central place for application configuration."""

    def __init__(self) -> None:
        self.TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

    def validate(self) -> None:
        """Fail fast when required configuration is missing."""
        if not self.TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY is missing. Add it to your .env file.")


# Reusable settings instance imported by the rest of the application.
settings = Settings()
