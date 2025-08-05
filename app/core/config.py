"""Application configuration."""
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Math Operations Microservice"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A microservice for mathematical operations with caching and persistence"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    
    # Database Configuration
    DATABASE_URL: Optional[str] = None
    
    # Cache Configuration
    CACHE_TTL_SECONDS: int = 3600
    CACHE_MAX_SIZE: int = 1000
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        """Pydantic settings config."""
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()