"""
Sentiment Analysis Agents
Focus on news, analyst opinions, insider trading, and market sentiment
"""

from agent_builder.agents import simple_agent
from agent_builder.repositories.connection import get_db_cursor
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


# =============================================================================
# NEWS SENTIMENT AGENTS
# =============================================================================


@simple_agent("News Sentiment Analyzer", weight=0.12)
def news_sentiment_agent(ticker, context):
    """
    Aggregate news sentiment over 30 days

    Strategy:
    - Positive news = bullish
    - Negative news = bearish
    - Weight by recency and relevance
    """
    news = context.get_news(limit=30)

    if not news:
        return "neutral", 0.5

    # Calculate weighted sentiment
    total_score = 0
    total_weight = 0
    positive_count = 0
    negative_count = 0

    for article in news:
        score = article.get("sentiment_score", 0)
        confidence = article.get("sentiment_confidence", 0.5)
        relevance = article.get("relevance_score", 0.8)
        sentiment = article.get("sentiment", "neutral")

        # Weight by confidence and relevance
        weight = confidence * relevance
        total_score += score * weight
        total_weight += weight

        if sentiment == "positive":
            positive_count += 1
        elif sentiment == "negative":
            negative_count += 1

    if total_weight == 0:
        return "neutral", 0.5

    avg_sentiment = total_score / total_weight
    sentiment_ratio = positive_count / len(news) if news else 0.5

    # Decision based on average sentiment and ratio
    if avg_sentiment > 0.4 and sentiment_ratio > 0.6:
        return "bullish", 0.85
    elif avg_sentiment > 0.2 and sentiment_ratio > 0.5:
        return "bullish", 0.7
    elif avg_sentiment > 0.1:
        return "bullish", 0.6
    elif avg_sentiment < -0.4 and sentiment_ratio < 0.3:
        return "bearish", 0.85
    elif avg_sentiment < -0.2 and sentiment_ratio < 0.4:
        return "bearish", 0.7
    elif avg_sentiment < -0.1:
        return "bearish", 0.6
    else:
        return "neutral", 0.5


@simple_agent("News Momentum Tracker", weight=0.10)
def news_momentum_agent(ticker, context):
    """
    Track changes in news sentiment over time

    Strategy:
    - Improving sentiment = bullish
    - Deteriorating sentiment = bearish
    - Look for sentiment inflection points
    """
    news = context.get_news(limit=30)

    if len(news) < 10:
        return "neutral", 0.5

    # Sort by date
    sorted_news = sorted(news, key=lambda x: x.get("published_at", datetime.now()))

    # Split into recent and older
    recent_news = sorted_news[-10:]
    older_news = sorted_news[-20:-10] if len(sorted_news) >= 20 else sorted_news[:-10]

    # Calculate average sentiment for each period
    recent_sentiment = sum(n.get("sentiment_score", 0) for n in recent_news) / len(
        recent_news
    )
    older_sentiment = (
        sum(n.get("sentiment_score", 0) for n in older_news) / len(older_news)
        if older_news
        else 0
    )

    # Calculate momentum
    sentiment_change = recent_sentiment - older_sentiment

    # Decision
    if sentiment_change > 0.3:
        return "bullish", 0.85  # Strong positive momentum
    elif sentiment_change > 0.15:
        return "bullish", 0.7  # Moderate positive momentum
    elif sentiment_change > 0.05:
        return "bullish", 0.6  # Slight improvement
    elif sentiment_change < -0.3:
        return "bearish", 0.85  # Strong negative momentum
    elif sentiment_change < -0.15:
        return "bearish", 0.7  # Moderate negative momentum
    elif sentiment_change < -0.05:
        return "bearish", 0.6  # Slight deterioration
    else:
        return "neutral", 0.5


