from typing import Callable
from agent_builder.agents.base_agent import BaseAgent, AgentSignal
from agent_builder.agents.context import AgentContext


class SimpleAgent(BaseAgent):
    """Wrapper for decorator-based agents"""

    def __init__(self, name: str, func: Callable, weight: float = 0.1):
        super().__init__(name)
        self.func = func
        self.weight = weight

    def analyze(self, ticker: str, **kwargs) -> AgentSignal:
        """Execute the agent function"""
        # Create proper AgentContext
        context = AgentContext(ticker)

        # Call user function with context
        result = self.func(ticker, context)

        # Parse result
        if isinstance(result, tuple) and len(result) == 2:
            signal_type, confidence = result
        else:
            signal_type = result
            confidence = 0.6

        return AgentSignal(
            ticker=ticker,
            signal_type=signal_type,
            confidence=confidence,
            reasoning=f"{self.name} analysis",
            agent_name=self.name,
        )


def simple_agent(name: str, weight: float = 0.1):
    """
    Decorator to create simple agents

    Usage:
        @simple_agent("My Agent")
        def my_agent(ticker, context):
            pe = context.get_metric('pe_ratio')
            return "bullish", 0.8
    """

    def decorator(func):
        agent = SimpleAgent(name, func, weight)
        func.agent = agent
        func.analyze = agent.analyze
        return func

    return decorator
