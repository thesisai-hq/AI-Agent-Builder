"""Centralized LLM error handling and solution generation.

Extracts error parsing and solution logic from multiple locations into
a single source of truth.
"""

import re
from typing import Dict


class LLMErrorHandler:
    """Handles LLM-related errors with user-friendly messages and solutions."""

    @staticmethod
    def detect_llm_fallback(signal) -> bool:
        """Detect if signal is from LLM fallback (error occurred).

        Args:
            signal: Signal object with reasoning

        Returns:
            True if this is a fallback signal indicating LLM failure
        """
        reasoning = signal.reasoning.lower()

        # These indicators suggest the LLM itself failed, not other systems
        fallback_indicators = [
            "llm unavailable",
            "llm error",
            "llm service unavailable",
            "using fallback",
            "no module named 'ollama'",
            "no module named 'openai'",
            "no module named 'anthropic'",
            "api error",
            "rate limit",
            "api key",
            "model not found",
            "model not downloaded",
            "ollama",  # Specific to Ollama errors
            "openai",  # Specific to OpenAI errors
            "anthropic",  # Specific to Anthropic errors
        ]

        return any(indicator in reasoning for indicator in fallback_indicators)

    @staticmethod
    def parse_error(reasoning: str) -> Dict:
        """Parse error reasoning to extract useful information.

        Distinguishes between:
        - LLM/Ollama connection errors
        - Database connection errors
        - Package import errors
        - API key errors
        - Other errors

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

        # =================================================================
        # 1. Module/Package not found errors
        # =================================================================
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

        # =================================================================
        # 2. Database connection errors (NOT LLM errors!)
        # =================================================================
        elif any(
            db_indicator in reasoning_lower
            for db_indicator in [
                "database",
                "postgresql",
                "postgres",
                "asyncpg",
                "psycopg",
                "db_host",
                "db_port",
                "fundamentals",  # Table name from our schema
                "thesis_data",  # Schema name
            ]
        ):
            error_info.update(
                {
                    "error_type": "database_error",
                    "provider": None,
                    "install_command": None,
                    "description": "Database connection error. Check PostgreSQL is running and credentials are correct.",
                }
            )

        # =================================================================
        # 3. Ollama-specific connection errors
        # =================================================================
        elif "ollama" in reasoning_lower and (
            "connection" in reasoning_lower or "refused" in reasoning_lower
        ):
            error_info.update(
                {
                    "error_type": "connection_error",
                    "provider": "ollama",
                    "install_command": None,
                    "description": "Ollama service not running. Start with: ollama serve",
                }
            )

        # =================================================================
        # 4. Generic connection errors on port 11434 (Ollama's default port)
        # =================================================================
        elif "11434" in reasoning_lower and "connection" in reasoning_lower:
            error_info.update(
                {
                    "error_type": "connection_error",
                    "provider": "ollama",
                    "install_command": None,
                    "description": "Ollama service not running. Start with: ollama serve",
                }
            )

        # =================================================================
        # 5. Model not found (need to pull)
        # =================================================================
        elif "model" in reasoning_lower and (
            "not found" in reasoning_lower or "not downloaded" in reasoning_lower
        ):
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

        # =================================================================
        # 6. API key errors
        # =================================================================
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

        # =================================================================
        # 7. Rate limit errors
        # =================================================================
        elif "rate limit" in reasoning_lower:
            error_info.update(
                {
                    "error_type": "rate_limit",
                    "provider": None,
                    "install_command": None,
                    "description": "API rate limit exceeded. Wait a few minutes and try again.",
                }
            )

        # =================================================================
        # 8. Timeout errors
        # =================================================================
        elif "timeout" in reasoning_lower or "timed out" in reasoning_lower:
            error_info.update(
                {
                    "error_type": "timeout",
                    "provider": None,
                    "install_command": None,
                    "description": "Request timed out. Service may be slow or unavailable.",
                }
            )

        # =================================================================
        # 9. Generic LLM errors (only if LLM-related keywords present)
        # =================================================================
        elif any(
            llm_keyword in reasoning_lower
            for llm_keyword in ["llm", "ollama", "openai", "anthropic", "gpt", "claude"]
        ):
            error_info.update(
                {
                    "error_type": "llm_error",
                    "provider": None,
                    "install_command": None,
                    "description": "LLM service encountered an error",
                }
            )

        # =================================================================
        # 10. Unknown errors - don't assume LLM
        # =================================================================
        else:
            error_info.update(
                {
                    "error_type": "unknown",
                    "provider": None,
                    "install_command": None,
                    "description": str(reasoning)[:200],  # First 200 chars of error
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

        elif error_type == "database_error":
            return """❌ **Database Connection Error**

**Problem:** Cannot connect to PostgreSQL database

**Solutions:**

1. **Check if PostgreSQL is running:**
```bash
# Docker
docker ps | grep postgres

# Or check service
systemctl status postgresql
```

2. **Start the database:**
```bash
# If using Docker
cd AI-Agent-Builder
docker-compose up -d

# Or start PostgreSQL service
systemctl start postgresql
```

3. **Verify connection settings in `.env`:**
```bash
DB_HOST=localhost
DB_PORT=5433
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=agent_framework
```

4. **Run database setup:**
```bash
python setup_test_db.py
```"""

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
            return """⚠️ **Rate Limit Exceeded**

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

        elif error_type == "llm_error":
            return f"""❌ **LLM Error**

**Problem:** {error_info.get("description", "LLM service encountered an error")}

**Solutions to try:**
1. Check if LLM service is running (for Ollama: `ollama serve`)
2. Verify API keys are set in `.env` file
3. Check internet connection
4. Try a different LLM provider"""

        else:
            # Unknown error - show the actual error message
            description = error_info.get("description", "Unknown error occurred")
            return f"""❌ **Error**

**Details:** {description}

**Troubleshooting:**
- Check that all dependencies are installed
- Verify database is running (for Rule-Based agents)
- Check LLM service is running (for LLM agents)
- Review the error message above for specific issues"""