@simple_agent("News Category Analyzer", weight=0.09)
def news_category_agent(ticker, context):
    """
    Analyze sentiment by news category

    Strategy:
    - Earnings news is most important
    - Product news indicates innovation
    - Regulatory news is risk factor
    """
    news = context.get_news(limit=30)

    if not news:
        return "neutral", 0.5

    # Categorize news
    category_sentiment = {}
    category_counts = {}

    for article in news:
        category = article.get("category", "market")
        sentiment_score = article.get("sentiment_score", 0)

        if category not in category_sentiment:
            category_sentiment[category] = []
            category_counts[category] = 0

        category_sentiment[category].append(sentiment_score)
        category_counts[category] += 1

    # Calculate weighted score (earnings news weighted higher)
    weights = {
        "earnings": 3.0,
        "product": 2.0,
        "leadership": 1.5,
        "regulatory": 2.0,
        "market": 1.0,
    }

    total_score = 0
    total_weight = 0

    for category, scores in category_sentiment.items():
        avg_score = sum(scores) / len(scores)
        weight = weights.get(category, 1.0)
        total_score += avg_score * weight * len(scores)
        total_weight += weight * len(scores)

    if total_weight == 0:
        return "neutral", 0.5

    weighted_sentiment = total_score / total_weight

    # Decision
    if weighted_sentiment > 0.4:
        return "bullish", 0.8
    elif weighted_sentiment > 0.2:
        return "bullish", 0.7
    elif weighted_sentiment > 0:
        return "neutral", 0.55
    elif weighted_sentiment < -0.4:
        return "bearish", 0.8
    elif weighted_sentiment < -0.2:
        return "bearish", 0.7
    else:
        return "neutral", 0.5


# =============================================================================
# ANALYST RATING AGENTS
# =============================================================================


@simple_agent("Analyst Consensus", weight=0.12)
def analyst_consensus_agent(ticker, context):
    """
    Aggregate analyst ratings and price targets

    Strategy:
    - Majority buy = bullish
    - High price target upside = bullish
    - Recent upgrades = bullish
    """
    ratings = context.get_analyst_ratings(limit=20)

    if not ratings:
        return "neutral", 0.5

    # Count ratings
    buy_count = 0
    hold_count = 0
    sell_count = 0
    price_targets = []

    for rating in ratings:
        rating_type = rating.get("rating", "hold")
        price_target = rating.get("price_target", 0)

        if rating_type in ["strong buy", "buy"]:
            buy_count += 1
        elif rating_type == "hold":
            hold_count += 1
        elif rating_type in ["sell", "strong sell"]:
            sell_count += 1

        if price_target > 0:
            price_targets.append(price_target)

    total_ratings = len(ratings)
    if total_ratings == 0:
        return "neutral", 0.5

    # Calculate consensus
    buy_ratio = buy_count / total_ratings
    sell_ratio = sell_count / total_ratings

    # Calculate price target upside
    if price_targets:
        avg_target = sum(price_targets) / len(price_targets)
        current_price = context.get_latest_price()
        if current_price > 0:
            upside = ((avg_target - current_price) / current_price) * 100
        else:
            upside = 0
    else:
        upside = 0

    # Decision
    score = 0

    # Rating consensus
    if buy_ratio > 0.7:
        score += 3
    elif buy_ratio > 0.5:
        score += 2
    elif buy_ratio > 0.4:
        score += 1

    if sell_ratio > 0.3:
        score -= 2
    elif sell_ratio > 0.2:
        score -= 1

    # Price target upside
    if upside > 20:
        score += 3
    elif upside > 10:
        score += 2
    elif upside > 5:
        score += 1
    elif upside < -10:
        score -= 2
    elif upside < -5:
        score -= 1

    # Final decision
    if score >= 5:
        return "bullish", 0.9
    elif score >= 3:
        return "bullish", 0.75
    elif score >= 1:
        return "bullish", 0.6
    elif score <= -3:
        return "bearish", 0.8
    elif score <= -1:
        return "bearish", 0.65
    else:
        return "neutral", 0.5


