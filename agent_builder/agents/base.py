"""Base agent classes"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable


@dataclass
class AgentSignal:
    ticker: str
    signal_type: str
    confidence: float
    reasoning: str
    agent_name: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        return {
            "ticker": self.ticker,
            "signal_type": self.signal_type,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "agent_name": self.agent_name,
            "timestamp": self.timestamp.isoformat(),
        }


class BaseAgent(ABC):
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
    
    @abstractmethod
    def analyze(self, ticker: str, context) -> AgentSignal:
        pass


class SimpleAgent(BaseAgent):
    def __init__(self, name: str, func: Callable, description: str = ""):
        super().__init__(name, description)
        self.func = func
    
    def analyze(self, ticker: str, context) -> AgentSignal:
        result = self.func(ticker, context)
        if isinstance(result, tuple) and len(result) >= 2:
            signal_type, confidence = result[0], result[1]
            reasoning = result[2] if len(result) > 2 else f"{self.name} analysis"
        else:
            signal_type, confidence, reasoning = result, 0.6, f"{self.name} analysis"
        return AgentSignal(ticker, signal_type, confidence, reasoning, self.name)


def agent(name: str, description: str = ""):
    def decorator(func):
        agent_instance = SimpleAgent(name, func, description)
        func.agent = agent_instance
        return func
    return decorator
