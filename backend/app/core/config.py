from typing import Dict, List
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "Shadow Awakening"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:password@localhost:5432/shadow_awakening",
    )
    DATABASE_URL_SYNC: str = os.getenv(
        "DATABASE_URL_SYNC",
        "postgresql://postgres:password@localhost:5432/shadow_awakening",
    )

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "shadow-awakening-dev-secret-key-2024")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # CORS
    CORS_ORIGINS: str = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:3000",
    )

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def database_url_async(self) -> str:
        """
        Normalize DATABASE_URL for SQLAlchemy async + asyncpg.

        - Converts postgresql:// -> postgresql+asyncpg://
        - Removes URL params such as sslmode/channel_binding that asyncpg should not
          receive as raw kwargs through SQLAlchemy.
        """
        url = self.DATABASE_URL.strip()
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)

        parsed = urlparse(url)
        cleaned_query = [
            (key, value)
            for key, value in parse_qsl(parsed.query, keep_blank_values=True)
            if key not in {"sslmode", "channel_binding"}
        ]
        return urlunparse(parsed._replace(query=urlencode(cleaned_query)))

    @property
    def database_connect_args(self) -> Dict[str, object]:
        """
        asyncpg expects `ssl`, not `sslmode`.
        Neon requires SSL, so we enable it automatically when needed.
        """
        raw = self.DATABASE_URL.lower()
        if "sslmode=require" in raw or ".neon.tech" in raw:
            return {"ssl": True}
        return {}

    class Config:
        env_file = ".env"


settings = Settings()