@simple_agent("Analyst Momentum", weight=0.10)
def analyst_momentum_agent(ticker, context):
    """
    Track recent changes in analyst ratings

    Strategy:
    - Recent upgrades = bullish
    - Recent downgrades = bearish
    - Multiple upgrades = very bullish
    """
    ratings = context.get_analyst_ratings(limit=20)

    if not ratings:
        return "neutral", 0.5

    # Count rating changes in last 30 days
    recent_cutoff = datetime.now() - timedelta(days=30)
    upgrades = 0
    downgrades = 0
    maintains = 0

    for rating in ratings:
        rating_date = rating.get("rating_date", datetime.now())
        rating_change = rating.get("rating_change")

        # Only count recent changes
        if isinstance(rating_date, str):
            rating_date = datetime.fromisoformat(rating_date.replace("Z", "+00:00"))

        if rating_date > recent_cutoff:
            if rating_change == "upgrade":
                upgrades += 1
            elif rating_change == "downgrade":
                downgrades += 1
            elif rating_change == "maintain":
                maintains += 1

    total_changes = upgrades + downgrades

    if total_changes == 0:
        return "neutral", 0.5

    # Calculate momentum
    if upgrades >= 3 and upgrades > downgrades * 2:
        return "bullish", 0.85
    elif upgrades >= 2 and upgrades > downgrades:
        return "bullish", 0.75
    elif upgrades > downgrades:
        return "bullish", 0.65
    elif downgrades >= 3 and downgrades > upgrades * 2:
        return "bearish", 0.85
    elif downgrades >= 2 and downgrades > upgrades:
        return "bearish", 0.75
    elif downgrades > upgrades:
        return "bearish", 0.65
    else:
        return "neutral", 0.5


@simple_agent("Price Target Analyzer", weight=0.09)
def price_target_agent(ticker, context):
    """
    Analyze analyst price target distribution

    Strategy:
    - Consensus upside > 15% = bullish
    - Wide price target range = uncertainty
    - Rising price targets = bullish
    """
    ratings = context.get_analyst_ratings(limit=20)

    if not ratings:
        return "neutral", 0.5

    price_targets = []
    previous_targets = []

    for rating in ratings:
        current_target = rating.get("price_target", 0)
        previous_target = rating.get("previous_price_target", 0)

        if current_target > 0:
            price_targets.append(current_target)

        if previous_target > 0 and current_target > 0:
            previous_targets.append((previous_target, current_target))

    if not price_targets:
        return "neutral", 0.5

    # Calculate statistics
    avg_target = sum(price_targets) / len(price_targets)
    max_target = max(price_targets)
    min_target = min(price_targets)
    target_range = max_target - min_target

    current_price = context.get_latest_price()
    if current_price <= 0:
        return "neutral", 0.5

    # Upside potential
    upside = ((avg_target - current_price) / current_price) * 100

    # Price target revisions
    targets_raised = sum(1 for prev, curr in previous_targets if curr > prev)
    targets_lowered = sum(1 for prev, curr in previous_targets if curr < prev)

    score = 0

    # Upside potential
    if upside > 20:
        score += 3
    elif upside > 15:
        score += 2
    elif upside > 10:
        score += 1
    elif upside < -10:
        score -= 2
    elif upside < -5:
        score -= 1

    # Price target momentum
    if targets_raised > targets_lowered * 1.5:
        score += 2
    elif targets_raised > targets_lowered:
        score += 1
    elif targets_lowered > targets_raised * 1.5:
        score -= 2
    elif targets_lowered > targets_raised:
        score -= 1

    # Uncertainty (wide range is negative)
    range_pct = (target_range / avg_target) * 100 if avg_target > 0 else 0
    if range_pct > 40:
        score -= 1  # High uncertainty

    # Decision
    if score >= 4:
        return "bullish", 0.85
    elif score >= 2:
        return "bullish", 0.7
    elif score >= 1:
        return "bullish", 0.6
    elif score <= -3:
        return "bearish", 0.8
    elif score <= -1:
        return "bearish", 0.65
    else:
        return "neutral", 0.5


# =============================================================================
# INSIDER TRADING AGENTS
# =============================================================================


