"""
Application configuration management.
Centralizes all configuration and environment variables.
"""
from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "Assembly Factory API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # CORS
    ALLOWED_ORIGINS: str = "https://assembly-factory.vercel.app"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse ALLOWED_ORIGINS string into a list."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    # Service Ports (for supervisor/docker)
    DESIGN_PORT: int = 8001
    ASSEMBLY_PORT: int = 8002
    QUALITY_PORT: int = 8003
    PACKAGING_PORT: int = 8004
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Using lru_cache ensures we only create one instance.
    """
    return Settings()


settings = get_settings()
