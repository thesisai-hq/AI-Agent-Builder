"""AI Agent Framework - Simple, maintainable AI agent builder.

Public API exports for clean imports:
    from agent_framework import Agent, Signal, LLMConfig, Database
"""

__version__ = "1.0.0"

# Core classes
from .agent import Agent
from .models import (
    Signal, 
    LLMConfig, 
    RAGConfig, 
    AgentConfig,
    DatabaseConfig
)

# LLM and RAG
from .llm import LLMClient, LLMError, APIError, RateLimitError
from .rag import RAGSystem, RAGError

# Database
from .database import (
    Database, 
    DatabaseError, 
    ConnectionError,
    QueryError
)

# API
from .api import app as api_app, register_agent_instance, clear_agents

# Utilities
from .config import Config
from .utils import (
    parse_llm_signal,
    format_fundamentals,
    calculate_sentiment_score
)

__all__ = [
    # Core
    'Agent',
    'Signal',
    'AgentConfig',
    
    # Configuration
    'LLMConfig',
    'RAGConfig',
    'DatabaseConfig',
    'Config',
    
    # Components
    'LLMClient',
    'RAGSystem',
    'Database',
    
    # Exceptions
    'LLMError',
    'APIError',
    'RateLimitError',
    'RAGError',
    'DatabaseError',
    'ConnectionError',
    'QueryError',
    
    # API
    'api_app',
    'register_agent_instance',
    'clear_agents',
    
    # Utilities
    'parse_llm_signal',
    'format_fundamentals',
    'calculate_sentiment_score',
]
