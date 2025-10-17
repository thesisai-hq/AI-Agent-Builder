"""LLM Provider Implementations"""

import os
import requests
from typing import Optional, List, Dict
import logging

from agent_builder.llm.base import BaseLLMProvider, LLMResponse

logger = logging.getLogger(__name__)


# ============================================================================
# OLLAMA PROVIDER (Local)
# ============================================================================


class OllamaProvider(BaseLLMProvider):
    """
    Ollama provider for local LLM inference

    Setup:
        1. Install Ollama: https://ollama.ai
        2. Pull model: ollama pull llama3.2
        3. Start: ollama serve

    Usage:
        llm = OllamaProvider(model="llama3.2")
        response = llm.generate("Analyze Apple stock")
    """

    def __init__(
        self,
        model: str = "llama3.2",
        base_url: str = "http://localhost:11434",
        timeout: int = 60,
    ):
        super().__init__(model)
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._model_loaded = False

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs,
    ) -> LLMResponse:
        """Generate with Ollama"""
        try:
            # Build messages
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            return self.chat(messages, temperature, max_tokens, **kwargs)

        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            return LLMResponse(
                content=f"Error: {str(e)}", model=self.model, provider="ollama"
            )

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs,
    ) -> LLMResponse:
        """Chat with Ollama"""
        try:
            if not self._model_loaded:
                logger.info(f"First run - loading {self.model} (may take 30-60s)...")

            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens,
                    },
                },
                timeout=self.timeout,
            )

            response.raise_for_status()
            result = response.json()

            self._model_loaded = True

            content = result.get("message", {}).get("content", "")

            return LLMResponse(
                content=content,
                model=self.model,
                provider="ollama",
                prompt_tokens=result.get("prompt_eval_count"),
                completion_tokens=result.get("eval_count"),
                total_tokens=(
                    result.get("prompt_eval_count", 0) + result.get("eval_count", 0)
                ),
                finish_reason="stop",
            )

        except requests.exceptions.Timeout:
            logger.error(f"Ollama timeout after {self.timeout}s")
            return LLMResponse(
                content="Error: Request timeout", model=self.model, provider="ollama"
            )
        except requests.exceptions.ConnectionError:
            logger.error(f"Cannot connect to Ollama at {self.base_url}")
            return LLMResponse(
                content="Error: Cannot connect to Ollama. Is it running?",
                model=self.model,
                provider="ollama",
            )
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return LLMResponse(
                content=f"Error: {str(e)}", model=self.model, provider="ollama"
            )

    def is_available(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False


# ============================================================================
# OPENAI PROVIDER (API)
# ============================================================================


class OpenAIProvider(BaseLLMProvider):
    """
    OpenAI provider for GPT models

    Setup:
        1. Get API key: https://platform.openai.com/api-keys
        2. Set environment: export OPENAI_API_KEY=sk-...

    Usage:
        llm = OpenAIProvider(model="gpt-4", api_key="sk-...")
        response = llm.generate("Analyze Apple stock")
    """

    def __init__(
        self,
        model: str = "gpt-4",
        api_key: Optional[str] = None,
        base_url: str = "https://api.openai.com/v1",
        timeout: int = 30,
    ):
        super().__init__(model)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url
        self.timeout = timeout

        if not self.api_key:
            logger.warning("OpenAI API key not set")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs,
    ) -> LLMResponse:
        """Generate with OpenAI"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        return self.chat(messages, temperature, max_tokens, **kwargs)

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs,
    ) -> LLMResponse:
        """Chat with OpenAI"""
        if not self.api_key:
            return LLMResponse(
                content="Error: OpenAI API key not configured",
                model=self.model,
                provider="openai",
            )

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
                timeout=self.timeout,
            )

            response.raise_for_status()
            result = response.json()

            choice = result["choices"][0]
            usage = result.get("usage", {})

            return LLMResponse(
                content=choice["message"]["content"],
                model=result["model"],
                provider="openai",
                prompt_tokens=usage.get("prompt_tokens"),
                completion_tokens=usage.get("completion_tokens"),
                total_tokens=usage.get("total_tokens"),
                finish_reason=choice.get("finish_reason"),
            )

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                logger.error("Invalid OpenAI API key")
            elif e.response.status_code == 429:
                logger.error("OpenAI rate limit exceeded")
            else:
                logger.error(f"OpenAI HTTP error: {e}")
            return LLMResponse(
                content=f"Error: {str(e)}", model=self.model, provider="openai"
            )
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return LLMResponse(
                content=f"Error: {str(e)}", model=self.model, provider="openai"
            )

    def is_available(self) -> bool:
        """Check if OpenAI API is accessible"""
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


# ============================================================================
# ANTHROPIC PROVIDER (Claude)
# ============================================================================


class AnthropicProvider(BaseLLMProvider):
    """
    Anthropic provider for Claude models

    Setup:
        1. Get API key: https://console.anthropic.com/
        2. Set environment: export ANTHROPIC_API_KEY=sk-ant-...

    Usage:
        llm = AnthropicProvider(model="claude-3-sonnet-20240229")
        response = llm.generate("Analyze Apple stock")
    """

    def __init__(
        self,
        model: str = "claude-3-sonnet-20240229",
        api_key: Optional[str] = None,
        base_url: str = "https://api.anthropic.com/v1",
        timeout: int = 30,
    ):
        super().__init__(model)
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.base_url = base_url
        self.timeout = timeout
        self.api_version = "2023-06-01"

        if not self.api_key:
            logger.warning("Anthropic API key not set")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs,
    ) -> LLMResponse:
        """Generate with Claude"""
        try:
            payload = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [{"role": "user", "content": prompt}],
            }

            if system_prompt:
                payload["system"] = system_prompt

            response = requests.post(
                f"{self.base_url}/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": self.api_version,
                    "content-type": "application/json",
                },
                json=payload,
                timeout=self.timeout,
            )

            response.raise_for_status()
            result = response.json()

            content = result["content"][0]["text"]
            usage = result.get("usage", {})

            return LLMResponse(
                content=content,
                model=result["model"],
                provider="anthropic",
                prompt_tokens=usage.get("input_tokens"),
                completion_tokens=usage.get("output_tokens"),
                total_tokens=(
                    usage.get("input_tokens", 0) + usage.get("output_tokens", 0)
                ),
                finish_reason=result.get("stop_reason"),
            )

        except Exception as e:
            logger.error(f"Anthropic error: {e}")
            return LLMResponse(
                content=f"Error: {str(e)}", model=self.model, provider="anthropic"
            )

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs,
    ) -> LLMResponse:
        """Chat with Claude"""
        # Extract system message if present
        system_prompt = None
        user_messages = []

        for msg in messages:
            if msg["role"] == "system":
                system_prompt = msg["content"]
            else:
                user_messages.append(msg)

        # For multi-turn, use last user message
        if user_messages:
            prompt = user_messages[-1]["content"]
            return self.generate(
                prompt, system_prompt, temperature, max_tokens, **kwargs
            )

        return LLMResponse(
            content="Error: No user message provided",
            model=self.model,
            provider="anthropic",
        )

    def is_available(self) -> bool:
        """Check if Anthropic API is accessible"""
        if not self.api_key:
            return False
        # Could add actual API check here
        return True


# ============================================================================
# FACTORY FUNCTION
# ============================================================================


def get_llm_provider(
    provider: str = "ollama", model: Optional[str] = None, **kwargs
) -> Optional[BaseLLMProvider]:
    """
    Factory function to get LLM provider

    Args:
        provider: "ollama", "openai", or "anthropic"
        model: Model name (uses default if not specified)
        **kwargs: Provider-specific arguments

    Returns:
        LLM provider instance or None

    Usage:
        # Ollama
        llm = get_llm_provider("ollama", model="llama3.2")

        # OpenAI
        llm = get_llm_provider("openai", model="gpt-4", api_key="sk-...")

        # Anthropic
        llm = get_llm_provider("anthropic", model="claude-3-sonnet-20240229")
    """
    provider = provider.lower()

    if provider == "ollama":
        model = model or os.getenv("OLLAMA_MODEL", "llama3.2")
        base_url = kwargs.get(
            "base_url", os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )
        return OllamaProvider(model=model, base_url=base_url)

    elif provider == "openai":
        model = model or os.getenv("OPENAI_MODEL", "gpt-4")
        api_key = kwargs.get("api_key", os.getenv("OPENAI_API_KEY"))
        return OpenAIProvider(model=model, api_key=api_key)

    elif provider == "anthropic":
        model = model or os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
        api_key = kwargs.get("api_key", os.getenv("ANTHROPIC_API_KEY"))
        return AnthropicProvider(model=model, api_key=api_key)

    else:
        logger.error(f"Unknown provider: {provider}")
        return None
