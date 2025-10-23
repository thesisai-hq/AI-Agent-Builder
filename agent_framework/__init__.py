"""AI Agent Framework - Simple, maintainable AI agent builder with PostgreSQL.

Public API exports for clean imports:
    from agent_framework import Agent, Signal, LLMConfig, Database
"""

__version__ = "1.0.0"

# Core classes
from .agent import Agent
from .models import Signal, LLMConfig, RAGConfig, AgentConfig

# LLM and RAG
from .llm import LLMClient
from .rag import RAGSystem

# Database
from .database import Database, get_database

# API
from .api import app as api_app, register_agent_instance

__all__ = [
    # Core
    'Agent',
    'Signal',
    'AgentConfig',
    
    # Configuration
    'LLMConfig',
    'RAGConfig',
    
    # Components
    'LLMClient',
    'RAGSystem',
    'Database',
    'get_database',
    
    # API
    'api_app',
    'register_agent_instance',
]