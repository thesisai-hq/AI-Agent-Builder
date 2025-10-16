"""
Groq LLM Provider - WITH SYSTEM PROMPT SUPPORT
"""

import requests
from typing import Optional
from agent_builder.llm.base import LLMProvider
import os
import logging

logger = logging.getLogger(__name__)


class GroqProvider(LLMProvider):
    """
    Groq LLM Provider with system prompt support

    Example with persona:
        llm = GroqProvider()
        response = llm.generate(
            prompt="Analyze AAPL",
            system_prompt="You are a risk-focused analyst who prioritizes downside protection"
        )
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "llama3-8b-8192"):
        super().__init__(model)
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1"

        if not self.api_key:
            logger.warning("GROQ_API_KEY not set")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
        **kwargs,
    ) -> str:
        """Generate text with optional system prompt"""
        messages = []

        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # Add user prompt
        messages.append({"role": "user", "content": prompt})

        return self.chat(messages, temperature, max_tokens, **kwargs)

    def chat(
        self, messages: list, temperature: float = 0.7, max_tokens: int = 500, **kwargs
    ) -> str:
        """Chat completion with full message history"""
        if not self.api_key:
            logger.error("GROQ_API_KEY not configured")
            return ""

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                },
                timeout=30,
            )

            response.raise_for_status()
            result = response.json()

            return result["choices"][0]["message"]["content"]

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                logger.error("Invalid GROQ_API_KEY")
            elif e.response.status_code == 429:
                logger.error("Rate limit exceeded")
            else:
                logger.error(f"Groq API error: {e}")
            return ""
        except Exception as e:
            logger.error(f"Groq generation error: {e}")
            return ""

    def is_available(self) -> bool:
        """Check if Groq API is accessible"""
        if not self.api_key:
            return False

        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=5,
            )
            return response.status_code == 200
        except:
            return False
