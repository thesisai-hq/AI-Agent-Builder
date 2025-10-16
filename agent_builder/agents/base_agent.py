from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any


class AgentSignal:
    def __init__(self, ticker: str, signal_type: str, confidence: float, 
                 reasoning: str, agent_name: str):
        self.ticker = ticker
        self.signal_type = signal_type
        self.confidence = confidence
        self.reasoning = reasoning
        self.agent_name = agent_name
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "ticker": self.ticker,
            "signal_type": self.signal_type,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "agent_name": self.agent_name,
            "timestamp": self.timestamp.isoformat()
        }


class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def analyze(self, ticker: str, **kwargs) -> AgentSignal:
        pass