@simple_agent("Insider Trading Activity", weight=0.11)
def insider_trading_agent(ticker, context):
    """
    Follow the smart money - insider trading

    Strategy:
    - Executive buying = very bullish
    - Heavy insider buying = bullish
    - Heavy insider selling = bearish
    - C-suite trades weighted higher
    """
    trades = context.get_insider_trades(limit=20)

    if not trades:
        return "neutral", 0.5

    buy_value = 0
    sell_value = 0
    exec_buys = 0
    exec_sells = 0

    # Executive titles have higher weight
    exec_titles = ["CEO", "CFO", "COO", "President"]

    for trade in trades:
        transaction_type = trade.get("transaction_type", "")
        transaction_value = trade.get("transaction_value", 0)
        insider_title = trade.get("insider_title", "")

        # Weight executive trades higher
        weight = 2.0 if insider_title in exec_titles else 1.0

        if transaction_type == "buy":
            buy_value += transaction_value * weight
            if insider_title in exec_titles:
                exec_buys += 1
        elif transaction_type == "sell":
            sell_value += transaction_value * weight
            if insider_title in exec_titles:
                exec_sells += 1

    total_value = buy_value + sell_value

    if total_value == 0:
        return "neutral", 0.5

    # Calculate buy ratio
    buy_ratio = buy_value / total_value

    # Decision
    if exec_buys >= 2 and buy_ratio > 0.7:
        return "bullish", 0.9  # Multiple executive buys
    elif exec_buys >= 1 and buy_ratio > 0.6:
        return "bullish", 0.8  # Executive buying
    elif buy_ratio > 0.7:
        return "bullish", 0.75  # Heavy buying
    elif buy_ratio > 0.6:
        return "bullish", 0.65  # More buying than selling
    elif buy_ratio < 0.3:
        return "bearish", 0.75  # Heavy selling
    elif buy_ratio < 0.4:
        return "bearish", 0.65  # More selling than buying
    else:
        return "neutral", 0.5


@simple_agent("Insider Transaction Timing", weight=0.09)
def insider_timing_agent(ticker, context):
    """
    Analyze timing of insider trades

    Strategy:
    - Recent insider buying = bullish
    - Buying after price drop = very bullish (buy the dip)
    - Clustered buying = strong signal
    """
    trades = context.get_insider_trades(limit=20)
    prices = context.get_price_data(days=90)

    if not trades or not prices:
        return "neutral", 0.5

    # Get recent trades (last 30 days)
    recent_cutoff = datetime.now() - timedelta(days=30)
    recent_buys = 0
    recent_sells = 0

    for trade in trades:
        trade_date = trade.get("transaction_date", datetime.now())
        transaction_type = trade.get("transaction_type", "")

        if isinstance(trade_date, str):
            trade_date = datetime.fromisoformat(trade_date.replace("Z", "+00:00"))

        if trade_date > recent_cutoff:
            if transaction_type == "buy":
                recent_buys += 1
            elif transaction_type == "sell":
                recent_sells += 1

    # Check if buying after price decline
    if len(prices) >= 30:
        recent_prices = [p["close"] for p in prices[:30]]
        older_prices = (
            [p["close"] for p in prices[30:60]] if len(prices) >= 60 else recent_prices
        )

        recent_avg = sum(recent_prices) / len(recent_prices)
        older_avg = sum(older_prices) / len(older_prices)

        price_decline = (
            ((recent_avg - older_avg) / older_avg) * 100 if older_avg > 0 else 0
        )
    else:
        price_decline = 0

    # Decision
    score = 0

    # Recent buying activity
    if recent_buys >= 3:
        score += 3
    elif recent_buys >= 2:
        score += 2
    elif recent_buys >= 1:
        score += 1

    # Buying the dip
    if recent_buys > 0 and price_decline < -10:
        score += 2  # Strong signal
    elif recent_buys > 0 and price_decline < -5:
        score += 1

    # Selling activity
    if recent_sells >= 3:
        score -= 2
    elif recent_sells >= 2:
        score -= 1

    # Final decision
    if score >= 4:
        return "bullish", 0.85
    elif score >= 2:
        return "bullish", 0.7
    elif score >= 1:
        return "bullish", 0.6
    elif score <= -2:
        return "bearish", 0.7
    else:
        return "neutral", 0.5


