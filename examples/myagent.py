"""Auto-generated LLM-powered agent: MyAgent


"""

import asyncio
from agent_framework import (
    Agent, Signal, AgentConfig, LLMConfig,
    Database, Config, parse_llm_signal, format_fundamentals
)


class MyAgent(Agent):
    """"""
    
    def __init__(self):
        """Initialize agent with LLM configuration."""
        config = AgentConfig(
            name="MyAgent",
            description="",
            llm=LLMConfig(
                provider='ollama',
                temperature=0.5,
                max_tokens=1000,
                system_prompt="""you are fundamental analyst"""
            )
        )
        super().__init__(config)
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze using LLM with configured personality.
        
        Args:
            ticker: Stock ticker symbol
            data: Financial data dictionary
            
        Returns:
            Signal with direction, confidence, and reasoning
        """
        # Format fundamentals for LLM
        fundamentals_text = format_fundamentals(data)
        
        # Build prompt
        prompt = f"""Analyze {ticker} with the following data:

{fundamentals_text}

Provide your investment recommendation.
Format: DIRECTION|CONFIDENCE|REASONING
Example: bullish|75|Strong growth with healthy margins"""
        
        try:
            # Query LLM
            response = self.llm.chat(prompt)
            return parse_llm_signal(response, f"Analysis of {ticker}")
        
        except Exception as e:
            print(f"⚠️  LLM error: {e}")
            # Fallback to simple rule
            pe = data.get('pe_ratio', 0)
            if pe < 20:
                return Signal('neutral', 0.5, f'LLM unavailable, PE={pe:.1f}')
            return Signal('neutral', 0.5, 'LLM unavailable, insufficient data')


async def main():
    """Example usage of the LLM-powered agent."""
    print(f"{'-' * 60}")
    print(f"MyAgent - LLM-Powered Analysis")
    print(f"{'-' * 60}\n")
    
    # Connect to database
    db = Database(Config.get_database_url())
    await db.connect()
    
    try:
        # Create agent
        agent = MyAgent()
        
        # Analyze tickers
        for ticker in ['AAPL', 'TSLA']:
            data = await db.get_fundamentals(ticker)
            
            if not data:
                print(f"⚠️  No data for {ticker}")
                continue
            
            print(f"📊 Analyzing {ticker}...")
            signal = agent.analyze(ticker, data)
            
            print(f"{signal.direction.upper()} ({signal.confidence:.0%})")
            print(f"{signal.reasoning}\n")
    
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
