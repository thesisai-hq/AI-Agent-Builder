"""Base Agent class with lazy LLM/RAG initialization."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from .models import AgentConfig, Signal


class Agent(ABC):
    """Base class for all agents.

    Design:
    - All agents use async analyze() for consistency
    - Simple agents can use sync logic inside async function (no overhead)
    - RAG/LLM agents can use true async operations (parallel queries, async I/O)
    - Lazy initialization: LLM/RAG only created when accessed
    - System prompt support: Personas via config.llm.system_prompt

    Performance:
    - Async overhead for simple agents: ~0.001ms (negligible)
    - Async benefit for complex agents: 3-5x speedup (parallel operations)
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize agent with optional configuration.

        Args:
            config: Agent configuration. If None, creates minimal config.
        """
        self.config = config or AgentConfig(
            name=self.__class__.__name__, description="Default agent"
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
    async def analyze(self, ticker: str, data: Dict[str, Any]) -> Signal:
        """Analyze data and generate signal (async).

        Args:
            ticker: Stock ticker symbol
            data: Market/fundamental data dictionary or document text

        Returns:
            Signal with direction, confidence, and reasoning

        Note:
            This is async to support I/O operations like LLM API calls,
            database queries, and parallel processing. Simple agents can
            use synchronous logic inside the async function with no penalty.

        Example:
            # Simple agent (sync logic in async function)
            async def analyze(self, ticker, data):
                pe = data.get('pe_ratio', 0)
                if pe < 15:
                    return Signal('bullish', 0.8, 'Undervalued')
                return Signal('neutral', 0.5, 'Fair')

            # Complex agent (true async with parallel operations)
            async def analyze(self, ticker, data):
                insights = await asyncio.gather(
                    self._analyze_risks(),
                    self._analyze_performance()
                )
                return self._synthesize(insights)
        """
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.config.name}>"