@simple_agent("Insider Conviction Level", weight=0.08)
def insider_conviction_agent(ticker, context):
    """
    Measure insider conviction by transaction size

    Strategy:
    - Large transactions = high conviction
    - Multiple insiders buying = high conviction
    - Small sales don't matter (could be for taxes/expenses)
    """
    trades = context.get_insider_trades(limit=20)

    if not trades:
        return "neutral", 0.5

    # Analyze transaction sizes
    large_buys = 0
    large_sells = 0
    buy_count = 0
    sell_count = 0
    unique_buyers = set()

    for trade in trades:
        transaction_type = trade.get("transaction_type", "")
        transaction_value = trade.get("transaction_value", 0)
        insider_name = trade.get("insider_name", "")

        # Large transaction threshold: $500k+
        is_large = transaction_value >= 500000

        if transaction_type == "buy":
            buy_count += 1
            if is_large:
                large_buys += 1
            unique_buyers.add(insider_name)
        elif transaction_type == "sell":
            sell_count += 1
            if is_large:
                large_sells += 1

    # Multiple insiders buying = strong signal
    multiple_insiders = len(unique_buyers) >= 3

    # Decision
    if large_buys >= 2 or (large_buys >= 1 and multiple_insiders):
        return "bullish", 0.85  # High conviction buying
    elif large_buys >= 1:
        return "bullish", 0.75
    elif buy_count >= 3 and multiple_insiders:
        return "bullish", 0.7  # Multiple smaller buys
    elif large_sells >= 3:
        return "bearish", 0.7  # Significant selling
    elif large_sells >= 2:
        return "bearish", 0.6
    else:
        return "neutral", 0.5


# =============================================================================
# COMBINED SENTIMENT AGENTS
# =============================================================================


@simple_agent("Sentiment Divergence Detector", weight=0.10)
def sentiment_divergence_agent(ticker, context):
    """
    Detect divergences between different sentiment sources

    Strategy:
    - News positive + Analysts negative = investigate
    - Insiders buying + News negative = contrarian opportunity
    - All aligned = strong signal
    """
    # Get sentiment from different sources
    news = context.get_news(limit=20)
    ratings = context.get_analyst_ratings(limit=15)
    trades = context.get_insider_trades(limit=15)

    # Calculate news sentiment
    news_score = 0
    if news:
        news_score = sum(n.get("sentiment_score", 0) for n in news) / len(news)

    # Calculate analyst sentiment
    analyst_score = 0
    if ratings:
        buy_count = sum(
            1 for r in ratings if r.get("rating", "") in ["strong buy", "buy"]
        )
        sell_count = sum(
            1 for r in ratings if r.get("rating", "") in ["sell", "strong sell"]
        )
        analyst_score = (buy_count - sell_count) / len(ratings)

    # Calculate insider sentiment
    insider_score = 0
    if trades:
        buy_value = sum(
            t.get("transaction_value", 0)
            for t in trades
            if t.get("transaction_type") == "buy"
        )
        sell_value = sum(
            t.get("transaction_value", 0)
            for t in trades
            if t.get("transaction_type") == "sell"
        )
        total_value = buy_value + sell_value
        if total_value > 0:
            insider_score = (buy_value - sell_value) / total_value

    # Check for alignment or divergence
    scores = [news_score, analyst_score, insider_score]
    avg_score = sum(scores) / 3

    # All positive
    if all(s > 0.2 for s in scores):
        return "bullish", 0.85

    # All negative
    if all(s < -0.2 for s in scores):
        return "bearish", 0.85

    # Contrarian: Insiders buying while news is negative
    if insider_score > 0.3 and news_score < -0.2:
        return "bullish", 0.75  # Smart money disagrees with market

    # Mixed signals
    if avg_score > 0.2:
        return "bullish", 0.65
    elif avg_score < -0.2:
        return "bearish", 0.65
    else:
        return "neutral", 0.5


