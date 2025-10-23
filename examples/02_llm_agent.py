"""Example 2: LLM-powered agent with system prompt persona and error handling."""

import asyncio
import os
from agent_framework import (
    Agent, Signal, AgentConfig, LLMConfig, 
    Config, parse_llm_signal, format_fundamentals
)
from agent_framework.database import Database


class ConservativeInvestorAgent(Agent):
    """Conservative investor with risk-averse persona via system prompt."""
    
    def __init__(self):
        """Initialize with conservative persona."""
        config = AgentConfig(
            name="Conservative Investor",
            description="Risk-averse value investor focusing on safety",
            llm=LLMConfig(
                provider='ollama',  # or 'openai', 'anthropic'
                model='llama3.2',
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
        """Analyze using LLM with conservative persona."""
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
    """Aggressive trader with growth-focused persona."""
    
    def __init__(self):
        """Initialize with aggressive growth persona."""
        config = AgentConfig(
            name="Aggressive Growth Trader",
            description="High-risk, high-reward growth focused",
            llm=LLMConfig(
                provider='ollama',
                model='llama3.2',
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
        """Analyze using LLM with aggressive persona."""
        fundamentals_text = format_fundamentals(data)
        
        prompt = f"""Analyze {ticker}:
        
{fundamentals_text}

What's your aggressive take? Format: DIRECTION|CONFIDENCE|REASONING"""
        
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


async def main():
    """Compare conservative vs aggressive personas."""
    print("=" * 60)
    print("AI Agent Framework - LLM Agent Example")
    print("System Prompt Personas: Conservative vs Aggressive")
    print("=" * 60)
    
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
        
        # Initialize agents
        print("\n🤖 Initializing agents...")
        conservative = ConservativeInvestorAgent()
        aggressive = AggressiveTraderAgent()
        print("✅ Agents ready!")
        
        # Analyze TSLA (high growth) and JPM (value)
        for ticker in ['TSLA', 'JPM']:
            data = await db.get_fundamentals(ticker)
            if not data:
                print(f"\n⚠️  No data for {ticker}")
                continue
            
            print(f"\n{'='*60}")
            print(f"📊 Analyzing {ticker} - {data['name']}")
            print(f"{'='*60}")
            print(f"PE: {data['pe_ratio']:.1f} | Growth: {data['revenue_growth']:.1f}% | "
                  f"Div Yield: {data['dividend_yield']:.1f}%")
            
            # Conservative analysis
            print(f"\n🛡️  Conservative Investor:")
            cons_signal = conservative.analyze(ticker, data)
            print(f"   {cons_signal.direction.upper()} ({cons_signal.confidence:.0%})")
            print(f"   {cons_signal.reasoning}")
            
            # Aggressive analysis
            print(f"\n🚀 Aggressive Trader:")
            agg_signal = aggressive.analyze(ticker, data)
            print(f"   {agg_signal.direction.upper()} ({agg_signal.confidence:.0%})")
            print(f"   {agg_signal.reasoning}")
        
        print("\n" + "=" * 60)
        print("✅ LLM personas demonstrate different investment styles!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
