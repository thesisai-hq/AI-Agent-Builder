"""Configuration management for GUI system."""

from pydantic_settings import BaseSettings
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
    
    # CORS Configuration
    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:4173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:4173",
    ]
    
    # Storage Configuration
    storage_path: str = "gui_system/storage"
    
    # Agent Configuration
    max_position_size: float = 100.0
    default_position_size: float = 10.0
    min_position_size: float = 1.0
    
    # Logging Configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Feature Flags
    enable_formula_validation: bool = True
    enable_llm_agents: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """FastAPI dependency for settings."""
    return settings
