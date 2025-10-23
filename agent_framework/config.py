"""Centralized configuration management."""

import os
from typing import Optional


class Config:
    """Application configuration with environment variable support."""
    
    @staticmethod
    def get_database_url(env_var: str = 'DATABASE_URL') -> str:
        """Get database connection string from environment.
        
        Args:
            env_var: Environment variable name
            
        Returns:
            Database connection string
        """
        return os.getenv(
            env_var,
            'postgresql://postgres:postgres@localhost:5432/agent_framework'
        )
    
    @staticmethod
    def get_test_database_url() -> str:
        """Get test database connection string.
        
        Uses separate database for tests to avoid data pollution.
        """
        return os.getenv(
            'TEST_DATABASE_URL',
            'postgresql://postgres:postgres@localhost:5432/agent_framework_test'
        )
    
    @staticmethod
    def get_llm_api_key(provider: str) -> Optional[str]:
        """Get LLM API key from environment.
        
        Args:
            provider: LLM provider name (openai, anthropic)
            
        Returns:
            API key or None
        """
        key_map = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
        }
        env_var = key_map.get(provider.lower())
        return os.getenv(env_var) if env_var else None
    
    @staticmethod
    def get_ollama_url() -> str:
        """Get Ollama base URL."""
        return os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')