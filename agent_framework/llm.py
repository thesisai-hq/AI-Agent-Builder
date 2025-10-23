"""LLM client with error handling, retries, and system prompts."""

from typing import Optional, List
import time
import logging

from .models import LLMConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMError(Exception):
    """Base exception for LLM errors."""
    pass


class APIError(LLMError):
    """API communication error."""
    pass


class RateLimitError(LLMError):
    """Rate limit exceeded."""
    pass


class LLMClient:
    """Unified LLM client with error handling and system prompt support.
    
    Features:
    - Supports OpenAI, Anthropic, Ollama
    - Automatic retries with exponential backoff
    - System prompts for agent personas
    - Comprehensive error handling
    - Timeout management
    
    Example:
        config = LLMConfig(provider='ollama', model='llama3.2')
        client = LLMClient(config)
        response = client.chat("Analyze AAPL stock")
    """
    
    def __init__(self, config: LLMConfig):
        """Initialize LLM client.
        
        Args:
            config: LLM configuration including system_prompt for persona
        """
        self.config = config
        self._client = None
    
    def _get_client(self):
        """Lazy initialize provider-specific client.
        
        Returns:
            Provider client
            
        Raises:
            LLMError: If provider initialization fails
        """
        if self._client is not None:
            return self._client
        
        try:
            if self.config.provider == 'openai':
                import openai
                self._client = openai.OpenAI(
                    api_key=self.config.api_key,
                    timeout=self.config.timeout
                )
            elif self.config.provider == 'anthropic':
                import anthropic
                self._client = anthropic.Anthropic(
                    api_key=self.config.api_key,
                    timeout=self.config.timeout
                )
            elif self.config.provider == 'ollama':
                import ollama
                self._client = ollama.Client(
                    host=self.config.base_url or 'http://localhost:11434'
                )
            else:
                raise LLMError(f"Unknown provider: {self.config.provider}")
            
            logger.info(f"Initialized {self.config.provider} client")
            return self._client
        except Exception as e:
            logger.error(f"Failed to initialize {self.config.provider} client: {e}")
            raise LLMError(f"Could not initialize {self.config.provider}") from e
    
    def chat(self, message: str, context: Optional[str] = None) -> str:
        """Send chat message with optional context and retries.
        
        Args:
            message: User message
            context: Additional context (e.g., from RAG)
            
        Returns:
            LLM response text
            
        Raises:
            LLMError: If all retries fail
            RateLimitError: If rate limit exceeded
        """
        client = self._get_client()
        
        # Build messages with system prompt (persona) if provided
        messages = []
        
        # Add context if provided
        if context:
            full_message = f"Context:\n{context}\n\nQuestion: {message}"
        else:
            full_message = message
        
        messages.append({
            "role": "user",
            "content": full_message
        })
        
        # Retry logic with exponential backoff
        last_error = None
        for attempt in range(self.config.max_retries):
            try:
                if self.config.provider == 'openai':
                    return self._chat_openai(client, messages)
                elif self.config.provider == 'anthropic':
                    return self._chat_anthropic(client, messages)
                elif self.config.provider == 'ollama':
                    return self._chat_ollama(client, messages)
            
            except Exception as e:
                last_error = e
                logger.warning(f"Attempt {attempt + 1}/{self.config.max_retries} failed: {e}")
                
                # Don't retry on rate limits immediately
                if "rate_limit" in str(e).lower():
                    if attempt < self.config.max_retries - 1:
                        wait_time = 2 ** (attempt + 2)  # 4, 8, 16 seconds
                        logger.info(f"Rate limited, waiting {wait_time}s")
                        time.sleep(wait_time)
                    else:
                        raise RateLimitError("Rate limit exceeded") from e
                # Exponential backoff for other errors
                elif attempt < self.config.max_retries - 1:
                    wait_time = 2 ** attempt  # 1, 2, 4 seconds
                    time.sleep(wait_time)
        
        # All retries failed
        logger.error(f"All {self.config.max_retries} attempts failed")
        raise APIError(f"Failed after {self.config.max_retries} attempts: {last_error}") from last_error
    
    def _chat_openai(self, client, messages: List[dict]) -> str:
        """OpenAI-specific chat implementation.
        
        Args:
            client: OpenAI client
            messages: Chat messages
            
        Returns:
            Response text
        """
        # Add system message if provided
        if self.config.system_prompt:
            messages = [
                {"role": "system", "content": self.config.system_prompt}
            ] + messages
        
        response = client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        return response.choices[0].message.content
    
    def _chat_anthropic(self, client, messages: List[dict]) -> str:
        """Anthropic-specific chat implementation.
        
        Args:
            client: Anthropic client
            messages: Chat messages
            
        Returns:
            Response text
        """
        response = client.messages.create(
            model=self.config.model,
            system=self.config.system_prompt or "",  # System prompt as persona
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        return response.content[0].text
    
    def _chat_ollama(self, client, messages: List[dict]) -> str:
        """Ollama-specific chat implementation.
        
        Args:
            client: Ollama client
            messages: Chat messages
            
        Returns:
            Response text
        """
        # Add system message if provided
        if self.config.system_prompt:
            messages = [
                {"role": "system", "content": self.config.system_prompt}
            ] + messages
        
        response = client.chat(
            model=self.config.model,
            messages=messages
        )
        return response['message']['content']
    
    def embed(self, text: str) -> List[float]:
        """Generate embedding for text (for RAG).
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
            
        Raises:
            LLMError: If embedding generation fails
        """
        client = self._get_client()
        
        try:
            if self.config.provider == 'openai':
                response = client.embeddings.create(
                    input=text,
                    model="text-embedding-ada-002"
                )
                return response.data[0].embedding
            
            elif self.config.provider == 'ollama':
                response = client.embeddings(
                    model=self.config.model,
                    prompt=text
                )
                return response['embedding']
            
            else:
                raise LLMError(f"Embeddings not supported for {self.config.provider}")
        
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            raise LLMError(f"Could not generate embedding: {e}") from e
