"""Peter Lynch GARP Strategy

Growth at Reasonable Price - find growth companies trading at fair valuations.

Strategy:
- Rule 1: PEG < 1.0 AND Growth > 15% AND Margin > 10% → Strong Bullish
- Rule 2: Growth > 25% AND PE < 30 → Moderate Bullish

PEG Ratio = PE / Growth Rate (< 1.0 means undervalued growth)
"""

import asyncio
from agent_framework import Agent, Signal, Database, Config


class LynchGARPAgent(Agent):
    """Peter Lynch GARP: Growth at reasonable price with PEG ratio focus"""
    
    async def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze using advanced multi-condition rules.
        
        Args:
            ticker: Stock ticker symbol
            data: Financial data dictionary
            
        Returns:
            Signal with direction, confidence, and reasoning
        """
        # Extract all metrics
        pe_ratio = data.get('pe_ratio', 0)
        revenue_growth = data.get('revenue_growth', 0)
        profit_margin = data.get('profit_margin', 0)
        
        # Calculate PEG ratio
        peg_ratio = pe_ratio / max(revenue_growth, 0.1) if revenue_growth > 0.1 else 999
        
        # Rule 1: Ideal GARP (PEG < 1.0 AND Growth > 15% AND Margin > 10%)
        if (peg_ratio < 1.0) and (revenue_growth > 15) and (profit_margin > 10):
            return Signal(
                direction='bullish',
                confidence=0.9,
                reasoning=f"Excellent GARP: PEG={peg_ratio:.2f}, Growth={revenue_growth:.1f}%, Margin={profit_margin:.1f}%"
            )
        
        # Rule 2: High growth at reasonable price (Growth > 25% AND PE < 30)
        if (revenue_growth > 25) and (pe_ratio < 30):
            return Signal(
                direction='bullish',
                confidence=0.75,
                reasoning=f"Strong growth at fair price: Growth={revenue_growth:.1f}%, PE={pe_ratio:.1f}"
            )
        
        # Default fallback
        return Signal(
            direction='neutral',
            confidence=0.5,
            reasoning=f"No GARP criteria met. PEG={peg_ratio:.2f}, Growth={revenue_growth:.1f}%"
        )


async def main():
    """Example usage."""
    print(f"{'-' * 60}")
    print(f"LynchGARPAgent - Advanced Rules")
    print(f"{'-' * 60}\n")
    
    db = Database(Config.get_database_url())
    await db.connect()
    
    try:
        agent = LynchGARPAgent()
        
        for ticker in ['AAPL', 'MSFT', 'GOOGL']:
            data = await db.get_fundamentals(ticker)
            
            if not data:
                print(f"⚠️  No data for {ticker}")
                continue
            
            signal = await agent.analyze(ticker, data)
            print(f"📊 {ticker}: {signal.direction.upper()} ({signal.confidence:.0%})")
            print(f"   {signal.reasoning}\n")
    
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
