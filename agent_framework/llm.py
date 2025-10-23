"""LLM client supporting OpenAI, Anthropic, and Ollama with system prompts."""

from typing import Optional, List
from .models import LLMConfig


class LLMClient:
    """Unified LLM client with system prompt support for agent personas.
    
    Supports:
    - OpenAI (GPT-3.5, GPT-4)
    - Anthropic (Claude)
    - Ollama (local models)
    
    System prompts enable agent personas:
    - "You are a conservative value investor..."
    - "You are an aggressive growth trader..."
    """
    
    def __init__(self, config: LLMConfig):
        """Initialize LLM client.
        
        Args:
            config: LLM configuration including system_prompt for persona
        """
        self.config = config
        self._client = None
    
    def _get_client(self):
        """Lazy initialize provider-specific client."""
        if self._client is not None:
            return self._client
        
        try:
            if self.config.provider == 'openai':
                import openai
                self._client = openai.OpenAI(api_key=self.config.api_key)
            elif self.config.provider == 'anthropic':
                import anthropic
                self._client = anthropic.Anthropic(api_key=self.config.api_key)
            elif self.config.provider == 'ollama':
                import ollama
                self._client = ollama.Client(host=self.config.base_url or 'http://localhost:11434')
            else:
                raise ValueError(f"Unknown provider: {self.config.provider}")
        except ImportError as e:
            raise ImportError(
                f"Missing package for {self.config.provider}. Install with:\n"
                f"  pip install {self.config.provider}\n"
                f"Or install all LLM providers:\n"
                f"  pip install -e .[llm]"
            ) from e
        
        return self._client
    
    def chat(self, message: str, context: Optional[str] = None) -> str:
        """Send chat message with optional context.
        
        Args:
            message: User message
            context: Additional context (e.g., from RAG)
            
        Returns:
            LLM response text
        """
        client = self._get_client()
        
        # Build messages with system prompt (persona) if provided
        messages = []
        
        # Add system prompt for agent persona
        if self.config.system_prompt:
            if self.config.provider == 'openai':
                messages.append({
                    "role": "system",
                    "content": self.config.system_prompt
                })
            elif self.config.provider == 'anthropic':
                # Anthropic handles system separately
                pass
        
        # Add context if provided
        if context:
            messages.append({
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {message}"
            })
        else:
            messages.append({
                "role": "user",
                "content": message
            })
        
        # Call provider
        try:
            if self.config.provider == 'openai':
                response = client.chat.completions.create(
                    model=self.config.model,
                    messages=messages,
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens
                )
                return response.choices[0].message.content
            
            elif self.config.provider == 'anthropic':
                response = client.messages.create(
                    model=self.config.model,
                    system=self.config.system_prompt or "",
                    messages=messages,
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens
                )
                return response.content[0].text
            
            elif self.config.provider == 'ollama':
                response = client.chat(
                    model=self.config.model,
                    messages=messages
                )
                return response['message']['content']
        except Exception as e:
            raise RuntimeError(
                f"LLM call failed for {self.config.provider}/{self.config.model}: {e}"
            ) from e
    
    def embed(self, text: str) -> List[float]:
        """Generate embedding for text (for RAG).
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        client = self._get_client()
        
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
            raise NotImplementedError(f"Embeddings not supported for {self.config.provider}")