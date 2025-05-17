from pydantic import BaseSettings
import os
from pathlib import Path

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    VECTOR_DB_URL: str

    class Config:
        env_file = ".env"
