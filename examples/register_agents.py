"""
Register All Available Agents

This file is imported at API startup and registers all agents.
Add new agents here to make them available via API.
"""

import sys

sys.path.insert(0, ".")

from agent_builder.agents.builder import simple_agent
from agent_builder.agents.registry import get_registry
from agent_builder.agents.context import AgentContext
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# BASIC RULE-BASED AGENTS
# ============================================================================


@simple_agent("PE Ratio Agent", weight=0.12)
def pe_ratio_agent(ticker, context):
    """Analyze P/E ratio"""
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
def dividend_agent(ticker, context):
    """Check dividend yield"""
    div_yield = context.get_metric("dividend_yield", default=0)

    if div_yield > 4.0:
        return "bullish", 0.90
    elif div_yield > 3.0:
        return "bullish", 0.75
    elif div_yield > 2.0:
        return "neutral", 0.55
    else:
        return "bearish", 0.40


@simple_agent("Debt Ratio Agent", weight=0.08)
def debt_agent(ticker, context):
    """Analyze debt to equity"""
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
def roe_agent(ticker, context):
    """Return on Equity analysis"""
    roe = context.get_metric("roe", default=0)

    if roe > 20:
        return "bullish", 0.90
    elif roe > 15:
        return "bullish", 0.75
    elif roe > 10:
        return "neutral", 0.55
    else:
        return "bearish", 0.40


@simple_agent("News Sentiment Agent", weight=0.09)
def news_agent(ticker, context):
    """Analyze news sentiment"""
    news = context.get_news(limit=10)

    if not news:
        return "neutral", 0.40

    avg_sentiment = sum(n["sentiment_score"] for n in news) / len(news)

    if avg_sentiment > 0.3:
        return "bullish", 0.70
    elif avg_sentiment > 0:
        return "neutral", 0.55
    else:
        return "bearish", 0.60


@simple_agent("Insider Trading Agent", weight=0.08)
def insider_agent(ticker, context):
    """Analyze insider trading patterns"""
    trades = context.get_insider_trades(limit=15)

    if not trades:
        return "neutral", 0.40

    buys = sum(1 for t in trades if t["transaction_type"] == "buy")
    buy_ratio = buys / len(trades)

    if buy_ratio > 0.7:
        return "bullish", 0.80
    elif buy_ratio > 0.5:
        return "neutral", 0.60
    else:
        return "bearish", 0.65


# ============================================================================
# COMPREHENSIVE FUNDAMENTAL AGENTS
# ============================================================================


@simple_agent("Basic Fundamental Agent", weight=0.20)
def basic_fundamental_agent(ticker, context):
    """Simple 5-factor fundamental check"""
    pe = context.get_metric("pe_ratio", default=999)
    roe = context.get_metric("roe", default=0)
    debt = context.get_metric("debt_to_equity", default=999)
    margin = context.get_metric("profit_margin", default=0)
    dividend = context.get_metric("dividend_yield", default=0)

    score = 0
    if pe < 20:
        score += 1
    if roe > 15:
        score += 1
    if debt < 0.5:
        score += 1
    if margin > 15:
        score += 1
    if dividend > 2:
        score += 1

    if score >= 4:
        return "bullish", 0.90
    elif score >= 3:
        return "bullish", 0.75
    elif score >= 2:
        return "neutral", 0.60
    else:
        return "bearish", 0.70


@simple_agent("Advanced Fundamental Agent", weight=0.25)
def advanced_fundamental_agent(ticker, context):
    """Advanced multi-factor analysis with weighted scoring"""
    from examples.fundamental_agents import (
        _score_valuation,
        _score_profitability,
        _score_financial_health,
        _score_growth_income,
    )

    fund = context.get_fundamentals()

    if not fund:
        return "neutral", 0.40

    # Calculate weighted score
    total_score = (
        _score_valuation(fund) * 0.30
        + _score_profitability(fund) * 0.30
        + _score_financial_health(fund) * 0.25
        + _score_growth_income(fund) * 0.15
    )

    if total_score >= 80:
        return "bullish", 0.95
    elif total_score >= 70:
        return "bullish", 0.85
    elif total_score >= 60:
        return "bullish", 0.75
    elif total_score >= 50:
        return "neutral", 0.65
    else:
        return "bearish", 0.70


