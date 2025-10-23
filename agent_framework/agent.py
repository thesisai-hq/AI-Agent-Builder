"""Base Agent class with lazy LLM/RAG initialization."""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from .models import Signal, AgentConfig


class Agent(ABC):
    """Base class for all agents.
    
    Design:
    - Lazy initialization: LLM/RAG only created when accessed
    - Optional complexity: Simple agents don't need LLM/RAG
    - System prompt support: Personas via config.llm.system_prompt
    """
    
    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize agent with optional configuration.
        
        Args:
            config: Agent configuration. If None, creates minimal config.
        """
        self.config = config or AgentConfig(
            name=self.__class__.__name__,
            description="Default agent"
        )
        self._llm = None
        self._rag = None
    
    @property
    def llm(self):
        """Lazy initialization of LLM client.
        
        Returns LLM instance only if config.llm is set.
        """
        if self._llm is None and self.config.llm:
            from .llm import LLMClient
            self._llm = LLMClient(self.config.llm)
        return self._llm
    
    @property
    def rag(self):
        """Lazy initialization of RAG system.
        
        Returns RAG instance only if config.rag is set.
        """
        if self._rag is None and self.config.rag:
            from .rag import RAGSystem
            self._rag = RAGSystem(self.config.rag)
        return self._rag
    
    @abstractmethod
    def analyze(self, ticker: str, data: Dict[str, Any]) -> Signal:
        """Analyze data and generate signal.
        
        Args:
            ticker: Stock ticker symbol
            data: Market/fundamental data dictionary
            
        Returns:
            Signal with direction, confidence, and reasoning
        """
        pass
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.config.name}>"