"""
LLM Provider Factory
"""

from agent_builder.llm.base import LLMProvider
from agent_builder.llm.ollama import OllamaProvider
from agent_builder.llm.groq import GroqProvider
from agent_builder.config import Config
from typing import Optional
import os
import logging

logger = logging.getLogger(__name__)


def get_llm_provider(
    provider_name: Optional[str] = None, model: Optional[str] = None
) -> Optional[LLMProvider]:
    """
    Get LLM provider based on configuration

    Args:
        provider_name: 'ollama' or 'groq' (defaults to config)
        model: Model name (defaults to provider default)

    Returns:
        LLMProvider instance or None if not configured

    Usage:
        llm = get_llm_provider()
        response = llm.generate("Analyze AAPL")
    """
    provider_name = provider_name or os.getenv("LLM_PROVIDER", "ollama")

    if provider_name == "ollama":
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        model = model or os.getenv("OLLAMA_MODEL", "llama3.2")

        logger.info(f"Using Ollama: {model} at {base_url}")
        return OllamaProvider(base_url=base_url, model=model)

    elif provider_name == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        model = model or os.getenv("GROQ_MODEL", "llama3-8b-8192")

        if not api_key:
            logger.error("GROQ_API_KEY not set in .env")
            return None

        logger.info(f"Using Groq: {model}")
        return GroqProvider(api_key=api_key, model=model)

    else:
        logger.warning(f"Unknown LLM provider: {provider_name}")
        return None
