"""Example 2: LLM-powered agent with customizable temperature and max_tokens.

This example shows how to:
1. Create agents with custom system prompts (personas)
2. Customize temperature per agent (conservative vs aggressive)
3. Customize max_tokens per agent (brief vs detailed)
4. Handle LLM errors with fallback logic

⚠️ DISCLAIMER: This is educational code for learning purposes only.
Do NOT use for real trading. Not financial advice. See DISCLAIMER.md for full terms.
"""

import asyncio
import os
from agent_framework import (
    Agent, Signal, AgentConfig, LLMConfig, 
    Config, parse_llm_signal, format_fundamentals
)
from agent_framework.database import Database


class ConservativeInvestorAgent(Agent):
    """Conservative investor with risk-averse persona and low temperature."""
    
    def __init__(self):
        """Initialize with conservative persona and focused analysis."""
        config = AgentConfig(
            name="Conservative Investor",
            description="Risk-averse value investor focusing on safety",
            llm=LLMConfig(
                provider='ollama',  # or 'openai', 'anthropic'
                model='llama3.2',
                temperature=0.3,    # Low temperature for consistent, focused analysis
                max_tokens=1000,    # Moderate detail level
                system_prompt="""You are a conservative value investor with 30 years of experience.

Your investment philosophy:
- Safety of principal is paramount
- Focus on companies with low PE ratios (< 15)
- Prefer high dividend yields (> 2%)
- Avoid high-debt companies
- Look for stable, profitable businesses
- Be skeptical of high-growth narratives

Analyze companies critically and conservatively. If in doubt, recommend caution."""
            )
        )
        super().__init__(config)
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze using LLM with conservative persona and low temperature."""
        # Build analysis prompt using utility function
        fundamentals_text = format_fundamentals(data)
        
        prompt = f"""Analyze {ticker} with the following data:
        
{fundamentals_text}

Provide your investment recommendation as:
1. Direction (bullish/bearish/neutral)
2. Confidence (0-100%)
3. Brief reasoning

Format: DIRECTION|CONFIDENCE|REASONING"""
        
        try:
            # Query LLM (uses system prompt automatically)
            response = self.llm.chat(prompt)
            
            # Parse response using utility function
            return parse_llm_signal(response, f"Conservative analysis of {ticker}")
        
        except Exception as e:
            print(f"⚠️  LLM error: {e}")
            # Fallback to rule-based analysis
            pe = data.get('pe_ratio', 0)
            div_yield = data.get('dividend_yield', 0)
            
            if pe < 15 and div_yield > 2:
                return Signal('bullish', 0.7, 'Low PE with good dividend (rule-based fallback)')
            return Signal('neutral', 0.5, f'LLM unavailable, rule-based fallback: PE={pe:.1f}')


class AggressiveTraderAgent(Agent):
    """Aggressive trader with growth-focused persona and high temperature."""
    
    def __init__(self):
        """Initialize with aggressive growth persona and creative analysis."""
        config = AgentConfig(
            name="Aggressive Growth Trader",
            description="High-risk, high-reward growth focused",
            llm=LLMConfig(
                provider='ollama',
                model='llama3.2',
                temperature=0.9,    # High temperature for creative, diverse ideas
                max_tokens=1500,    # More detailed analysis
                system_prompt="""You are an aggressive growth trader seeking maximum returns.

Your trading philosophy:
- Growth is everything - chase revenue growth > 30%
- PE ratios don't matter if growth is strong
- Love disruption and innovation
- Not concerned about short-term profitability
- High conviction in winners, cut losers fast
- Momentum matters - follow the trend

Be bold and opportunistic. Look for explosive growth potential."""
            )
        )
        super().__init__(config)
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze using LLM with aggressive persona and high temperature."""
        fundamentals_text = format_fundamentals(data)
        
        prompt = f"""Analyze {ticker} with aggressive growth mindset:
        
{fundamentals_text}

What's your aggressive take? Look for explosive growth opportunities.
Format: DIRECTION|CONFIDENCE|REASONING"""
        
        try:
            response = self.llm.chat(prompt)
            return parse_llm_signal(response, f"Aggressive analysis of {ticker}")
        
        except Exception as e:
            print(f"⚠️  LLM error: {e}")
            # Fallback
            growth = data.get('revenue_growth', 0)
            
            if growth > 30:
                return Signal('bullish', 0.8, 'High growth (rule-based fallback)')
            return Signal('neutral', 0.5, f'LLM unavailable, rule-based fallback: growth={growth:.1f}%')


