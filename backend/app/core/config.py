from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "Shadow Awakening"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:password@localhost:5432/shadow_awakening"
    )
    DATABASE_URL_SYNC: str = os.getenv(
        "DATABASE_URL_SYNC",
        "postgresql://postgres:password@localhost:5432/shadow_awakening"
    )
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "shadow-awakening-dev-secret-key-2024")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # CORS
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"


settings = Settings()
