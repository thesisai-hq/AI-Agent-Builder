"""Configuration management for GUI system."""

from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import List
from pathlib import Path


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # API Configuration
    api_title: str = "AI Agent Builder - GUI System"
    api_description: str = "Web-based GUI for creating and managing AI investment agents"
    api_version: str = "1.0.0"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    
    # CORS Configuration (can be overridden via CORS_ORIGINS env var)
    cors_origins: List[str] = Field(
        default=[
            "http://localhost:5173",
            "http://localhost:5174",
            "http://localhost:4173",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:5174",
            "http://127.0.0.1:4173",
        ],
        description="Allowed CORS origins (comma-separated string or list)"
    )
    
    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        return v
    
    # Storage Configuration
    storage_path: str = Field(
        default="gui_system/storage",
        description="Path to storage directory for agents and templates"
    )
    
    # Agent Configuration
    max_position_size: float = Field(default=100.0, gt=0)
    default_position_size: float = Field(default=10.0, gt=0)
    min_position_size: float = Field(default=1.0, gt=0)
    
    # Logging Configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Cache Configuration
    cache_ttl_seconds: int = Field(
        default=300,
        description="Cache time-to-live in seconds (default: 5 minutes)"
    )
    
    # Feature Flags
    enable_formula_validation: bool = True
    enable_llm_agents: bool = True
    enable_data_cache: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """FastAPI dependency for settings."""
    return settings
