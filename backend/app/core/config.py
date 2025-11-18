"""
Application configuration using Pydantic Settings
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Evently - Event Impact Analyzer"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API for analyzing economic and touristic impact of urban events"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Database
    DATABASE_URL: str = Field(
        default="postgresql://evently:evently123@localhost:5432/evently",
        env="DATABASE_URL"
    )

    # Security
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        env="SECRET_KEY"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # External APIs
    AIRROI_API_KEY: str = Field(default="", env="AIRROI_API_KEY")
    AIRROI_BASE_URL: str = "https://www.airroi.com/data-portal"

    # Analytics
    DEFAULT_ANALYSIS_WINDOW_DAYS: int = 30
    EVENT_IMPACT_WINDOW_BEFORE_DAYS: int = 14
    EVENT_IMPACT_WINDOW_AFTER_DAYS: int = 14

    # Pagination
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 1000

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
