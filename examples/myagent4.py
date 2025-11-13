"""Auto-generated hybrid agent: MyAgent4



Uses rule-based logic for clear signals, LLM for complex analysis.

DEPENDENCIES:
This agent requires LLM dependencies. Install with:
  pip install 'ai-agent-framework[llm]'

Or install specific provider:
  pip install ollama

To check which providers are installed:
  python3 gui/check_llm_deps.py
"""

import asyncio
from agent_framework import (
    Agent, Signal, AgentConfig, LLMConfig,
    Database, Config, parse_llm_signal, format_fundamentals
)


class MyAgent4(Agent):
    """"""
    
    def __init__(self):
        """Initialize agent with LLM configuration."""
        config = AgentConfig(
            name="MyAgent4",
            description="",
            llm=LLMConfig(
                provider='ollama',
                model='llama3.2',
                temperature=0.5,
                max_tokens=1000,
                system_prompt="""You are a financial analyst."""
            )
        )
        super().__init__(config)
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        """Hybrid analysis: rules first, then LLM for complex cases.
        
        Args:
            ticker: Stock ticker symbol
            data: Financial data dictionary
            
        Returns:
            Signal with direction, confidence, and reasoning
        """
        # Check if any rule-based conditions are met
        if data.get('pe_ratio', 0) < 0.0 or data.get('pe_ratio', 0) < 0.0:
            # Use LLM for detailed analysis
            return self._llm_analysis(ticker, data)
        
        # Default neutral signal
        return Signal(
            direction='neutral',
            confidence=0.5,
            reasoning='No significant indicators, holding neutral stance'
        )
    
    def _llm_analysis(self, ticker: str, data: dict) -> Signal:
        """Perform LLM-based analysis."""
        fundamentals_text = format_fundamentals(data)
        
        prompt = f"""Analyze {ticker}:

{fundamentals_text}

Provide detailed reasoning for your recommendation.
Format: DIRECTION|CONFIDENCE|REASONING"""
        
        try:
            response = self.llm.chat(prompt)
            return parse_llm_signal(response, f"Hybrid analysis of {ticker}")
        except Exception as e:
            print(f"⚠️  LLM error: {e}")
            return Signal(
                direction='neutral',
                confidence=0.5,
                reasoning=f'LLM error: {str(e)[:100]}'
            )


async def main():
    """Example usage of the hybrid agent."""
    print(f"{'-' * 60}")
    print(f"MyAgent4 - Hybrid Analysis")
    print(f"{'-' * 60}\n")
    
    db = Database(Config.get_database_url())
    await db.connect()
    
    try:
        agent = MyAgent4()
        
        for ticker in ['AAPL', 'MSFT']:
            data = await db.get_fundamentals(ticker)
            
            if not data:
                print(f"⚠️  No data for {ticker}")
                continue
            
            print(f"📊 {ticker}")
            signal = agent.analyze(ticker, data)
            print(f"{signal.direction.upper()} ({signal.confidence:.0%})")
            print(f"{signal.reasoning}\n")
    
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