class DetailedAnalystAgent(Agent):
    """Detailed analyst with high max_tokens for comprehensive reports."""
    
    def __init__(self):
        """Initialize with balanced temperature and high max_tokens for detail."""
        config = AgentConfig(
            name="Detailed Analyst",
            description="Comprehensive, detailed analysis",
            llm=LLMConfig(
                provider='ollama',
                model='llama3.2',
                temperature=0.5,    # Balanced temperature
                max_tokens=2500,    # High tokens for detailed analysis
                system_prompt="""You are a thorough research analyst providing comprehensive reports.

Your approach:
- Analyze multiple perspectives
- Consider both opportunities and risks
- Provide detailed reasoning
- Back up claims with data
- Be thorough and comprehensive

Provide detailed, well-reasoned analysis."""
            )
        )
        super().__init__(config)
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze with detailed, comprehensive approach."""
        fundamentals_text = format_fundamentals(data)
        
        prompt = f"""Provide comprehensive analysis of {ticker}:

{fundamentals_text}

Consider:
1. Valuation metrics (PE, PB ratios)
2. Growth prospects (revenue growth)
3. Financial health (margins, debt, ROE)
4. Risk factors
5. Overall investment thesis

Provide detailed reasoning. Format: DIRECTION|CONFIDENCE|DETAILED_REASONING"""
        
        try:
            response = self.llm.chat(prompt)
            return parse_llm_signal(response, f"Detailed analysis of {ticker}")
        
        except Exception as e:
            print(f"⚠️  LLM error: {e}")
            return Signal('neutral', 0.5, f'LLM error: {str(e)[:100]}')


async def main():
    """Compare different agent configurations (temperature, max_tokens, personas)."""
    print("=" * 70)
    print("AI Agent Framework - LLM Agent Example")
    print("Custom Temperature, Max Tokens, and System Prompt Personas")
    print("=" * 70)
    
    # Check for Ollama
    if not os.path.exists('/usr/local/bin/ollama') and not os.path.exists('/usr/bin/ollama'):
        print("\n⚠️  This example requires Ollama installed locally.")
        print("Install: https://ollama.ai")
        print("\nAlternatively, change provider to 'openai' or 'anthropic'")
        print("and set API keys in .env file")
        return
    
    # Connect to database
    connection_string = Config.get_database_url()
    
    print("\n📌 Connecting to database...")
    db = Database(connection_string)
    
    try:
        await db.connect()
        print("✅ Connected!")
        
        # Initialize agents with different configurations
        print("\n🤖 Initializing agents with custom configurations...")
        
        conservative = ConservativeInvestorAgent()
        print("  ✓ Conservative Investor (temp=0.3, tokens=1000, focused)")
        
        aggressive = AggressiveTraderAgent()
        print("  ✓ Aggressive Trader (temp=0.9, tokens=1500, creative)")
        
        detailed = DetailedAnalystAgent()
        print("  ✓ Detailed Analyst (temp=0.5, tokens=2500, comprehensive)")
        
        print("✅ Agents ready!")
        
        # Analyze different stocks
        for ticker in ['TSLA', 'JPM']:
            data = await db.get_fundamentals(ticker)
            if not data:
                print(f"\n⚠️  No data for {ticker}")
                continue
            
            print(f"\n{'='*70}")
            print(f"📊 Analyzing {ticker} - {data['name']}")
            print(f"{'='*70}")
            print(f"PE: {data['pe_ratio']:.1f} | Growth: {data['revenue_growth']:.1f}% | "
                  f"Margin: {data['profit_margin']:.1f}% | Div Yield: {data['dividend_yield']:.1f}%")
            
            # Conservative analysis (low temp, focused)
            print(f"\n🛡️  Conservative Investor (T=0.3, MT=1000):")
            cons_signal = conservative.analyze(ticker, data)
            print(f"   {cons_signal.direction.upper()} ({cons_signal.confidence:.0%})")
            print(f"   {cons_signal.reasoning[:150]}...")
            
            # Aggressive analysis (high temp, creative)
            print(f"\n🚀 Aggressive Trader (T=0.9, MT=1500):")
            agg_signal = aggressive.analyze(ticker, data)
            print(f"   {agg_signal.direction.upper()} ({agg_signal.confidence:.0%})")
            print(f"   {agg_signal.reasoning[:150]}...")
            
            # Detailed analysis (balanced temp, high tokens)
            print(f"\n📊 Detailed Analyst (T=0.5, MT=2500):")
            det_signal = detailed.analyze(ticker, data)
            print(f"   {det_signal.direction.upper()} ({det_signal.confidence:.0%})")
            print(f"   {det_signal.reasoning[:200]}...")
        
        print("\n" + "=" * 70)
        print("✅ Example completed!")
        print("\nKey Takeaways:")
        print("  • Each agent can have custom temperature and max_tokens")
        print("  • Low temperature (0.3) = Focused, consistent analysis")
        print("  • High temperature (0.9) = Creative, diverse ideas")
        print("  • High max_tokens (2500) = Detailed, comprehensive output")
        print("  • System prompts define agent personality and approach")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
