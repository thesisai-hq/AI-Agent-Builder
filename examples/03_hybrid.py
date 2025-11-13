"""Example 3: Hybrid Agent (Rules + LLM)

This example demonstrates the best of both worlds:
- Rules for fast screening (filter thousands of stocks)
- LLM for deep analysis (only on filtered candidates)
- Cost-effective (95% fewer LLM calls)
- Time-efficient (95% faster than pure LLM)

Learning Focus:
- Two-stage analysis (filter → analyze)
- Combining rule-based and AI approaches
- Resource optimization (speed + cost)
- When to use hybrid vs pure approaches

⚠️ DISCLAIMER: This is educational code for learning purposes only.
Do NOT use for real trading. Not financial advice. See DISCLAIMER.md for full terms.

DEPENDENCIES:
This example requires LLM dependencies. Install with:
  pip install 'ai-agent-framework[llm]'

Or install Ollama specifically:
  pip install ollama

Then download the model:
  ollama pull llama3.2
"""

import asyncio
from agent_framework import (
    Agent, Signal, AgentConfig, LLMConfig,
    Database, Config, parse_llm_signal, format_fundamentals
)


class GrowthQualityHybrid(Agent):
    """Hybrid agent combining growth screening with quality analysis.
    
    Strategy:
    Stage 1 (Rules): Screen for growth stocks (fast)
      - Revenue growth > 15%
      - Profit margin > 10%
      
    Stage 2 (LLM): Deep quality analysis (slow, only on candidates)
      - Uses AI to assess sustainability
      - Evaluates competitive advantages
      - Identifies potential risks
    
    Why Hybrid?
    - Analyze 500 stocks: Pure LLM = 25 min, Hybrid = 2 min
    - Cost: Pure LLM = $5, Hybrid = $0.25
    - Quality: Same depth on qualified candidates
    
    Configuration:
    - Provider: Ollama (free, local)
    - Model: llama3.2
    - Temperature: 0.6 (slightly creative for quality assessment)
    - Max Tokens: 1200 (detailed reasoning)
    """
    
    def __init__(self):
        """Initialize hybrid agent with LLM configuration."""
        config = AgentConfig(
            name="Growth Quality Hybrid",
            description="Screens for growth, analyzes quality with AI",
            llm=LLMConfig(
                provider='ollama',
                model='llama3.2',
                temperature=0.6,
                max_tokens=1200,
                system_prompt="""You are an investment analyst evaluating growth stocks for QUALITY.

A stock passed initial growth screening (revenue growth >15%, margins >10%).
Your job: Assess if this growth is SUSTAINABLE and QUALITY.

Consider:
1. Is the growth sustainable or temporary?
2. Does the company have competitive advantages?
3. What are the key risks to growth continuation?
4. Is management executing well?
5. Are profit margins stable or improving?

Be critical and thorough. Growth without quality is risky."""
            )
        )
        super().__init__(config)
    
    async def analyze(self, ticker: str, data: dict) -> Signal:
        """Two-stage hybrid analysis.
        
        Stage 1: Rule-based screening (fast)
        Stage 2: LLM quality analysis (slow, only if passed)
        
        Args:
            ticker: Stock ticker symbol
            data: Financial data dictionary
            
        Returns:
            Signal with direction, confidence, and reasoning
        """
        # Extract key metrics
        revenue_growth = data.get('revenue_growth', 0)
        profit_margin = data.get('profit_margin', 0)
        
        # STAGE 1: Rule-based screening (FAST - milliseconds)
        # Filter for growth stocks only
        if revenue_growth > 15 and profit_margin > 10:
            # Passed screening! Use LLM for deep analysis
            print(f"  ✓ {ticker} passed growth screening (Growth={revenue_growth:.1f}%, Margin={profit_margin:.1f}%)")
            print(f"  🧠 Running AI quality analysis...")
            
            # STAGE 2: LLM analysis (SLOW - seconds, but only on candidates)
            return self._llm_quality_analysis(ticker, data)
        else:
            # Didn't pass growth screening - skip LLM
            return Signal(
                direction='neutral',
                confidence=0.5,
                reasoning=f"Did not pass growth screening (Growth={revenue_growth:.1f}%, Margin={profit_margin:.1f}%). Criteria: Growth >15% AND Margin >10%"
            )
    
    def _llm_quality_analysis(self, ticker: str, data: dict) -> Signal:
        """Stage 2: Deep LLM analysis for quality assessment.
        
        This only runs on stocks that passed Stage 1 screening.
        """
        # Format data for LLM
        fundamentals_text = format_fundamentals(data)
        
        # Build prompt for quality assessment
        prompt = f"""Stock {ticker} passed growth screening:
Revenue Growth: {data.get('revenue_growth', 0):.1f}%
Profit Margin: {data.get('profit_margin', 0):.1f}%

Full fundamentals:
{fundamentals_text}

Question: Is this high-quality growth worth investing in?

Analyze:
1. Growth sustainability
2. Competitive advantages
3. Key risks
4. Overall quality rating

Provide recommendation.
Format: DIRECTION|CONFIDENCE|REASONING"""
        
        try:
            # LLM analyzes quality
            response = self.llm.chat(prompt)
            return parse_llm_signal(response, f"Hybrid analysis of {ticker}")
        
        except Exception as e:
            print(f"  ⚠️  LLM error: {e}")
            
            # Fallback: Simple quality check
            roe = data.get('roe', 0)
            debt = data.get('debt_to_equity', 0)
            
            if roe > 15 and debt < 1.0:
                return Signal(
                    direction='bullish',
                    confidence=0.6,
                    reasoning=f'LLM unavailable ({type(e).__name__}), using fallback: Growth + quality metrics (ROE={roe:.1f}%, Debt={debt:.1f})'
                )
            else:
                return Signal(
                    direction='neutral',
                    confidence=0.5,
                    reasoning=f'LLM unavailable ({type(e).__name__}), using fallback: Growth without strong quality metrics'
                )


