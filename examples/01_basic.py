"""Example 1: Basic Rule-Based Agent

This example demonstrates the simplest form of investment agent:
- Pure rule-based logic (no AI, no LLM)
- Fast execution (milliseconds)
- Deterministic (same input = same output)
- No dependencies beyond core framework
- Uses async analyze() for consistency with framework

Learning Focus:
- Understanding the Agent base class
- Working with financial data from PostgreSQL
- Creating simple if/then investment rules
- Returning Signal objects
- Using async/await pattern (even for simple logic)

⚠️ DISCLAIMER: This is educational code for learning purposes only.
Do NOT use for real trading. Not financial advice. See DISCLAIMER.md for full terms.
"""

import asyncio
from agent_framework import Agent, Signal, Database, Config


class ValueAgent(Agent):
    """Simple value investing agent using PE ratio.
    
    Strategy: Buy when stocks are cheap relative to earnings (PE < 15)
    
    This demonstrates:
    - Basic rule-based logic
    - Simple thresholds
    - Clear reasoning
    - Async function (no await needed for simple logic)
    """
    
    async def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze based on PE ratio threshold.
        
        Investment Logic:
        - PE < 15: Undervalued → Bullish
        - PE > 30: Overvalued → Bearish
        - PE 15-30: Fair value → Neutral
        
        Args:
            ticker: Stock ticker symbol
            data: Financial data dictionary
            
        Returns:
            Signal with direction, confidence, and reasoning
            
        Note:
            This is async but doesn't use await (simple logic).
            Async is for API consistency - no performance penalty.
        """
        pe = data.get('pe_ratio', 0)
        
        if pe < 15:
            return Signal(
                direction='bullish',
                confidence=0.8,
                reasoning=f"PE ratio {pe:.1f} indicates undervaluation (value threshold: <15)"
            )
        elif pe > 30:
            return Signal(
                direction='bearish',
                confidence=0.7,
                reasoning=f"PE ratio {pe:.1f} indicates overvaluation (overvalued threshold: >30)"
            )
        else:
            return Signal(
                direction='neutral',
                confidence=0.6,
                reasoning=f"PE ratio {pe:.1f} is fairly valued (between 15-30)"
            )


async def main():
    """Example usage of rule-based agent."""
    print("=" * 60)
    print("Example 1: Basic Rule-Based Agent")
    print("=" * 60)
    print("\n📚 Learning: Simple if/then rules, no AI needed")
    print("⚡ Speed: Very fast (milliseconds)")
    print("💰 Cost: Free (no LLM calls)")
    print("🔄 Async: Uses async for consistency (no overhead)")
    
    # Connect to database
    connection_string = Config.get_database_url()
    
    print("\n📌 Connecting to database...")
    db = Database(connection_string)
    
    try:
        await db.connect()
        print("✅ Connected!")
        
        # Create agent
        agent = ValueAgent()
        print(f"\n🤖 Agent: {agent.config.name}")
        print(f"📝 Strategy: {agent.__doc__.split('Strategy:')[1].split('This')[0].strip()}")
        
        # Analyze all tickers
        tickers = await db.list_tickers()
        print(f"\n📊 Analyzing {len(tickers)} stocks: {', '.join(tickers)}")
        
        for ticker in tickers:
            print(f"\n{'─'*60}")
            
            # Get data
            data = await db.get_fundamentals(ticker)
            if not data:
                print(f"⚠️  No data available for {ticker}")
                continue
            
            # Show company info
            print(f"📈 {ticker} - {data['name']}")
            print(f"   PE Ratio: {data['pe_ratio']:.1f}")
            print(f"   Sector: {data['sector']}")
            
            # Run analysis (async)
            signal = await agent.analyze(ticker, data)
            
            # Display result
            emoji = {'bullish': '🟢', 'bearish': '🔴', 'neutral': '🟡'}[signal.direction]
            print(f"\n   {emoji} {signal.direction.upper()} ({signal.confidence:.0%})")
            print(f"   {signal.reasoning}")
        
        print("\n" + "=" * 60)
        print("✅ Example completed successfully!")
        print("\n💡 Key Takeaways:")
        print("   • Rule-based agents are fast and deterministic")
        print("   • Perfect for clear investment criteria")
        print("   • No LLM dependencies needed")
        print("   • Async design allows parallel execution in orchestrators")
        print("   • Great foundation for understanding the framework")
        print("\n📖 Next: Try 02_llm_agent.py for AI-powered analysis")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