@simple_agent("Sector-Specific Fundamental Agent", weight=0.18)
def sector_fundamental_agent(ticker, context):
    """Fundamental analysis adjusted for sector"""
    from examples.fundamental_agents import _get_sector_thresholds

    fund = context.get_fundamentals()

    if not fund:
        return "neutral", 0.40

    sector = fund.get("sector", "Unknown")
    thresholds = _get_sector_thresholds(sector)

    score = 0
    pe = fund.get("pe_ratio", 999)
    roe = fund.get("roe", 0)
    debt = fund.get("debt_to_equity", 999)
    margin = fund.get("profit_margin", 0)

    if pe < thresholds["pe_good"]:
        score += 25
    elif pe < thresholds["pe_fair"]:
        score += 15
    elif pe < thresholds["pe_high"]:
        score += 5

    if roe > thresholds["roe_excellent"]:
        score += 25
    elif roe > thresholds["roe_good"]:
        score += 15

    if debt < thresholds["debt_low"]:
        score += 25
    elif debt < thresholds["debt_acceptable"]:
        score += 15

    if margin > thresholds["margin_high"]:
        score += 25
    elif margin > thresholds["margin_good"]:
        score += 15

    if score >= 75:
        return "bullish", 0.90
    elif score >= 60:
        return "bullish", 0.80
    elif score >= 40:
        return "neutral", 0.65
    else:
        return "bearish", 0.75


@simple_agent("Quality Score Agent", weight=0.22)
def quality_score_agent(ticker, context):
    """Buffett-style quality investing"""
    fund = context.get_fundamentals()

    if not fund:
        return "neutral", 0.40

    quality_score = 0

    # High ROE (30 points)
    roe = fund.get("roe", 0)
    if roe > 25:
        quality_score += 30
    elif roe > 20:
        quality_score += 25
    elif roe > 15:
        quality_score += 18
    elif roe > 10:
        quality_score += 10

    # Strong margins (25 points)
    profit_margin = fund.get("profit_margin", 0)
    operating_margin = fund.get("operating_margin", 0)
    avg_margin = (profit_margin + operating_margin) / 2

    if avg_margin > 25:
        quality_score += 25
    elif avg_margin > 20:
        quality_score += 20
    elif avg_margin > 15:
        quality_score += 13

    # Financial strength (25 points)
    debt = fund.get("debt_to_equity", 999)
    current_ratio = fund.get("current_ratio", 0)

    if debt < 0.3 and current_ratio > 2.0:
        quality_score += 25
    elif debt < 0.5 and current_ratio > 1.5:
        quality_score += 18
    elif debt < 1.0 and current_ratio > 1.0:
        quality_score += 10

    # Fair valuation (20 points)
    pe = fund.get("pe_ratio", 999)
    if pe < 15:
        quality_score += 20
    elif pe < 20:
        quality_score += 15
    elif pe < 25:
        quality_score += 10
    elif pe < 30:
        quality_score += 5

    quality_pct = quality_score

    if quality_pct >= 80:
        return "bullish", 0.95
    elif quality_pct >= 70:
        return "bullish", 0.85
    elif quality_pct >= 60:
        return "bullish", 0.75
    elif quality_pct >= 50:
        return "neutral", 0.65
    else:
        return "bearish", 0.70


# ============================================================================
# REGISTER ALL AGENTS
# ============================================================================


