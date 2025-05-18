from pydantic.v1 import BaseSettings, Field
from functools import lru_cache

class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    VECTOR_DB_URL: str = Field(..., env="VECTOR_DB_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()