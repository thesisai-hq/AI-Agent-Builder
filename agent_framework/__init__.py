"""AI Agent Framework - Simple, maintainable AI agent builder.

Public API exports for clean imports:
    from agent_framework import Agent, Signal, LLMConfig, Database
"""

__version__ = "1.0.0"

# Core classes
from .agent import Agent

# API
from .api import app as api_app
from .api import clear_agents, register_agent_instance

# Utilities
from .config import Config

# Confidence Calculation
from .confidence import (
    ConfidenceCalculator,
    EnhancedConfidenceCalculator,
    calculate_simple_confidence,
    enhanced_parse_llm_signal,
)

# Database
from .database import ConnectionError, Database, DatabaseError, QueryError

# LLM and RAG
from .llm import APIError, LLMClient, LLMError, RateLimitError
from .models import AgentConfig, DatabaseConfig, LLMConfig, RAGConfig, Signal
from .rag import RAGError, RAGSystem
from .utils import calculate_sentiment_score, format_fundamentals, parse_llm_signal

__all__ = [
    # Core
    "Agent",
    "Signal",
    "AgentConfig",
    # Configuration
    "LLMConfig",
    "RAGConfig",
    "DatabaseConfig",
    "Config",
    # Components
    "LLMClient",
    "RAGSystem",
    "Database",
    # Exceptions
    "LLMError",
    "APIError",
    "RateLimitError",
    "RAGError",
    "DatabaseError",
    "ConnectionError",
    "QueryError",
    # API
    "api_app",
    "register_agent_instance",
    "clear_agents",
    # Utilities
    "parse_llm_signal",
    "format_fundamentals",
    "calculate_sentiment_score",
    # Confidence
    "ConfidenceCalculator",
    "EnhancedConfidenceCalculator",
    "calculate_simple_confidence",
    "enhanced_parse_llm_signal",
]
