"""
Example LLM Agents with Personas
"""

import sys

sys.path.insert(0, ".")

from agent_builder.agents.builder import simple_agent
from agent_builder.agents.context import AgentContext
from agent_builder.llm.factory import get_llm_provider
from agent_builder.agents.personas import AgentPersonas


@simple_agent("Fundamental Analyst (LLM)", weight=0.15)
def fundamental_analyst_llm(ticker, context):
    """
    Deep fundamental analysis with analyst persona

    Uses LLM with fundamental analyst persona for thorough analysis
    """
    llm = get_llm_provider()
    if not llm:
        return "neutral", 0.5

    # Get data
    fund = context.get_fundamentals()

    if not fund:
        return "neutral", 0.4

    # Build prompt
    prompt = f"""Analyze {ticker} ({fund.get('company_name', ticker)}) from a fundamental perspective:

VALUATION METRICS:
- P/E Ratio: {fund.get('pe_ratio', 'N/A')}
- PEG Ratio: {fund.get('peg_ratio', 'N/A')}
- Price/Book: {fund.get('price_to_book', 'N/A')}

PROFITABILITY:
- ROE: {fund.get('roe', 'N/A')}%
- ROA: {fund.get('roa', 'N/A')}%
- Profit Margin: {fund.get('profit_margin', 'N/A')}%
- Operating Margin: {fund.get('operating_margin', 'N/A')}%

FINANCIAL HEALTH:
- Debt/Equity: {fund.get('debt_to_equity', 'N/A')}
- Current Ratio: {fund.get('current_ratio', 'N/A')}

Based on your analysis, provide your investment recommendation.
Respond with ONLY: bullish, bearish, or neutral"""

    # Generate with persona
    response = llm.generate(
        prompt=prompt, system_prompt=AgentPersonas.FUNDAMENTAL_ANALYST, temperature=0.4
    )

    response_lower = response.lower()

    if "bullish" in response_lower:
        return "bullish", 0.85
    elif "bearish" in response_lower:
        return "bearish", 0.85
    else:
        return "neutral", 0.70


@simple_agent("Value Investor (LLM)", weight=0.12)
def value_investor_llm(ticker, context):
    """
    Value investing perspective with Buffett-style persona

    Looks for undervalued stocks with margin of safety
    """
    llm = get_llm_provider()
    if not llm:
        return "neutral", 0.5

    fund = context.get_fundamentals()

    if not fund:
        return "neutral", 0.4

    prompt = f"""Evaluate {ticker} as a value investment opportunity:

VALUATION:
- P/E Ratio: {fund.get('pe_ratio', 'N/A')} (Market avg: ~20)
- Price/Book: {fund.get('price_to_book', 'N/A')} (Value threshold: <3)
- PEG Ratio: {fund.get('peg_ratio', 'N/A')} (Value threshold: <1.5)

QUALITY:
- ROE: {fund.get('roe', 'N/A')}% (Good: >15%)
- Debt/Equity: {fund.get('debt_to_equity', 'N/A')} (Safe: <0.5)
- Current Ratio: {fund.get('current_ratio', 'N/A')} (Safe: >1.5)

Is this stock undervalued with a margin of safety?
Respond with ONLY: bullish (undervalued), bearish (overvalued), or neutral"""

    response = llm.generate(
        prompt=prompt, system_prompt=AgentPersonas.VALUE_INVESTOR, temperature=0.3
    )

    response_lower = response.lower()

    if "bullish" in response_lower:
        return "bullish", 0.90
    elif "bearish" in response_lower:
        return "bearish", 0.85
    else:
        return "neutral", 0.75


@simple_agent("Risk Analyst (LLM)", weight=0.11)
def risk_analyst_llm(ticker, context):
    """
    Risk-focused analysis with risk analyst persona

    Emphasizes downside protection and risk factors
    """
    llm = get_llm_provider()
    if not llm:
        return "neutral", 0.5

    fund = context.get_fundamentals()
    news = context.get_news(limit=3)

    if not fund:
        return "neutral", 0.4

    # Build risk-focused prompt
    news_summary = (
        "\n".join([f"- {n['headline']}" for n in news]) if news else "No recent news"
    )

    prompt = f"""Assess the risk profile for {ticker}:

FINANCIAL RISK:
- Debt/Equity: {fund.get('debt_to_equity', 'N/A')} (Risky if >1.0)
- Current Ratio: {fund.get('current_ratio', 'N/A')} (Risky if <1.0)
- Beta: {fund.get('beta', 'N/A')} (Volatile if >1.5)

VALUATION RISK:
- P/E Ratio: {fund.get('pe_ratio', 'N/A')} (Bubble if >40)
- Price/Book: {fund.get('price_to_book', 'N/A')} (Expensive if >5)

NEWS SENTIMENT:
{news_summary}

From a risk management perspective, what's your assessment?
Respond: bullish (low risk), bearish (high risk), or neutral"""

    response = llm.generate(
        prompt=prompt, system_prompt=AgentPersonas.RISK_ANALYST, temperature=0.3
    )

    response_lower = response.lower()

    if "bearish" in response_lower or "high risk" in response_lower:
        return "bearish", 0.80
    elif "bullish" in response_lower or "low risk" in response_lower:
        return "bullish", 0.75
    else:
        return "neutral", 0.65


