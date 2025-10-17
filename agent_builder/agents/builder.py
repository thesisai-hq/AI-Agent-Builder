"""
Agent Builder - REFACTORED for efficiency
"""

from typing import Callable, Optional, Tuple, Union, Dict, Any
from agent_builder.agents.base_agent import BaseAgent, AgentSignal
from agent_builder.agents.context import AgentContext
import logging

logger = logging.getLogger(__name__)


class SimpleAgent(BaseAgent):
    """
    Wrapper for decorator-based agents - IMPROVED

    Changes from original:
    - Context passed from outside (enables shared caching)
    - Better result parsing with validation
    - Support for 3-tuple return (signal, confidence, reasoning)
    - Error tracking for monitoring
    - Optional detailed reasoning
    """

    def __init__(
        self,
        name: str,
        func: Callable,
        weight: float = 0.1,
        enabled: bool = True,
        tags: Optional[list] = None,
    ):
        super().__init__(name, weight, enabled, tags)
        self.func = func

        # Statistics tracking
        self._call_count = 0
        self._error_count = 0
        self._last_error = None

    def analyze(self, ticker: str, context: AgentContext) -> AgentSignal:
        """
        Execute the agent function - IMPROVED

        Changes:
        - Context passed in (not created here) - CRITICAL FOR PERFORMANCE
        - Better error handling with fallback
        - Validation of return values
        - Statistics tracking

        Args:
            ticker: Stock ticker
            context: Shared AgentContext (with cache)

        Returns:
            AgentSignal with validated values
        """
        try:
            self._call_count += 1

            # Call user function with shared context
            result = self.func(ticker, context)

            # Parse and validate result
            signal_type, confidence, reasoning = self._parse_result(result)

            # Create signal with metadata
            return AgentSignal(
                signal_type=signal_type,
                confidence=confidence,
                reasoning=reasoning or f"{self.name} analysis",
                metadata={
                    "agent_name": self.name,
                    "agent_weight": self.weight,
                    "agent_tags": self.tags,
                    "call_count": self._call_count,
                },
            )

        except Exception as e:
            self._error_count += 1
            self._last_error = str(e)

            logger.error(f"Agent '{self.name}' failed on {ticker}: {e}", exc_info=True)

            # Return safe neutral signal on error
            return AgentSignal(
                signal_type="neutral",
                confidence=0.5,
                reasoning=f"Agent error: {str(e)[:100]}",
                metadata={
                    "agent_name": self.name,
                    "agent_weight": self.weight,
                    "error": True,
                    "error_message": str(e),
                },
            )

    def _parse_result(
        self, result: Union[str, Tuple]
    ) -> Tuple[str, float, Optional[str]]:
        """
        Parse agent function return value with validation

        Supported formats:
        1. "bullish" → ("bullish", 0.6, None)
        2. ("bullish", 0.8) → ("bullish", 0.8, None)
        3. ("bullish", 0.8, "Low P/E") → ("bullish", 0.8, "Low P/E")

        Args:
            result: Agent function return value

        Returns:
            (signal_type, confidence, reasoning) tuple

        Raises:
            ValueError: If result format is invalid
        """
        # Format 1: Single string
        if isinstance(result, str):
            return result, 0.6, None

        # Format 2 & 3: Tuple
        if isinstance(result, tuple):
            if len(result) == 2:
                signal_type, confidence = result
                return signal_type, float(confidence), None

            elif len(result) == 3:
                signal_type, confidence, reasoning = result
                return signal_type, float(confidence), reasoning

            else:
                raise ValueError(
                    f"Invalid tuple length: {len(result)}. "
                    f"Expected 2 (signal, confidence) or 3 (signal, confidence, reasoning)"
                )

        # Invalid type
        raise ValueError(
            f"Invalid return type: {type(result).__name__}. "
            f"Expected str or tuple, got {result}"
        )

    def get_stats(self) -> Dict[str, Any]:
        """
        Get agent execution statistics

        Returns:
            Dict with call count, error count, error rate
        """
        return {
            "name": self.name,
            "calls": self._call_count,
            "errors": self._error_count,
            "error_rate": (
                round(self._error_count / self._call_count, 3)
                if self._call_count > 0
                else 0
            ),
            "last_error": self._last_error,
        }


def simple_agent(
    name: str, weight: float = 0.1, enabled: bool = True, tags: Optional[list] = None
):
    """
    Decorator to create simple agents - IMPROVED

    Changes:
    - Support for all BaseAgent parameters
    - Better documentation
    - Attached helper methods

    Usage:
        @simple_agent("My Agent", weight=0.15, tags=['fundamental', 'value'])
        def my_agent(ticker, context):
            pe = context.get_metric('pe_ratio')

            # Return options:
            return "bullish"                              # Simple
            return "bullish", 0.85                        # With confidence
            return "bullish", 0.85, "Low P/E at 15.2"   # With reasoning

    Args:
        name: Agent display name
        weight: Agent importance (0.0-1.0, default 0.1)
        enabled: Whether agent is active (default True)
        tags: List of tags for categorization

    Returns:
        Decorated function with .agent attribute
    """

    def decorator(func: Callable) -> Callable:
        # Create agent instance
        agent_instance = SimpleAgent(
            name=name, func=func, weight=weight, enabled=enabled, tags=tags
        )

        # Attach agent and methods to function
        func.agent = agent_instance
        func.analyze = agent_instance.analyze
        func.get_stats = agent_instance.get_stats
        func.get_metadata = agent_instance.get_metadata

        return func

    return decorator