def register_all_agents():
    """
    Register all agents with the global registry

    This function is called at API startup
    """
    registry = get_registry()

    logger.info("Registering agents...")

    # Basic rule-based agents
    registry.register(pe_ratio_agent.agent, weight=0.12, tags=["basic", "valuation"])

    registry.register(dividend_agent.agent, weight=0.10, tags=["basic", "income"])

    registry.register(debt_agent.agent, weight=0.08, tags=["basic", "risk"])

    registry.register(roe_agent.agent, weight=0.11, tags=["basic", "profitability"])

    registry.register(news_agent.agent, weight=0.09, tags=["sentiment", "news"])

    registry.register(insider_agent.agent, weight=0.08, tags=["sentiment", "insider"])

    # Comprehensive fundamental agents
    registry.register(
        basic_fundamental_agent.agent, weight=0.20, tags=["fundamental", "multi-factor"]
    )

    registry.register(
        advanced_fundamental_agent.agent,
        weight=0.25,
        tags=["fundamental", "advanced", "multi-factor"],
    )

    registry.register(
        sector_fundamental_agent.agent,
        weight=0.18,
        tags=["fundamental", "sector-aware"],
    )

    registry.register(
        quality_score_agent.agent, weight=0.22, tags=["fundamental", "quality", "value"]
    )

    # Optional: LLM agents (if available)
    try:
        from agent_builder.llm.factory import get_llm_provider

        llm = get_llm_provider()
        if llm:
            # Import and register LLM agents
            try:
                from examples.llm_agents_with_personas import (
                    fundamental_analyst_llm,
                    value_investor_llm,
                    risk_analyst_llm,
                    dividend_investor_llm,
                    growth_investor_llm,
                )

                registry.register(
                    fundamental_analyst_llm.agent,
                    weight=0.15,
                    tags=["llm", "fundamental", "persona"],
                )

                registry.register(
                    value_investor_llm.agent,
                    weight=0.12,
                    tags=["llm", "value", "persona"],
                )

                registry.register(
                    risk_analyst_llm.agent, weight=0.11, tags=["llm", "risk", "persona"]
                )

                registry.register(
                    dividend_investor_llm.agent,
                    weight=0.10,
                    tags=["llm", "income", "persona"],
                )

                registry.register(
                    growth_investor_llm.agent,
                    weight=0.13,
                    tags=["llm", "growth", "persona"],
                )

                logger.info("✅ LLM agents registered")

            except ImportError:
                logger.info("ℹ️  LLM persona agents not available")

    except ImportError:
        logger.info("ℹ️  LLM not configured")

    # Optional: Sentiment agents (if available)
    try:
        from examples.sentiment_agents import vader_news_agent, hybrid_sentiment_agent

        registry.register(
            vader_news_agent.agent, weight=0.09, tags=["sentiment", "vader", "news"]
        )

        registry.register(
            hybrid_sentiment_agent.agent,
            weight=0.11,
            tags=["sentiment", "hybrid", "news"],
        )

        logger.info("✅ Sentiment agents registered")

    except ImportError:
        logger.info("ℹ️  Sentiment agents not available")

    # Optional: FinBERT agent (if available)
    try:
        from examples.sentiment_agents import finbert_news_agent

        registry.register(
            finbert_news_agent.agent, weight=0.12, tags=["sentiment", "finbert", "news"]
        )

        logger.info("✅ FinBERT agent registered")

    except ImportError:
        logger.info("ℹ️  FinBERT not available")

    # Get final stats
    stats = registry.stats()
    logger.info(f"✅ Total agents registered: {stats['total_agents']}")
    logger.info(f"   Enabled: {stats['enabled_agents']}")
    logger.info(f"   Agent IDs: {', '.join(stats['agent_ids'][:5])}...")

    return registry


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Testing Complete Agent Registration")
    print("=" * 70)

    # Register all agents
    print("\n📝 Registering agents...")
    registry = register_all_agents()

    # Show stats
    print(f"\n📊 Registry Stats:")
    stats = registry.stats()
    print(f"   Total agents: {stats['total_agents']}")
    print(f"   Enabled agents: {stats['enabled_agents']}")

    # List by category
    print(f"\n🏷️  Agents by Category:")

    categories = {
        "basic": "Basic Rule-Based",
        "fundamental": "Comprehensive Fundamental",
        "llm": "LLM-Powered",
        "sentiment": "Sentiment Analysis",
    }

    for tag, name in categories.items():
        agents = registry.get_by_tag(tag)
        if agents:
            print(f"\n   {name} ({len(agents)} agents):")
            for agent in agents:
                meta = registry.get_metadata(agent.name.lower().replace(" ", "_"))
                if meta:
                    print(f"      - {agent.name} (weight: {meta['weight']})")

    # Test execution on sample ticker
    print(f"\n🧪 Testing agent execution on AAPL...")

    test_ticker = "AAPL"
    enabled_agents = registry.get_enabled_agents()

    print(f"\n   Running {len(enabled_agents)} agents...")

    signals = []
    for i, agent in enumerate(enabled_agents[:5], 1):  # Test first 5
        try:
            signal = agent.analyze(test_ticker)
            signals.append(signal)
            print(
                f"   {i}. {signal.agent_name}: {signal.signal_type} ({signal.confidence:.2f})"
            )
        except Exception as e:
            print(f"   {i}. {agent.name}: ❌ {e}")

    # Calculate consensus
    if signals:
        print(f"\n📊 Sample Consensus (first 5 agents):")

        signal_counts = {}
        total_conf = 0

        for sig in signals:
            signal_counts[sig.signal_type] = signal_counts.get(sig.signal_type, 0) + 1
            total_conf += sig.confidence

        majority = max(signal_counts.items(), key=lambda x: x[1])
        avg_conf = total_conf / len(signals)

        print(f"   Consensus: {majority[0]}")
        print(f"   Confidence: {avg_conf:.2%}")
        print(f"   Agreement: {majority[1]}/{len(signals)}")

    print("\n" + "=" * 70)
    print("✅ All agents registered and working!")
    print("=" * 70)

    print("\n💡 To use via API:")
    print("   1. Start API: uvicorn agent_builder.api.main:app --reload")
    print("   2. List agents: curl http://localhost:8000/agents")
    print(
        '   3. Analyze: curl -X POST http://localhost:8000/analyze -d \'{"ticker":"AAPL"}\''
    )
