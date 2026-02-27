"""Configuration settings loaded from environment or .env file."""

from pydantic import BaseSettings, AnyUrl
from typing import Optional


class Settings(BaseSettings):
    """Application configuration container.

    Attributes are loaded from environment variables or a .env file.
    """

    # General
    ENV: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: AnyUrl

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # AWS
    AWS_REGION: str
    AWS_S3_BUCKET: str
    # Bedrock service name may vary
    BEDROCK_MODEL_ID: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