@simple_agent("Market Sentiment Aggregator", weight=0.11)
def market_sentiment_aggregator_agent(ticker, context):
    """
    Aggregate all sentiment signals with optimal weighting

    Strategy:
    - Combine news, analysts, and insiders
    - Weight by reliability and recency
    - Detect extreme sentiment (contrarian indicator)
    """
    news = context.get_news(limit=25)
    ratings = context.get_analyst_ratings(limit=20)
    trades = context.get_insider_trades(limit=20)

    total_score = 0
    total_weight = 0

    # News sentiment (30% weight)
    if news:
        recent_news = [
            n
            for n in news
            if (datetime.now() - n.get("published_at", datetime.now())).days <= 14
        ]
        if recent_news:
            news_sentiment = sum(
                n.get("sentiment_score", 0) * n.get("relevance_score", 1.0)
                for n in recent_news
            ) / len(recent_news)
            total_score += news_sentiment * 0.3
            total_weight += 0.3

    # Analyst sentiment (35% weight)
    if ratings:
        buy_ratio = sum(
            1 for r in ratings if r.get("rating", "") in ["strong buy", "buy"]
        ) / len(ratings)
        sell_ratio = sum(
            1 for r in ratings if r.get("rating", "") in ["sell", "strong sell"]
        ) / len(ratings)
        analyst_sentiment = buy_ratio - sell_ratio  # Range: -1 to 1
        total_score += analyst_sentiment * 0.35
        total_weight += 0.35

    # Insider sentiment (35% weight)
    if trades:
        buy_value = sum(
            t.get("transaction_value", 0)
            for t in trades
            if t.get("transaction_type") == "buy"
        )
        sell_value = sum(
            t.get("transaction_value", 0)
            for t in trades
            if t.get("transaction_type") == "sell"
        )
        total_value = buy_value + sell_value
        if total_value > 0:
            insider_sentiment = (buy_value - sell_value) / total_value
            total_score += insider_sentiment * 0.35
            total_weight += 0.35

    if total_weight == 0:
        return "neutral", 0.5

    # Normalized aggregate score
    aggregate_score = total_score / total_weight

    # Decision with confidence scaling
    if aggregate_score > 0.5:
        return "bullish", 0.9
    elif aggregate_score > 0.3:
        return "bullish", 0.8
    elif aggregate_score > 0.15:
        return "bullish", 0.7
    elif aggregate_score > 0.05:
        return "bullish", 0.6
    elif aggregate_score < -0.5:
        return "bearish", 0.9
    elif aggregate_score < -0.3:
        return "bearish", 0.8
    elif aggregate_score < -0.15:
        return "bearish", 0.7
    elif aggregate_score < -0.05:
        return "bearish", 0.6
    else:
        return "neutral", 0.5


# =============================================================================
# REGISTRATION
# =============================================================================


def register_sentiment_agents():
    """Register all sentiment agents"""
    from agent_builder.agents.registry import get_registry

    registry = get_registry()

    # News sentiment agents
    registry.register(news_sentiment_agent.agent, tags=["sentiment", "news"])
    registry.register(news_momentum_agent.agent, tags=["sentiment", "news"])
    registry.register(news_category_agent.agent, tags=["sentiment", "news"])

    # Analyst rating agents
    registry.register(analyst_consensus_agent.agent, tags=["sentiment", "analysts"])
    registry.register(analyst_momentum_agent.agent, tags=["sentiment", "analysts"])
    registry.register(price_target_agent.agent, tags=["sentiment", "analysts"])

    # Insider trading agents
    registry.register(insider_trading_agent.agent, tags=["sentiment", "insiders"])
    registry.register(insider_timing_agent.agent, tags=["sentiment", "insiders"])
    registry.register(insider_conviction_agent.agent, tags=["sentiment", "insiders"])

    # Combined sentiment agents
    registry.register(sentiment_divergence_agent.agent, tags=["sentiment", "combined"])
    registry.register(
        market_sentiment_aggregator_agent.agent, tags=["sentiment", "combined"]
    )

    logger.info("✅ Registered 11 sentiment agents")


if __name__ == "__main__":
    # Test agents
    from agent_builder.agents.context import AgentContext

    context = AgentContext("AAPL")

    print("Testing sentiment agents on AAPL:")
    print("-" * 60)

    agents = [
        news_sentiment_agent,
        analyst_consensus_agent,
        insider_trading_agent,
        market_sentiment_aggregator_agent,
    ]

    for agent_func in agents:
        signal, confidence = agent_func("AAPL", context)
        print(f"{agent_func.__name__:35s} {signal:8s} ({confidence:.2f})")
