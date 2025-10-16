"""
Example Agents Using Mock Data
"""

import sys

sys.path.insert(0, ".")

from agent_builder.agents.builder import simple_agent
from agent_builder.agents.context import AgentContext


@simple_agent("PE Ratio Agent", weight=0.12)
def pe_ratio_agent(ticker, context_dict):
    """Analyze P/E ratio using real mock data"""
    context = AgentContext(ticker)
    pe_ratio = context.get_metric("pe_ratio", default=100)

    if pe_ratio < 15:
        return "bullish", 0.85
    elif pe_ratio < 20:
        return "neutral", 0.65
    elif pe_ratio < 30:
        return "bearish", 0.45
    else:
        return "strong_sell", 0.70


@simple_agent("Dividend Yield Agent", weight=0.10)
def dividend_agent(ticker, context_dict):
    """Check dividend yield"""
    context = AgentContext(ticker)
    div_yield = context.get_metric("dividend_yield", default=0)

    if div_yield > 4.0:
        return "strong_buy", 0.90
    elif div_yield > 3.0:
        return "bullish", 0.75
    elif div_yield > 2.0:
        return "neutral", 0.55
    else:
        return "bearish", 0.40


@simple_agent("Debt Ratio Agent", weight=0.08)
def debt_agent(ticker, context_dict):
    """Analyze debt to equity ratio"""
    context = AgentContext(ticker)
    debt_ratio = context.get_metric("debt_to_equity", default=0)

    if debt_ratio < 0.3:
        return "bullish", 0.85
    elif debt_ratio < 0.5:
        return "neutral", 0.65
    elif debt_ratio < 1.0:
        return "bearish", 0.50
    else:
        return "strong_sell", 0.75


@simple_agent("ROE Agent", weight=0.11)
def roe_agent(ticker, context_dict):
    """Return on Equity analysis"""
    context = AgentContext(ticker)
    roe = context.get_metric("roe", default=0)

    if roe > 20:
        return "strong_buy", 0.90
    elif roe > 15:
        return "bullish", 0.75
    elif roe > 10:
        return "neutral", 0.55
    else:
        return "bearish", 0.40


@simple_agent("News Sentiment Agent", weight=0.09)
def news_sentiment_agent(ticker, context_dict):
    """Analyze news sentiment"""
    context = AgentContext(ticker)
    news = context.get_news(limit=10)

    if not news:
        return "neutral", 0.40

    # Calculate average sentiment
    avg_sentiment = sum(n["sentiment_score"] for n in news) / len(news)

    if avg_sentiment > 0.3:
        return "bullish", 0.70
    elif avg_sentiment > 0:
        return "neutral", 0.55
    elif avg_sentiment > -0.3:
        return "bearish", 0.55
    else:
        return "strong_sell", 0.70


@simple_agent("Insider Trading Agent", weight=0.08)
def insider_agent(ticker, context_dict):
    """Analyze insider trading patterns"""
    context = AgentContext(ticker)
    trades = context.get_insider_trades(limit=15)

    if not trades:
        return "neutral", 0.40

    # Count buys vs sells
    buys = sum(1 for t in trades if t["transaction_type"] == "buy")
    sells = len(trades) - buys

    buy_ratio = buys / len(trades)

    if buy_ratio > 0.7:
        return "bullish", 0.80
    elif buy_ratio > 0.5:
        return "neutral", 0.60
    elif buy_ratio > 0.3:
        return "bearish", 0.60
    else:
        return "strong_sell", 0.75


# Test all agents
if __name__ == "__main__":
    import random

    print("=" * 60)
    print("Testing Agents with Mock Data")
    print("=" * 60)

    # Test with a random ticker
    test_ticker = random.choice(["AAPL", "MSFT", "GOOGL", "TSLA"])
    print(f"\nTesting with ticker: {test_ticker}")

    agents = [
        pe_ratio_agent,
        dividend_agent,
        debt_agent,
        roe_agent,
        news_sentiment_agent,
        insider_agent,
    ]

    for agent_func in agents:
        try:
            signal = agent_func.analyze(test_ticker)
            print(f"\n✅ {signal.agent_name}")
            print(f"   Signal: {signal.signal_type}")
            print(f"   Confidence: {signal.confidence:.2f}")
            print(f"   Reasoning: {signal.reasoning}")
        except Exception as e:
            print(f"\n❌ {agent_func.agent.name} failed: {e}")

    print("\n" + "=" * 60)
    print("✅ Agent tests complete!")
    print("=" * 60)
