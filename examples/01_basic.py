"""Example 1: Simple agent with PostgreSQL database."""

import asyncio
import os
from agent_framework import Agent, Signal
from agent_framework.database import get_database


class ValueAgent(Agent):
    """Simple value investing agent using PE ratio."""
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze based on PE ratio threshold."""
        pe = data.get('pe_ratio', 0)
        
        if pe < 15:
            return Signal(
                direction='bullish',
                confidence=0.8,
                reasoning=f"PE ratio {pe:.1f} indicates undervaluation"
            )
        elif pe > 30:
            return Signal(
                direction='bearish',
                confidence=0.7,
                reasoning=f"PE ratio {pe:.1f} indicates overvaluation"
            )
        else:
            return Signal(
                direction='neutral',
                confidence=0.6,
                reasoning=f"PE ratio {pe:.1f} is fairly valued"
            )


class GrowthAgent(Agent):
    """Growth investing agent using revenue growth."""
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze based on revenue growth."""
        growth = data.get('revenue_growth', 0)
        margin = data.get('profit_margin', 0)
        
        if growth > 20 and margin > 15:
            return Signal(
                direction='bullish',
                confidence=0.9,
                reasoning=f"Strong growth ({growth:.1f}%) with healthy margins ({margin:.1f}%)"
            )
        elif growth < 5:
            return Signal(
                direction='bearish',
                confidence=0.6,
                reasoning=f"Low growth rate ({growth:.1f}%)"
            )
        else:
            return Signal(
                direction='neutral',
                confidence=0.5,
                reasoning=f"Moderate growth ({growth:.1f}%)"
            )


async def main():
    """Run example agents on PostgreSQL data."""
    print("=" * 60)
    print("AI Agent Framework - Basic Example")
    print("=" * 60)
    
    # Connect to database
    connection_string = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:postgres@localhost:5432/agent_framework'
    )
    
    print("\n🔌 Connecting to database...")
    db = get_database(connection_string)
    await db.connect()
    print("✅ Connected!")
    
    # Create agents
    value_agent = ValueAgent()
    growth_agent = GrowthAgent()
    
    try:
        # Analyze all tickers
        tickers = await db.list_tickers()
        
        for ticker in tickers:
            print(f"\n📊 Analyzing {ticker}")
            print("-" * 60)
            
            # Get data
            data = await db.get_fundamentals(ticker)
            print(f"Company: {data['name']}")
            print(f"PE Ratio: {data['pe_ratio']:.1f}")
            print(f"Revenue Growth: {data['revenue_growth']:.1f}%")
            print(f"Profit Margin: {data['profit_margin']:.1f}%")
            
            # Value agent analysis
            value_signal = value_agent.analyze(ticker, data)
            print(f"\n💡 Value Agent:")
            print(f"   Direction: {value_signal.direction.upper()}")
            print(f"   Confidence: {value_signal.confidence:.1%}")
            print(f"   Reasoning: {value_signal.reasoning}")
            
            # Growth agent analysis
            growth_signal = growth_agent.analyze(ticker, data)
            print(f"\n🚀 Growth Agent:")
            print(f"   Direction: {growth_signal.direction.upper()}")
            print(f"   Confidence: {growth_signal.confidence:.1%}")
            print(f"   Reasoning: {growth_signal.reasoning}")
        
        print("\n" + "=" * 60)
        print("✅ Example completed successfully!")
        print("=" * 60)
        
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())