import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings

from ..utils import get_root_path

BASE_DIR = get_root_path(Path(__file__).resolve())
ENV_DIR = BASE_DIR / "environment"


class BaseConfig(BaseSettings):
    ENV: str = "dev"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8080
    WRITER_DB_URL: str = (
        "mysql+aiomysql://fastapi:fastapi@localhost:33306/kokoro?timezone=UTC"
    )
    READER_DB_URL: str = (
        "mysql+aiomysql://fastapi:fastapi@localhost:33306/kokoro?timezone=UTC"
    )
    JWT_SECRET_KEY: str = "kokoro"
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = ENV_DIR / ".env.development"  # fallback
        env_file_encoding = "utf-8"


class DevelopmentConfig(BaseConfig):
    class Config(BaseConfig.Config):
        env_file = ENV_DIR / ".env.development"


class ProductionConfig(BaseConfig):
    class Config(BaseConfig.Config):
        env_file = ENV_DIR / ".env.production"


@lru_cache()
def get_settings() -> BaseConfig:
    env = os.getenv("ENV", "dev").lower()
    if env == "prod":
        return ProductionConfig()
    return DevelopmentConfig()
