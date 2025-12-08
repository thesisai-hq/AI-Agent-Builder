"""Centralized LLM error handling and solution generation.

Extracts error parsing and solution logic from multiple locations into
a single source of truth.
"""

import re
from typing import Dict, Optional


class LLMErrorHandler:
    """Handles LLM-related errors with user-friendly messages and solutions."""

    @staticmethod
    def detect_llm_fallback(signal) -> bool:
        """Detect if signal is from LLM fallback (error occurred).

        Args:
            signal: Signal object with reasoning

        Returns:
            True if this is a fallback signal
        """
        reasoning = signal.reasoning.lower()

        fallback_indicators = [
            "llm unavailable",
            "llm error",
            "llm service unavailable",
            "using fallback",
            "no module named",
            "connection refused",
            "connection failed",
            "api error",
            "rate limit",
            "authentication",
            "api key",
            "model not found",
            "not downloaded",
        ]

        return any(indicator in reasoning for indicator in fallback_indicators)

    @staticmethod
    def parse_error(reasoning: str) -> Dict:
        """Parse LLM error reasoning to extract useful information.

        Args:
            reasoning: Signal reasoning string or error message

        Returns:
            Dict with error_type, provider, model, install_command, description
        """
        reasoning_lower = reasoning.lower()

        error_info = {
            "error_type": "unknown",
            "provider": None,
            "model": None,
            "install_command": None,
            "description": "",
        }

        # Module not found errors
        if "no module named 'ollama'" in reasoning_lower or "import ollama" in reasoning_lower:
            error_info.update(
                {
                    "error_type": "missing_package",
                    "provider": "ollama",
                    "install_command": "pip install ollama",
                    "description": "Ollama Python package not installed",
                }
            )
        elif "no module named 'openai'" in reasoning_lower or "import openai" in reasoning_lower:
            error_info.update(
                {
                    "error_type": "missing_package",
                    "provider": "openai",
                    "install_command": "pip install openai",
                    "description": "OpenAI Python package not installed",
                }
            )
        elif (
            "no module named 'anthropic'" in reasoning_lower
            or "import anthropic" in reasoning_lower
        ):
            error_info.update(
                {
                    "error_type": "missing_package",
                    "provider": "anthropic",
                    "install_command": "pip install anthropic",
                    "description": "Anthropic Python package not installed",
                }
            )

        # Connection errors (Ollama not running)
        elif "connection refused" in reasoning_lower or "connect" in reasoning_lower:
            error_info.update(
                {
                    "error_type": "connection_error",
                    "provider": "ollama",
                    "install_command": None,
                    "description": "Ollama service not running. Start with: ollama serve",
                }
            )

        # Model not found (need to pull)
        elif "model" in reasoning_lower and (
            "not found" in reasoning_lower or "not downloaded" in reasoning_lower
        ):
            # Try to extract model name from reasoning
            model_match = re.search(r"model[\s'\"]*([a-z0-9\.:_-]+)", reasoning_lower)
            model_name = model_match.group(1) if model_match else "llama3.2"

            error_info.update(
                {
                    "error_type": "model_not_found",
                    "provider": "ollama",
                    "model": model_name,
                    "install_command": f"ollama pull {model_name}",
                    "description": f"Model '{model_name}' not downloaded in Ollama",
                }
            )

        # API key errors
        elif "api key" in reasoning_lower or "authentication" in reasoning_lower:
            if "openai" in reasoning_lower:
                provider = "openai"
                env_var = "OPENAI_API_KEY"
            elif "anthropic" in reasoning_lower:
                provider = "anthropic"
                env_var = "ANTHROPIC_API_KEY"
            else:
                provider = "unknown"
                env_var = "API_KEY"

            error_info.update(
                {
                    "error_type": "missing_api_key",
                    "provider": provider,
                    "install_command": None,
                    "description": f"API key not configured. Set {env_var} in .env file",
                }
            )

        # Rate limit errors
        elif "rate limit" in reasoning_lower:
            error_info.update(
                {
                    "error_type": "rate_limit",
                    "provider": None,
                    "install_command": None,
                    "description": "API rate limit exceeded. Wait a few minutes and try again.",
                }
            )

        # Timeout errors
        elif "timeout" in reasoning_lower or "timed out" in reasoning_lower:
            error_info.update(
                {
                    "error_type": "timeout",
                    "provider": None,
                    "install_command": None,
                    "description": "Request timed out. Service may be slow or unavailable.",
                }
            )

        # Generic LLM error
        else:
            error_info.update(
                {
                    "error_type": "llm_error",
                    "provider": None,
                    "install_command": None,
                    "description": "LLM service encountered an error",
                }
            )

        return error_info

    @staticmethod
    def get_solution_text(error_info: Dict) -> str:
        """Get user-friendly solution text for Streamlit display.

        Args:
            error_info: Error info dict from parse_error()

        Returns:
            Formatted solution text for st.error() or st.info()
        """
        error_type = error_info.get("error_type")

        if error_type == "missing_package":
            provider = error_info.get("provider", "unknown")
            install_cmd = error_info.get("install_command", "pip install <package>")

            return f"""❌ **Missing LLM Package**

**Problem:** {error_info.get("description")}

**Solution:** Install the required package:
```bash
{install_cmd}
```

Or install all LLM providers:
```bash
pip install 'ai-agent-framework[llm]'
```

Then restart the GUI."""

        elif error_type == "model_not_found":
            model_name = error_info.get("model", "llama3.2")
            install_cmd = error_info.get("install_command", f"ollama pull {model_name}")

            return f"""❌ **Model Not Available**

**Problem:** Model '{model_name}' not downloaded

**Solution:** Download the model with Ollama:
```bash
{install_cmd}
```

**Available Models:** Check with `ollama list`

**Popular Models:**
- `ollama pull llama3.2` (recommended)
- `ollama pull mistral`
- `ollama pull phi`"""

        elif error_type == "connection_error":
            return """❌ **Ollama Service Not Running**

**Problem:** Can't connect to Ollama service

**Solution:** Start Ollama in a terminal:
```bash
ollama serve
```

Or if Ollama is not installed:
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Download a model
ollama pull llama3.2

# Start service
ollama serve
```

Keep the terminal open while using the GUI."""

        elif error_type == "missing_api_key":
            provider = error_info.get("provider", "unknown")
            env_var = f"{provider.upper()}_API_KEY" if provider != "unknown" else "API_KEY"

            return f"""❌ **API Key Not Configured**

**Problem:** {error_info.get("description")}

**Solution:** Add your API key to the `.env` file:
```bash
# Edit .env file
nano .env

# Add this line:
{env_var}=your-api-key-here
```

**Get an API Key:**
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/

Then restart the GUI."""

        elif error_type == "rate_limit":
            return """❌ **Rate Limit Exceeded**

**Problem:** Too many API requests

**Solution:**
- Wait 1-2 minutes and try again
- Or use Ollama (free, no rate limits)
- Or upgrade your API plan"""

        elif error_type == "timeout":
            return """⚠️ **Request Timed Out**

**Problem:** Service took too long to respond

**Solution:**
- Try again (service may be slow)
- If using Ollama, check if `ollama serve` is running
- For API providers, check your internet connection"""

        else:
            return f"""❌ **LLM Error**

**Problem:** {error_info.get("description", "LLM service encountered an error")}

**Solutions to try:**
1. Check if LLM service is running (for Ollama: `ollama serve`)
2. Verify API keys are set in `.env` file
3. Check internet connection
4. Try a different LLM provider"""
