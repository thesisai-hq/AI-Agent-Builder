"""Example 2: LLM-powered agent with system prompt persona and PostgreSQL."""

import asyncio
import os
from agent_framework import Agent, Signal, AgentConfig, LLMConfig
from agent_framework.database import get_database


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
        # Build analysis prompt
        prompt = f"""Analyze {ticker} with the following data:
        
PE Ratio: {data.get('pe_ratio', 0):.1f}
Dividend Yield: {data.get('dividend_yield', 0):.1f}%
Debt-to-Equity: {data.get('debt_to_equity', 0):.1f}
Profit Margin: {data.get('profit_margin', 0):.1f}%
ROE: {data.get('roe', 0):.1f}%

Provide your investment recommendation as:
1. Direction (bullish/bearish/neutral)
2. Confidence (0-100%)
3. Brief reasoning

Format: DIRECTION|CONFIDENCE|REASONING"""
        
        # Query LLM (uses system prompt automatically)
        response = self.llm.chat(prompt)
        
        # Parse response
        try:
            parts = response.split('|')
            direction = parts[0].strip().lower()
            confidence = float(parts[1].strip()) / 100
            reasoning = parts[2].strip()
            
            return Signal(direction, confidence, reasoning)
        except:
            # Fallback if parsing fails
            return Signal('neutral', 0.5, response[:200])


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
        prompt = f"""Analyze {ticker}:
        
Revenue Growth: {data.get('revenue_growth', 0):.1f}%
PE Ratio: {data.get('pe_ratio', 0):.1f}
Profit Margin: {data.get('profit_margin', 0):.1f}%
Market Cap: ${data.get('market_cap', 0)/1e9:.1f}B

What's your aggressive take? Format: DIRECTION|CONFIDENCE|REASONING"""
        
        response = self.llm.chat(prompt)
        
        try:
            parts = response.split('|')
            direction = parts[0].strip().lower()
            confidence = float(parts[1].strip()) / 100
            reasoning = parts[2].strip()
            return Signal(direction, confidence, reasoning)
        except:
            return Signal('neutral', 0.5, response[:200])


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
    connection_string = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:postgres@localhost:5432/agent_framework'
    )
    
    print("\n🔌 Connecting to database...")
    db = get_database(connection_string)
    await db.connect()
    print("✅ Connected!")
    
    # Initialize agents
    conservative = ConservativeInvestorAgent()
    aggressive = AggressiveTraderAgent()
    
    try:
        # Analyze TSLA (high growth) and JPM (value)
        for ticker in ['TSLA', 'JPM']:
            data = await db.get_fundamentals(ticker)
            
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
        
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())