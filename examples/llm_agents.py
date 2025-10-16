"""
Example LLM-Powered Agents
"""

import sys

sys.path.insert(0, ".")

from agent_builder.agents.builder import simple_agent
from agent_builder.agents.context import AgentContext
from agent_builder.llm.factory import get_llm_provider


@simple_agent("LLM News Analyst", weight=0.12)
def llm_news_agent(ticker, context):
    """
    Analyze news sentiment using LLM

    Uses LLM to understand nuanced sentiment in headlines
    """
    # Get news
    news = context.get_news(limit=5)

    if not news:
        return "neutral", 0.4

    # Get LLM
    llm = get_llm_provider()
    if not llm:
        # Fallback to simple sentiment if no LLM
        avg_sentiment = sum(n["sentiment_score"] for n in news) / len(news)
        return ("bullish", 0.6) if avg_sentiment > 0 else ("bearish", 0.6)

    # Build prompt
    headlines = "\n".join([f"- {n['headline']}" for n in news])

    prompt = f"""Analyze these recent news headlines for {ticker}:

{headlines}

Based on these headlines, is the overall sentiment:
- bullish (positive for stock price)
- bearish (negative for stock price)
- neutral (mixed or unclear)

Respond with ONLY ONE WORD: bullish, bearish, or neutral"""

    # Get LLM response
    response = llm.generate(prompt, temperature=0.3, max_tokens=10)
    response_lower = response.lower().strip()

    # Parse response
    if "bullish" in response_lower:
        return "bullish", 0.75
    elif "bearish" in response_lower:
        return "bearish", 0.75
    else:
        return "neutral", 0.6


@simple_agent("LLM Fundamental Analyst", weight=0.15)
def llm_fundamental_agent(ticker, context):
    """
    Comprehensive fundamental analysis using LLM

    Analyzes multiple metrics holistically
    """
    # Get fundamentals
    fund = context.get_fundamentals()

    if not fund:
        return "neutral", 0.4

    # Get LLM
    llm = get_llm_provider()
    if not llm:
        return "neutral", 0.5

    # Build detailed prompt
    prompt = f"""Analyze these fundamentals for {ticker}:

Company: {fund.get('company_name', ticker)}
Sector: {fund.get('sector', 'Unknown')}

Valuation:
- P/E Ratio: {fund.get('pe_ratio', 'N/A')}
- PEG Ratio: {fund.get('peg_ratio', 'N/A')}
- Price/Book: {fund.get('price_to_book', 'N/A')}

Profitability:
- ROE: {fund.get('roe', 'N/A')}%
- Profit Margin: {fund.get('profit_margin', 'N/A')}%
- Operating Margin: {fund.get('operating_margin', 'N/A')}%

Financial Health:
- Debt/Equity: {fund.get('debt_to_equity', 'N/A')}
- Current Ratio: {fund.get('current_ratio', 'N/A')}

Income:
- Dividend Yield: {fund.get('dividend_yield', 'N/A')}%

Based on these metrics, provide an investment recommendation.
Respond with: bullish, bearish, or neutral, followed by your confidence (0.0-1.0).

Format: <signal> <confidence>
Example: bullish 0.85"""

    # Get LLM response
    response = llm.generate(prompt, temperature=0.5, max_tokens=50)

    # Parse response
    parts = response.lower().split()

    signal_type = "neutral"
    confidence = 0.6

    # Extract signal
    if "bullish" in parts:
        signal_type = "bullish"
    elif "bearish" in parts:
        signal_type = "bearish"

    # Extract confidence (look for number between 0 and 1)
    for part in parts:
        try:
            conf = float(part)
            if 0 <= conf <= 1:
                confidence = conf
                break
        except ValueError:
            continue

    return signal_type, confidence


@simple_agent("LLM Strategic Analyst", weight=0.10)
def llm_strategic_agent(ticker, context):
    """
    Strategic analysis combining multiple data sources

    Uses LLM to synthesize fundamentals, news, and insider activity
    """
    llm = get_llm_provider()
    if not llm:
        return "neutral", 0.5

    # Gather data
    fund = context.get_fundamentals()
    news = context.get_news(limit=3)
    trades = context.get_insider_trades(limit=5)

    # Build comprehensive prompt
    news_summary = (
        "\n".join([f"- {n['headline']}" for n in news]) if news else "No recent news"
    )

    insider_summary = ""
    if trades:
        buys = sum(1 for t in trades if t["transaction_type"] == "buy")
        sells = len(trades) - buys
        insider_summary = f"Insiders: {buys} buys, {sells} sells"
    else:
        insider_summary = "No insider activity"

    prompt = f"""Strategic analysis for {ticker}:

FUNDAMENTALS:
- P/E: {fund.get('pe_ratio', 'N/A')}
- ROE: {fund.get('roe', 'N/A')}%
- Debt/Equity: {fund.get('debt_to_equity', 'N/A')}

RECENT NEWS:
{news_summary}

INSIDER ACTIVITY:
{insider_summary}

Considering all factors, what's your strategic recommendation?
Respond: bullish, bearish, or neutral (one word only)"""

    response = llm.generate(prompt, temperature=0.4, max_tokens=20)
    response_lower = response.lower()

    if "bullish" in response_lower:
        return "bullish", 0.70
    elif "bearish" in response_lower:
        return "bearish", 0.70
    else:
        return "neutral", 0.55


# Test LLM agents
if __name__ == "__main__":
    print("=" * 70)
    print("Testing LLM-Powered Agents")
    print("=" * 70)

    # Check LLM availability
    from agent_builder.llm.factory import get_llm_provider

    llm = get_llm_provider()

    if not llm:
        print("\n⚠️  No LLM configured!")
        print("   Set LLM_PROVIDER in .env to 'ollama' or 'groq'")
        print("\n   For Ollama:")
        print("   1. Install: curl -fsSL https://ollama.com/install.sh | sh")
        print("   2. Run: ollama pull llama3.2")
        print("   3. Serve: ollama serve")
        print("\n   For Groq:")
        print("   1. Get key: console.groq.com")
        print("   2. Set GROQ_API_KEY in .env")
        sys.exit(1)

    print(f"\n✅ LLM Provider: {llm.__class__.__name__}")
    print(f"   Model: {llm.model}")

    # Check if available
    if hasattr(llm, "is_available"):
        if llm.is_available():
            print(f"   Status: Connected ✅")
        else:
            print(f"   Status: Not available ❌")
            sys.exit(1)

    # Test with a ticker
    test_ticker = "AAPL"
    print(f"\n🧪 Testing LLM agents on {test_ticker}...")

    agents = [llm_news_agent, llm_fundamental_agent, llm_strategic_agent]

    for agent_func in agents:
        try:
            print(f"\n📊 {agent_func.agent.name}")
            signal = agent_func.analyze(test_ticker)
            print(f"   Signal: {signal.signal_type}")
            print(f"   Confidence: {signal.confidence:.2f}")
            print(f"   ✅ Success")
        except Exception as e:
            print(f"   ❌ Error: {e}")

    print("\n" + "=" * 70)
    print("✅ LLM agents working!")
    print("=" * 70)
