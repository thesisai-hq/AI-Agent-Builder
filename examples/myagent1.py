"""Auto-generated agent: MyAgent1



Strategy: Simple rule-based conditions
"""

import asyncio
from agent_framework import Agent, Signal, Database, Config


class MyAgent1(Agent):
    """"""
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze based on defined rules.
        
        Args:
            ticker: Stock ticker symbol
            data: Financial data dictionary
            
        Returns:
            Signal with direction, confidence, and reasoning
        """
        # Extract metrics
        pe_ratio = data.get('pe_ratio', 0)
        
        # Apply rules
        if data.get('pe_ratio', 0) < 0.0:
            return Signal(
                direction='bullish',
                confidence=0.7,
                reasoning=f"Pe Ratio {pe_ratio:.1f} is bullish"
            )
        if data.get('pe_ratio', 0) < 0.0:
            return Signal(
                direction='bullish',
                confidence=0.7,
                reasoning=f"Pe Ratio {pe_ratio:.1f} is bullish"
            )
        
        # Default fallback
        return Signal(
            direction='neutral',
            confidence=0.5,
            reasoning='No rules matched'
        )


async def main():
    """Example usage."""
    print(f"{'-' * 60}")
    print(f"MyAgent1 - Example Usage")
    print(f"{'-' * 60}\n")
    
    db = Database(Config.get_database_url())
    await db.connect()
    
    try:
        agent = MyAgent1()
        
        for ticker in ['AAPL', 'MSFT', 'GOOGL']:
            data = await db.get_fundamentals(ticker)
            
            if not data:
                print(f"⚠️  No data for {ticker}")
                continue
            
            signal = agent.analyze(ticker, data)
            print(f"📊 {ticker}: {signal.direction.upper()} ({signal.confidence:.0%})")
            print(f"   {signal.reasoning}\n")
    
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
