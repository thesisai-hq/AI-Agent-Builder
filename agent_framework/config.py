"""Centralized configuration management with environment variable support.

All configuration values should be defined here and read from environment variables.
This ensures easy deployment across different environments (dev, test, prod).
"""

import os
from typing import Optional
from pathlib import Path

# Load .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    # python-dotenv not installed, will use system environment variables
    pass


class Config:
    """Application configuration with environment variable support.
    
    All hardcoded values have been moved here from various files.
    Change behavior by setting environment variables in .env file.
    """
    
    # ========================================
    # Database Configuration
    # ========================================
    
    @staticmethod
    def get_db_host() -> str:
        """Get database host."""
        return os.getenv('DB_HOST', 'localhost')
    
    @staticmethod
    def get_db_port() -> int:
        """Get database port."""
        return int(os.getenv('DB_PORT', '5433'))
    
    @staticmethod
    def get_db_user() -> str:
        """Get database user."""
        return os.getenv('DB_USER', 'postgres')
    
    @staticmethod
    def get_db_password() -> str:
        """Get database password."""
        return os.getenv('DB_PASSWORD', 'postgres')
    
    @staticmethod
    def get_db_name() -> str:
        """Get database name."""
        return os.getenv('DB_NAME', 'agent_framework')
    
    @staticmethod
    def get_test_db_name() -> str:
        """Get test database name."""
        return os.getenv('TEST_DB_NAME', 'agent_framework_test')
    
    @staticmethod
    def get_database_url(env_var: str = 'DATABASE_URL') -> str:
        """Get database connection string from environment.
        
        If DATABASE_URL is not set, constructs it from individual components.
        
        Args:
            env_var: Environment variable name for full connection string
            
        Returns:
            PostgreSQL connection string
        """
        # Allow override with full connection string
        url = os.getenv(env_var)
        if url:
            return url
        
        # Construct from components
        host = Config.get_db_host()
        port = Config.get_db_port()
        user = Config.get_db_user()
        password = Config.get_db_password()
        dbname = Config.get_db_name()
        
        return f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
    
    @staticmethod
    def get_test_database_url() -> str:
        """Get test database connection string.
        
        Uses separate database for tests to avoid data pollution.
        """
        # Allow override with full connection string
        url = os.getenv('TEST_DATABASE_URL')
        if url:
            return url
        
        # Construct from components
        host = Config.get_db_host()
        port = Config.get_db_port()
        user = Config.get_db_user()
        password = Config.get_db_password()
        dbname = Config.get_test_db_name()
        
        return f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
    
    # Database pool configuration
    @staticmethod
    def get_db_min_pool_size() -> int:
        """Get minimum database connection pool size."""
        return int(os.getenv('DB_MIN_POOL_SIZE', '2'))
    
    @staticmethod
    def get_db_max_pool_size() -> int:
        """Get maximum database connection pool size."""
        return int(os.getenv('DB_MAX_POOL_SIZE', '10'))
    
    @staticmethod
    def get_db_command_timeout() -> int:
        """Get database command timeout in seconds."""
        return int(os.getenv('DB_COMMAND_TIMEOUT', '60'))
    
    @staticmethod
    def get_db_max_queries() -> int:
        """Get maximum queries per connection."""
        return int(os.getenv('DB_MAX_QUERIES', '50000'))
    
    @staticmethod
    def get_db_max_inactive_connection_lifetime() -> float:
        """Get maximum inactive connection lifetime in seconds."""
        return float(os.getenv('DB_MAX_INACTIVE_CONNECTION_LIFETIME', '300.0'))
    
    # ========================================
    # API Configuration
    # ========================================
    
    @staticmethod
    def get_api_host() -> str:
        """Get API host."""
        return os.getenv('API_HOST', '0.0.0.0')
    
    @staticmethod
    def get_api_port() -> int:
        """Get API port."""
        return int(os.getenv('API_PORT', '8000'))
    
    @staticmethod
    def get_debug() -> bool:
        """Get debug mode setting."""
        return os.getenv('DEBUG', 'True').lower() in ('true', '1', 'yes')
    
    @staticmethod
    def get_cors_origins() -> list:
        """Get CORS allowed origins.
        
        Returns list of origins or ['*'] for all.
        """
        origins = os.getenv('CORS_ORIGINS', '*')
        if origins == '*':
            return ['*']
        return [origin.strip() for origin in origins.split(',')]
    
    # ========================================
    # LLM Configuration
    # ========================================
    
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
    def get_llm_model(provider: str) -> str:
        """Get default LLM model for provider."""
        defaults = {
            'openai': 'gpt-4',
            'anthropic': 'claude-3-5-sonnet-20241022',
            'ollama': 'llama3.2'
        }
        env_var = f'{provider.upper()}_MODEL'
        return os.getenv(env_var, defaults.get(provider.lower(), ''))
    
    @staticmethod
    def get_llm_temperature(provider: str) -> float:
        """Get LLM temperature for provider."""
        env_var = f'{provider.upper()}_TEMPERATURE'
        return float(os.getenv(env_var, '0.7'))
    
    @staticmethod
    def get_llm_max_tokens(provider: str) -> int:
        """Get LLM max tokens for provider."""
        env_var = f'{provider.upper()}_MAX_TOKENS'
        return int(os.getenv(env_var, '1000'))
    
    @staticmethod
    def get_llm_timeout(provider: str) -> int:
        """Get LLM timeout for provider."""
        env_var = f'{provider.upper()}_TIMEOUT'
        return int(os.getenv(env_var, '60'))
    
    @staticmethod
    def get_llm_max_retries() -> int:
        """Get LLM max retries."""
        return int(os.getenv('LLM_MAX_RETRIES', '3'))
    
    @staticmethod
    def get_ollama_url() -> str:
        """Get Ollama base URL."""
        return os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    
    # ========================================
    # RAG Configuration
    # ========================================
    
    @staticmethod
    def get_rag_chunk_size() -> int:
        """Get RAG chunk size."""
        return int(os.getenv('RAG_CHUNK_SIZE', '500'))
    
    @staticmethod
    def get_rag_chunk_overlap() -> int:
        """Get RAG chunk overlap."""
        return int(os.getenv('RAG_CHUNK_OVERLAP', '50'))
    
    @staticmethod
    def get_rag_top_k() -> int:
        """Get RAG top-k results."""
        return int(os.getenv('RAG_TOP_K', '3'))
    
    @staticmethod
    def get_rag_embedding_model() -> str:
        """Get RAG embedding model."""
        return os.getenv('RAG_EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
    
    # ========================================
    # Logging Configuration
    # ========================================
    
    @staticmethod
    def get_log_level() -> str:
        """Get logging level."""
        return os.getenv('LOG_LEVEL', 'INFO')
