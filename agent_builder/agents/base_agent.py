"""
Agent Base Classes - REFACTORED for efficiency
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class AgentSignal:
    """
    Agent analysis signal - IMPROVED

    Changes from original:
    - Removed redundant ticker parameter
    - Removed redundant agent_name parameter (use metadata)
    - Added validation for signal_type and confidence
    - Added metadata dict for extensibility
    - Made reasoning optional with better defaults
    """

    # Valid signal types - prevents typos and invalid signals
    VALID_SIGNALS = frozenset(["bullish", "bearish", "neutral"])

    def __init__(
        self,
        signal_type: str,
        confidence: float,
        reasoning: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Create agent signal with validation

        Args:
            signal_type: "bullish", "bearish", or "neutral"
            confidence: 0.0 to 1.0 (0 = no confidence, 1 = certain)
            reasoning: Optional explanation for the signal
            metadata: Optional dict with agent_name, weight, tags, etc.

        Raises:
            ValueError: If signal_type or confidence is invalid
        """
        # Validate signal type
        if signal_type not in self.VALID_SIGNALS:
            raise ValueError(
                f"Invalid signal_type: '{signal_type}'. "
                f"Must be one of {list(self.VALID_SIGNALS)}"
            )

        # Validate confidence bounds
        if not 0.0 <= confidence <= 1.0:
            raise ValueError(
                f"Invalid confidence: {confidence}. " f"Must be between 0.0 and 1.0"
            )

        self.signal_type = signal_type
        self.confidence = confidence
        self.reasoning = reasoning
        self.metadata = metadata or {}
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "signal_type": self.signal_type,
            "confidence": round(self.confidence, 3),
            "reasoning": self.reasoning,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
        }

    def __repr__(self) -> str:
        return f"AgentSignal({self.signal_type}, {self.confidence:.2f})"


class BaseAgent(ABC):
    """
    Abstract base class for all agents - IMPROVED

    Changes from original:
    - Added weight, enabled, tags as core properties
    - Better interface definition
    - Added metadata method
    """

    def __init__(
        self,
        name: str,
        weight: float = 0.1,
        enabled: bool = True,
        tags: Optional[list] = None,
    ):
        """
        Initialize base agent

        Args:
            name: Agent display name
            weight: Agent importance (0.0-1.0, higher = more influence)
            enabled: Whether agent is active
            tags: List of tags for categorization
        """
        self.name = name
        self.weight = weight
        self.enabled = enabled
        self.tags = tags or []

        # Validate weight (warning only, not error)
        if not 0.0 <= weight <= 1.0:
            logger.warning(
                f"Agent '{name}' weight {weight} outside typical range [0.0, 1.0]"
            )

    @abstractmethod
    def analyze(self, ticker: str, context: "AgentContext") -> AgentSignal:
        """
        Analyze a stock and return signal

        Args:
            ticker: Stock ticker symbol (e.g., "AAPL")
            context: AgentContext for data access (shared across agents)

        Returns:
            AgentSignal with recommendation

        Note:
            Context is shared across all agents in an analysis.
            Use context caching for efficiency!
        """
        pass

    def get_metadata(self) -> Dict[str, Any]:
        """Get agent metadata for registry"""
        return {
            "name": self.name,
            "weight": self.weight,
            "enabled": self.enabled,
            "tags": self.tags,
            "type": self.__class__.__name__,
        }

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', weight={self.weight})"