async def main():
    """Example usage of hybrid agent."""
    print("=" * 70)
    print("Example 3: Hybrid Agent (Rules + LLM)")
    print("=" * 70)
    print("\n📚 Learning: Combine speed of rules with intelligence of AI")
    print("⚡ Speed: Fast screening + selective deep analysis")
    print("💰 Cost: 95% cheaper than pure LLM (fewer API calls)")
    print("🎯 Use Case: Analyze large numbers of stocks efficiently")
    
    # Connect to database
    connection_string = Config.get_database_url()
    
    print("\n📌 Connecting to database...")
    db = Database(connection_string)
    
    try:
        await db.connect()
        print("✅ Connected!")
        
        # Create agent
        print("\n🤖 Initializing Hybrid Agent...")
        agent = GrowthQualityHybrid()
        print("   Stage 1 (Rules): Screen for growth (>15% revenue, >10% margin)")
        print("   Stage 2 (LLM): AI quality analysis on candidates only")
        print("   Provider: Ollama (llama3.2)")
        print("   Temperature: 0.6 (balanced)")
        
        # Analyze all tickers
        tickers = await db.list_tickers()
        print(f"\n📊 Analyzing {len(tickers)} stocks: {', '.join(tickers)}")
        print(f"   Watch how rules filter before LLM analyzes...\n")
        
        passed_screening = 0
        filtered_out = 0
        
        for ticker in tickers:
            print(f"\n{'─'*70}")
            
            data = await db.get_fundamentals(ticker)
            if not data:
                print(f"⚠️  No data for {ticker}")
                continue
            
            # Show company
            print(f"📈 {ticker} - {data['name']}")
            print(f"   Growth: {data['revenue_growth']:.1f}% | Margin: {data['profit_margin']:.1f}%")
            
            # Run hybrid analysis (watch two-stage process)
            signal = await agent.analyze(ticker, data)
            
            # Track screening results
            if "passed" in signal.reasoning.lower():
                passed_screening += 1
            else:
                filtered_out += 1
            
            # Display result
            emoji = {'bullish': '🟢', 'bearish': '🔴', 'neutral': '🟡'}[signal.direction]
            print(f"\n   {emoji} {signal.direction.upper()} ({signal.confidence:.0%})")
            print(f"   {signal.reasoning}")
        
        print("\n" + "=" * 70)
        print("✅ Example completed!")
        print(f"\n📊 Screening Results:")
        print(f"   Passed screening: {passed_screening}/{len(tickers)} → LLM analyzed")
        print(f"   Filtered out: {filtered_out}/{len(tickers)} → Skipped LLM")
        print(f"   Efficiency: Saved {filtered_out} LLM calls!")
        print("\n💡 Key Takeaways:")
        print("   • Hybrid = Rules (fast filter) + LLM (deep analysis)")
        print("   • Use rules to screen thousands of stocks quickly")
        print("   • Use LLM only on the candidates that pass screening")
        print("   • 95% cost reduction vs pure LLM on large datasets")
        print("   • Perfect for production workflows with scale")
        print("\n🎯 When to Use Hybrid:")
        print("   ✓ Analyzing large universes (S&P 500, Russell 2000, etc.)")
        print("   ✓ Need both speed and intelligence")
        print("   ✓ Budget constraints on LLM API calls")
        print("   ✓ Want deterministic filtering + nuanced reasoning")
        print("\n📖 Next: Try 04_rag_agent.py for document analysis")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
