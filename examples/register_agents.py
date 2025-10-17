"""
Simple Test Agents - Minimal Example for Testing Workflow
Save as: examples/register_agents.py

This file contains 3 simple agents to test the system:
1. PE Ratio Agent - Tests fundamental data access
2. Price Trend Agent - Tests price data access
3. News Agent - Tests news data access
"""

from agent_builder import agent, get_registry
from examples.my_agents import register_my_agents

# ============================================================================
# AGENT 1: PE Ratio Check (Fundamental Data)
# ============================================================================


@agent("PE Ratio Agent", "Simple P/E ratio analyzer")
def pe_ratio_agent(ticker, context):
    """
    Tests: Database connection, fundamental data access, basic logic

    Returns bullish if P/E < 20, bearish if P/E > 40, neutral otherwise
    """
    # Get P/E ratio from database
    pe = context.get_fundamental("pe_ratio", default=25)

    print(f"[PE Agent] Analyzing {ticker}: P/E = {pe}")

    # Simple logic
    if pe < 20:
        return "bullish", 0.8, f"Low P/E ratio of {pe:.1f} suggests good value"
    elif pe > 40:
        return "bearish", 0.7, f"High P/E ratio of {pe:.1f} suggests overvaluation"
    else:
        return "neutral", 0.5, f"Average P/E ratio of {pe:.1f}"


# ============================================================================
# AGENT 2: Price Trend Check (Technical Data)
# ============================================================================


@agent("Price Trend Agent", "Simple moving average trend analyzer")
def price_trend_agent(ticker, context):
    """
    Tests: Price data access, technical indicators, list handling

    Compares current price to 20-day moving average
    """
    # Get recent price data
    prices = context.get_price_data(days=5)

    if not prices or len(prices) == 0:
        print(f"[Trend Agent] No price data for {ticker}")
        return "neutral", 0.3, "No price data available"

    # Get latest price and SMA
    latest = prices[0]
    current_price = latest.get("close", 0)
    sma_20 = latest.get("sma_20", 0)

    print(
        f"[Trend Agent] Analyzing {ticker}: Price = ${current_price:.2f}, SMA20 = ${sma_20:.2f}"
    )

    # Simple logic
    if current_price > sma_20:
        diff_pct = ((current_price - sma_20) / sma_20) * 100
        return (
            "bullish",
            0.7,
            f"Price ${current_price:.2f} is {diff_pct:.1f}% above SMA20",
        )
    elif current_price < sma_20:
        diff_pct = ((sma_20 - current_price) / sma_20) * 100
        return (
            "bearish",
            0.6,
            f"Price ${current_price:.2f} is {diff_pct:.1f}% below SMA20",
        )
    else:
        return "neutral", 0.5, f"Price at SMA20: ${current_price:.2f}"


# ============================================================================
# AGENT 3: News Sentiment Check (Sentiment Data)
# ============================================================================


@agent("News Sentiment Agent", "Simple news sentiment analyzer")
def news_sentiment_agent(ticker, context):
    """
    Tests: News data access, aggregation, sentiment scoring

    Analyzes recent news sentiment
    """
    # Get recent news
    news = context.get_news(limit=5)

    if not news or len(news) == 0:
        print(f"[News Agent] No news for {ticker}")
        return "neutral", 0.3, "No recent news available"

    # Calculate average sentiment
    sentiments = [n.get("sentiment_score", 0) for n in news]
    avg_sentiment = sum(sentiments) / len(sentiments)

    print(
        f"[News Agent] Analyzing {ticker}: {len(news)} articles, avg sentiment = {avg_sentiment:.2f}"
    )

    # Simple logic
    if avg_sentiment > 0.3:
        return (
            "bullish",
            0.75,
            f"Positive news sentiment: {avg_sentiment:.2f} from {len(news)} articles",
        )
    elif avg_sentiment < -0.3:
        return (
            "bearish",
            0.75,
            f"Negative news sentiment: {avg_sentiment:.2f} from {len(news)} articles",
        )
    else:
        return "neutral", 0.5, f"Mixed news sentiment: {avg_sentiment:.2f}"


# ============================================================================
# REGISTER AGENTS
# ============================================================================


def register_all_agents():
    """
    Register the test agents

    This function is called by the API on startup
    """
    registry = get_registry()

    print("\n" + "=" * 70)
    print("REGISTERING TEST AGENTS")
    print("=" * 70)

    # Register each agent with weights
    registry.register(pe_ratio_agent.agent, weight=1.0, tags=["fundamental", "test"])
    print("✅ Registered: PE Ratio Agent")

    registry.register(price_trend_agent.agent, weight=1.0, tags=["technical", "test"])
    print("✅ Registered: Price Trend Agent")

    registry.register(
        news_sentiment_agent.agent, weight=1.0, tags=["sentiment", "test"]
    )
    print("✅ Registered: News Sentiment Agent")

    register_my_agents()
    # Show summary
    stats = registry.stats()
    agent_ids = registry.list_all()
    print(f"\n📊 Total agents registered: {stats['total']}")
    print(f"📊 Enabled agents: {stats['enabled']}")
    print(f"📊 Agent IDs: {', '.join(agent_ids)}")
    print("=" * 70 + "\n")


# ============================================================================
# STANDALONE TEST (Optional - for debugging)
# ============================================================================

if __name__ == "__main__":
    """
    Test agents directly without API
    Usage: python examples/register_agents.py
    """
    from agent_builder.core.config import Config
    from agent_builder.core.database import DatabasePool, Database
    from agent_builder.agents.context import AgentContext

    print("\n🧪 STANDALONE AGENT TEST\n")

    # Setup
    config = Config.from_env()
    pool = DatabasePool(config.database)
    db = Database(pool)

    # Test ticker
    ticker = "AAPL"
    context = AgentContext(ticker, db)

    # Test each agent
    agents = [
        ("PE Ratio Agent", pe_ratio_agent),
        ("Price Trend Agent", price_trend_agent),
        ("News Sentiment Agent", news_sentiment_agent),
    ]

    print(f"Testing agents for {ticker}:\n")

    for name, agent_func in agents:
        try:
            signal = agent_func.agent.analyze(ticker, context)
            print(f"\n{name}:")
            print(f"  Signal: {signal.signal_type}")
            print(f"  Confidence: {signal.confidence:.0%}")
            print(f"  Reasoning: {signal.reasoning}")
        except Exception as e:
            print(f"\n{name}: ❌ ERROR - {e}")

    pool.close()
    print("\n✅ Test complete\n")
