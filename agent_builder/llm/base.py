"""Base LLM Provider Interface"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Standardized LLM response"""
    content: str
    model: str
    provider: str
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    finish_reason: Optional[str] = None
    
    def __str__(self):
        return self.content


class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers"""
    
    def __init__(self, model: str, **kwargs):
        self.model = model
        self.provider_name = self.__class__.__name__
        logger.info(f"Initialized {self.provider_name} with model: {model}")
    
    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        """Generate text completion"""
        pass
    
    @abstractmethod
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        """Chat completion with message history"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is accessible"""
        pass
    
    def _log_usage(self, response: LLMResponse):
        """Log token usage for monitoring"""
        if response.total_tokens:
            logger.info(
                f"{self.provider_name} usage: "
                f"{response.total_tokens} tokens "
                f"({response.prompt_tokens} prompt + "
                f"{response.completion_tokens} completion)"
            )
