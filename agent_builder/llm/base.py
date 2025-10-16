"""
Base LLM Provider Interface - WITH SYSTEM PROMPT SUPPORT
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""

    def __init__(self, model: str):
        self.model = model

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
        **kwargs
    ) -> str:
        """
        Generate text from prompt

        Args:
            prompt: User prompt
            system_prompt: System prompt (sets AI personality/role)
            temperature: Randomness (0.0-1.0)
            max_tokens: Maximum response length

        Returns:
            Generated text
        """
        pass

    def chat(
        self, messages: list, temperature: float = 0.7, max_tokens: int = 500, **kwargs
    ) -> str:
        """Chat completion with message history"""
        pass
