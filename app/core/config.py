from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# CW1 polish: make .env loading deterministic even if you run uvicorn/pytest from a different cwd
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        extra="ignore",
    )

    database_url: str = "sqlite:///./app.db"
    api_key: str = "change-me"


settings = Settings()