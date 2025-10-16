"""
Centralized Configuration - UPDATED with LLM settings
"""

import os
from urllib.parse import urlparse
from typing import Optional, Dict
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration - Single source of truth"""

    # API Configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"

    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "memory")

    # CORS
    CORS_ORIGINS = os.getenv(
        "CORS_ORIGINS", "http://localhost:3000,http://localhost:8080"
    ).split(",")

    # LLM Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")  # ollama or groq

    # Ollama Settings
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

    # Groq Settings
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")

    # Sentiment Analyzer Configuration
    SENTIMENT_ANALYZER = os.getenv("SENTIMENT_ANALYZER", "vader")  # vader or finbert
    FINBERT_MODEL = os.getenv("FINBERT_MODEL", "ProsusAI/finbert")

    @classmethod
    def get_db_params(cls) -> Optional[Dict[str, any]]:
        """Parse DATABASE_URL into connection parameters"""
        if cls.DATABASE_URL == "memory":
            return None

        if cls.DATABASE_URL.startswith("postgresql"):
            parsed = urlparse(cls.DATABASE_URL)
            return {
                "host": parsed.hostname or "localhost",
                "port": parsed.port or 5432,
                "database": parsed.path.lstrip("/"),
                "user": parsed.username,
                "password": parsed.password,
            }

        return None

    @classmethod
    def is_postgres(cls) -> bool:
        """Check if using PostgreSQL"""
        return cls.DATABASE_URL.startswith("postgresql")

    @classmethod
    def is_memory(cls) -> bool:
        """Check if using in-memory storage"""
        return cls.DATABASE_URL == "memory"

    @classmethod
    def has_llm(cls) -> bool:
        """Check if LLM is configured"""
        if cls.LLM_PROVIDER == "ollama":
            return True  # Assume Ollama available locally
        elif cls.LLM_PROVIDER == "groq":
            return bool(cls.GROQ_API_KEY)
        return False