@simple_agent("Dividend Investor (LLM)", weight=0.10)
def dividend_investor_llm(ticker, context):
    """
    Income-focused analysis with dividend investor persona

    Prioritizes dividend yield and sustainability
    """
    llm = get_llm_provider()
    if not llm:
        return "neutral", 0.5

    fund = context.get_fundamentals()

    if not fund:
        return "neutral", 0.4

    prompt = f"""Evaluate {ticker} as a dividend investment:

INCOME METRICS:
- Dividend Yield: {fund.get('dividend_yield', 'N/A')}% (Target: >3%)
- Payout Ratio: Calculate from available data

SUSTAINABILITY:
- ROE: {fund.get('roe', 'N/A')}% (Need: >10% for sustainability)
- Debt/Equity: {fund.get('debt_to_equity', 'N/A')} (Safe: <0.5)
- Current Ratio: {fund.get('current_ratio', 'N/A')} (Safe: >1.5)

PROFITABILITY:
- Profit Margin: {fund.get('profit_margin', 'N/A')}%

Is this a good dividend investment with sustainable payouts?
Respond: bullish (good income), bearish (risky income), or neutral"""

    response = llm.generate(
        prompt=prompt, system_prompt=AgentPersonas.DIVIDEND_INVESTOR, temperature=0.4
    )

    response_lower = response.lower()

    if "bullish" in response_lower:
        return "bullish", 0.85
    elif "bearish" in response_lower:
        return "bearish", 0.80
    else:
        return "neutral", 0.70


@simple_agent("Growth Investor (LLM)", weight=0.13)
def growth_investor_llm(ticker, context):
    """
    Growth-focused analysis with growth investor persona

    Seeks high-growth opportunities, accepts higher valuations
    """
    llm = get_llm_provider()
    if not llm:
        return "neutral", 0.5

    fund = context.get_fundamentals()

    if not fund:
        return "neutral", 0.4

    prompt = f"""Evaluate {ticker} from a growth investing perspective:

GROWTH INDICATORS:
- Profit Margin: {fund.get('profit_margin', 'N/A')}% (Higher = better pricing power)
- ROE: {fund.get('roe', 'N/A')}% (High ROE = efficient growth)
- Operating Margin: {fund.get('operating_margin', 'N/A')}%

VALUATION (growth context):
- P/E Ratio: {fund.get('pe_ratio', 'N/A')} (Can be high for growth)
- PEG Ratio: {fund.get('peg_ratio', 'N/A')} (Key metric - want <2)

SECTOR:
- {fund.get('sector', 'Unknown')} (Is this a growth sector?)

Does this stock have strong growth potential worth the valuation?
Respond: bullish (strong growth), bearish (growth concerns), or neutral"""

    response = llm.generate(
        prompt=prompt, system_prompt=AgentPersonas.GROWTH_INVESTOR, temperature=0.5
    )

    response_lower = response.lower()

    if "bullish" in response_lower:
        return "bullish", 0.80
    elif "bearish" in response_lower:
        return "bearish", 0.75
    else:
        return "neutral", 0.65


# Test agents with personas
if __name__ == "__main__":
    print("=" * 70)
    print("🎭 Testing LLM Agents with Personas")
    print("=" * 70)

    # Check LLM
    from agent_builder.llm.factory import get_llm_provider

    llm = get_llm_provider()

    if not llm:
        print("\n⚠️  No LLM configured!")
        print("   Setup Ollama or Groq first")
        sys.exit(1)

    print(f"\n✅ LLM Provider: {llm.__class__.__name__}")
    print(f"   Model: {llm.model}")

    # Test personas
    test_ticker = "AAPL"
    print(f"\n🧪 Testing different analyst personas on {test_ticker}...")

    agents = [
        ("Fundamental Analyst", fundamental_analyst_llm),
        ("Value Investor", value_investor_llm),
        ("Risk Analyst", risk_analyst_llm),
        ("Dividend Investor", dividend_investor_llm),
        ("Growth Investor", growth_investor_llm),
    ]

    for name, agent_func in agents:
        try:
            print(f"\n👤 {name}")
            signal = agent_func.analyze(test_ticker)
            print(f"   Signal: {signal.signal_type}")
            print(f"   Confidence: {signal.confidence:.2f}")
            print(f"   ✅ Success")
        except Exception as e:
            print(f"   ❌ Error: {e}")

    print("\n" + "=" * 70)
    print("✅ All personas working!")
    print("=" * 70)
    print("\n💡 Each agent has a different perspective:")
    print("   - Fundamental: Deep analysis, conservative")
    print("   - Value: Seeking undervalued opportunities")
    print("   - Risk: Focused on downside protection")
    print("   - Dividend: Income and sustainability")
    print("   - Growth: High-growth potential")
    print("\n🎯 Different personas = diverse perspectives = better consensus!")
