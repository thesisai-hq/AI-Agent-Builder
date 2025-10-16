"""
Ollama LLM Provider - OPTIMIZED for first-run performance
"""

import requests
from typing import Optional
from agent_builder.llm.base import LLMProvider
import logging

logger = logging.getLogger(__name__)


class OllamaProvider(LLMProvider):
    """
    Ollama LLM Provider - OPTIMIZED

    Improvements:
    - Configurable timeout (default 60s for first run)
    - Warmup method to preload model
    - Better error messages
    """

    def __init__(
        self, model: str = "llama3.2", base_url: str = "http://localhost:11434"
    ):
        super().__init__(model)
        self.base_url = base_url.rstrip("/")
        self._model_loaded = False

    def warmup(self):
        """
        Warm up the model (load into memory)

        First generation is slow because Ollama loads the model.
        Call this once at startup to preload.

        Usage:
            llm = OllamaProvider()
            llm.warmup()  # Preload model
            # Future calls will be fast!
        """
        logger.info(f"Warming up Ollama model: {self.model}")
        try:
            # Simple generation to load model
            self.generate("hello", max_tokens=5, timeout=90)
            self._model_loaded = True
            logger.info(f"✅ Model {self.model} loaded and ready")
        except Exception as e:
            logger.warning(f"Warmup failed: {e}")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
        timeout: int = 60,
        **kwargs,
    ) -> str:
        """
        Generate text with configurable timeout

        Args:
            timeout: Request timeout in seconds (default: 60)
                    First run may be slow (model loading)
                    Subsequent runs are fast
        """
        # If system prompt provided, use chat API
        if system_prompt:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ]
            return self.chat(messages, temperature, max_tokens, timeout=timeout)

        try:
            # Log if first run
            if not self._model_loaded:
                logger.info(
                    f"First run - loading model {self.model} (may take 30-60s)..."
                )

            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens,
                    },
                },
                timeout=timeout,
            )

            response.raise_for_status()
            result = response.json()

            self._model_loaded = True
            return result.get("response", "")

        except requests.exceptions.Timeout:
            logger.error(
                f"Ollama timeout after {timeout}s - try increasing timeout or warmup first"
            )
            return ""
        except requests.exceptions.ConnectionError:
            logger.error(f"Cannot connect to Ollama at {self.base_url}")
            logger.error("Make sure Ollama is running: ollama serve")
            return ""
        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            return ""

    def chat(
        self,
        messages: list,
        temperature: float = 0.7,
        max_tokens: int = 500,
        timeout: int = 60,
        **kwargs,
    ) -> str:
        """Chat completion with configurable timeout"""
        try:
            if not self._model_loaded:
                logger.info(
                    f"First run - loading model {self.model} (may take 30-60s)..."
                )

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
                timeout=timeout,
            )

            response.raise_for_status()
            result = response.json()

            self._model_loaded = True
            return result.get("message", {}).get("content", "")

        except requests.exceptions.Timeout:
            logger.error(f"Ollama timeout after {timeout}s")
            return ""
        except Exception as e:
            logger.error(f"Ollama chat error: {e}")
            return ""

    def is_available(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def list_models(self) -> list:
        """List available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            models = response.json().get("models", [])
            return [m["name"] for m in models]
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
