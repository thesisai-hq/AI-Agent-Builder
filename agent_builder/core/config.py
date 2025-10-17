"""Configuration management"""

import os
from dataclasses import dataclass, field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass
class DatabaseConfig:
    url: str
    min_connections: int = 2
    max_connections: int = 10
    
    @property
    def is_postgres(self) -> bool:
        return self.url.startswith("postgresql")


@dataclass
class LLMConfig:
    provider: str
    model: str
    base_url: Optional[str] = None
    api_key: Optional[str] = None


@dataclass
class Config:
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    cors_origins: list = field(default_factory=lambda: ["http://localhost:3000"])
    database: DatabaseConfig = None
    llm: LLMConfig = None
    
    @classmethod
    def from_env(cls):
        return cls(
            host=os.getenv("API_HOST", "0.0.0.0"),
            port=int(os.getenv("API_PORT", 8000)),
            debug=os.getenv("DEBUG", "true").lower() == "true",
            cors_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
            database=DatabaseConfig(
                url=os.getenv("DATABASE_URL", "memory"),
                min_connections=int(os.getenv("DB_MIN_CONN", 2)),
                max_connections=int(os.getenv("DB_MAX_CONN", 10)),
            ),
            llm=LLMConfig(
                provider=os.getenv("LLM_PROVIDER", "ollama"),
                model=os.getenv("LLM_MODEL", "llama3.2"),
                base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434"),
                api_key=os.getenv("LLM_API_KEY"),
            ),
        )
