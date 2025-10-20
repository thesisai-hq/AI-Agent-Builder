"""
Production-Ready Agent Suite
Complete implementation of all agent types
"""

from agent_builder import agent, get_registry
from agent_builder.llm import get_llm_provider, PromptTemplates
from agent_builder.rag import RAGEngine

# from agent_builder.utils.indicators import TechnicalIndicators, get_technical_signal


# ============================================================================
# FUNDAMENTAL AGENTS
# ============================================================================


@agent("Value Investor", "Graham-style deep value analysis")
def value_investor(ticker, context):
    """
    Benjamin Graham value investing approach

    Criteria:
    - Low P/E (< 15)
    - Strong balance sheet (Debt/Equity < 1.0)
    - Positive earnings growth
    - Dividend paying
    """
    pe = context.get_fundamental("pe_ratio", 25)
    debt_eq = context.get_fundamental("debt_to_equity", 2.0)
    growth = context.get_fundamental("revenue_growth", 0)
    div_yield = context.get_fundamental("dividend_yield", 0)

    score = 0
    reasons = []

    if pe < 15:
        score += 2
        reasons.append(f"Attractive P/E of {pe:.1f}")
    elif pe > 25:
        score -= 1
        reasons.append(f"High P/E of {pe:.1f}")

    if debt_eq < 1.0:
        score += 1
        reasons.append(f"Healthy debt ratio {debt_eq:.2f}")

    if growth > 10:
        score += 1
        reasons.append(f"Strong growth {growth:.1f}%")

    if div_yield > 2:
        score += 1
        reasons.append(f"Good dividend {div_yield:.1f}%")

    if score >= 3:
        return "bullish", 0.8, "; ".join(reasons)
    elif score <= -1:
        return "bearish", 0.7, "; ".join(reasons)
    else:
        return "neutral", 0.5, "; ".join(reasons) if reasons else "Mixed fundamentals"


@agent("Growth Investor", "High-growth momentum strategy")
def growth_investor(ticker, context):
    """
    Growth investing - focus on revenue/earnings growth
    """
    rev_growth = context.get_fundamental("revenue_growth", 0)
    earn_growth = context.get_fundamental("earnings_growth", 0)
    roe = context.get_fundamental("roe", 0)
    margin = context.get_fundamental("profit_margin", 0)

    score = 0
    reasons = []

    if rev_growth > 20:
        score += 2
        reasons.append(f"Excellent revenue growth {rev_growth:.1f}%")
    elif rev_growth > 10:
        score += 1
        reasons.append(f"Good revenue growth {rev_growth:.1f}%")

    if earn_growth > 15:
        score += 1
        reasons.append(f"Strong earnings growth {earn_growth:.1f}%")

    if roe > 15:
        score += 1
        reasons.append(f"High ROE {roe:.1f}%")

    if margin > 20:
        score += 1
        reasons.append(f"Excellent margins {margin:.1f}%")

    confidence = min(0.9, 0.5 + (score * 0.1))

    if score >= 3:
        return "bullish", confidence, "; ".join(reasons)
    elif score == 0:
        return "bearish", 0.6, "Weak growth profile"
    else:
        return "neutral", confidence, "; ".join(reasons)


@agent("Quality Investor", "Buffett-style quality focus")
def quality_investor(ticker, context):
    """
    Quality investing - strong competitive moats
    """
    roe = context.get_fundamental("roe", 0)
    roic = context.get_fundamental("roic", 0)
    margin = context.get_fundamental("profit_margin", 0)
    debt_eq = context.get_fundamental("debt_to_equity", 2.0)

    # High quality thresholds
    is_quality = roe > 15 and roic > 12 and margin > 15 and debt_eq < 0.5

    if is_quality:
        return (
            "bullish",
            0.85,
            f"High quality business: ROE {roe:.1f}%, ROIC {roic:.1f}%, Margins {margin:.1f}%",
        )
    elif roe < 8 or margin < 5:
        return "bearish", 0.7, "Low quality metrics"
    else:
        return "neutral", 0.6, "Average quality"


# ============================================================================
# TECHNICAL AGENTS
# ============================================================================


@agent("Trend Follower", "Moving average trend analysis")
def trend_follower(ticker, context):
    """
    Follow the trend using moving averages
    """
    prices = context.get_price_data(days=10)
    if not prices:
        return "neutral", 0.3, "No price data"

    latest = prices[0]
    current = latest["close"]
    sma_20 = latest.get("sma_20", current)
    sma_50 = latest.get("sma_50", current)
    sma_200 = latest.get("sma_200", current)

    # Strong uptrend: price > sma_20 > sma_50 > sma_200
    if current > sma_20 > sma_50 > sma_200:
        pct_above = ((current - sma_200) / sma_200) * 100
        return "bullish", 0.85, f"Strong uptrend: {pct_above:.1f}% above 200-day MA"

    # Strong downtrend: price < sma_20 < sma_50 < sma_200
    elif current < sma_20 < sma_50 < sma_200:
        pct_below = ((sma_200 - current) / sma_200) * 100
        return "bearish", 0.85, f"Strong downtrend: {pct_below:.1f}% below 200-day MA"

    # Mixed signals
    else:
        return "neutral", 0.5, "Mixed trend signals"


@agent("Momentum Trader", "RSI and momentum analysis")
def momentum_trader(ticker, context):
    """
    Momentum-based trading using RSI
    """
    prices = context.get_price_data(days=20)
    if not prices:
        return "neutral", 0.3, "No price data"

    latest = prices[0]
    rsi = latest.get("rsi_14", 50)
    current = latest["close"]

    # Get price change
    if len(prices) > 10:
        past = prices[10]["close"]
        pct_change = ((current - past) / past) * 100
    else:
        pct_change = 0

    # Oversold + momentum
    if rsi < 30 and pct_change > -5:
        return "bullish", 0.8, f"Oversold (RSI {rsi:.1f}) with stabilizing price"

    # Overbought + momentum
    elif rsi > 70 and pct_change > 10:
        return "bearish", 0.75, f"Overbought (RSI {rsi:.1f}) after strong rally"

    # Strong momentum
    elif 40 < rsi < 60 and pct_change > 15:
        return "bullish", 0.7, f"Strong momentum: +{pct_change:.1f}% with healthy RSI"

    else:
        return "neutral", 0.5, f"RSI {rsi:.1f}, moderate momentum"


# ============================================================================
# SENTIMENT AGENTS
# ============================================================================


@agent("News Sentiment Analyst", "Analyzes news sentiment")
def news_sentiment(ticker, context):
    """
    Aggregate news sentiment analysis
    """
    news = context.get_news(limit=10)
    if not news:
        return "neutral", 0.3, "No news available"

    # Calculate average sentiment
    sentiments = [n.get("sentiment_score", 0) for n in news]
    avg_sentiment = sum(sentiments) / len(sentiments)

    # Count positive/negative
    positive = sum(1 for s in sentiments if s > 0.3)
    negative = sum(1 for s in sentiments if s < -0.3)

    if avg_sentiment > 0.4 and positive > negative:
        return (
            "bullish",
            0.75,
            f"Positive sentiment {avg_sentiment:.2f} across {len(news)} articles ({positive} positive)",
        )
    elif avg_sentiment < -0.4 and negative > positive:
        return (
            "bearish",
            0.75,
            f"Negative sentiment {avg_sentiment:.2f} across {len(news)} articles ({negative} negative)",
        )
    else:
        return "neutral", 0.5, f"Mixed sentiment {avg_sentiment:.2f}"


@agent("Analyst Consensus", "Tracks analyst ratings")
def analyst_consensus(ticker, context):
    """
    Aggregate analyst recommendations
    """
    ratings = context.get_analyst_ratings(limit=10)
    if not ratings:
        return "neutral", 0.3, "No analyst ratings"

    # Count ratings
    buy_count = sum(
        1
        for r in ratings
        if "buy" in r.get("rating", "").lower()
        or "overweight" in r.get("rating", "").lower()
    )
    sell_count = sum(
        1
        for r in ratings
        if "sell" in r.get("rating", "").lower()
        or "underweight" in r.get("rating", "").lower()
    )

    total = len(ratings)
    buy_pct = buy_count / total

    # Recent upgrades
    recent_upgrades = sum(
        1 for r in ratings[:5] if "buy" in r.get("rating", "").lower()
    )

    if buy_pct > 0.6 and recent_upgrades >= 2:
        return "bullish", 0.8, f"{buy_count}/{total} analysts rate Buy/Overweight"
    elif sell_count > buy_count:
        return "bearish", 0.7, f"{sell_count}/{total} analysts rate Sell/Underweight"
    else:
        return "neutral", 0.6, f"Mixed ratings: {buy_count} buy, {sell_count} sell"


# ============================================================================
# RISK AGENTS
# ============================================================================


@agent("Volatility Risk Manager", "Assesses volatility risk")
def volatility_risk(ticker, context):
    """
    Risk assessment based on volatility and options
    """
    # Get options data for implied volatility
    options = context.get_options_data()

    if options and (options.get("calls") or options.get("puts")):
        # Average implied volatility
        all_options = (options.get("calls", []) or []) + (options.get("puts", []) or [])
        if all_options:
            avg_iv = sum(o.get("implied_volatility", 0) for o in all_options) / len(
                all_options
            )

            if avg_iv < 20:
                return (
                    "bullish",
                    0.7,
                    f"Low volatility ({avg_iv:.1f}%) suggests stability",
                )
            elif avg_iv > 40:
                return "bearish", 0.75, f"High volatility ({avg_iv:.1f}%) suggests risk"
            else:
                return "neutral", 0.6, f"Moderate volatility ({avg_iv:.1f}%)"

    # Fallback to price volatility
    prices = context.get_price_data(days=30)
    if prices:
        price_changes = []
        for i in range(min(20, len(prices) - 1)):
            change = abs(
                (prices[i]["close"] - prices[i + 1]["close"]) / prices[i + 1]["close"]
            )
            price_changes.append(change)

        if price_changes:
            avg_change = sum(price_changes) / len(price_changes)
            if avg_change < 0.01:  # <1% average daily change
                return "neutral", 0.6, "Low historical volatility"
            elif avg_change > 0.03:  # >3% average daily change
                return "bearish", 0.7, "High historical volatility suggests risk"

    return "neutral", 0.5, "Unable to assess volatility risk"


@agent("Insider Activity Monitor", "Tracks insider trading")
def insider_activity(ticker, context):
    """
    Analyze insider trading patterns
    """
    trades = context.get_insider_trades(limit=15)
    if not trades:
        return "neutral", 0.3, "No insider trading data"

    # Analyze recent trades (last 5)
    recent_trades = trades[:5]
    buys = sum(1 for t in recent_trades if t.get("transaction_type") == "Purchase")
    sells = sum(1 for t in recent_trades if t.get("transaction_type") == "Sale")

    # Calculate total value
    buy_value = sum(
        t.get("total_value", 0)
        for t in recent_trades
        if t.get("transaction_type") == "Purchase"
    )
    sell_value = sum(
        t.get("total_value", 0)
        for t in recent_trades
        if t.get("transaction_type") == "Sale"
    )

    if buys > sells and buy_value > sell_value * 2:
        return (
            "bullish",
            0.75,
            f"Strong insider buying: {buys} purchases totaling ${buy_value:,.0f}",
        )
    elif sells > buys * 2:
        return "bearish", 0.65, f"Heavy insider selling: {sells} sales"
    else:
        return "neutral", 0.5, "Balanced insider activity"


# ============================================================================
# MACRO AGENTS
# ============================================================================


@agent("Macro Economic Analyst", "Analyzes economic indicators")
def macro_analyst(ticker, context):
    """
    Macro economic environment analysis
    """
    indicators = context.get_macro_indicators()
    if not indicators:
        return "neutral", 0.3, "No macro data"

    # Build macro context
    macro_factors = {}
    for ind in indicators:
        name = ind.get("indicator_name", "")
        value = ind.get("value", 0)
        prev = ind.get("previous_value", 0)

        if "Rate" in name or "rate" in name:
            macro_factors[name] = {"value": value, "prev": prev, "change": value - prev}

    reasons = []
    bullish_factors = 0
    bearish_factors = 0

    # Check key indicators
    for name, data in macro_factors.items():
        if "Federal Funds Rate" in name or "FFR" in name:
            if data["value"] > 4.0:
                bearish_factors += 1
                reasons.append(f"High Fed rate ({data['value']:.2f}%)")
            elif data["change"] < 0:
                bullish_factors += 1
                reasons.append("Fed cutting rates")

        elif "CPI" in name or "Inflation" in name:
            if data["value"] > 3.0:
                bearish_factors += 1
                reasons.append(f"Elevated inflation ({data['value']:.1f}%)")
            elif data["value"] < 2.5:
                bullish_factors += 1
                reasons.append("Inflation under control")

        elif "GDP" in name:
            if data["value"] > 2.5:
                bullish_factors += 1
                reasons.append(f"Strong GDP growth ({data['value']:.1f}%)")
            elif data["value"] < 1.0:
                bearish_factors += 1
                reasons.append("Weak GDP growth")

        elif "Unemployment" in name:
            if data["value"] < 4.0:
                bullish_factors += 1
                reasons.append("Low unemployment")
            elif data["value"] > 5.0:
                bearish_factors += 1
                reasons.append("Rising unemployment")

    reasoning = "; ".join(reasons) if reasons else "Limited macro data"

    if bullish_factors > bearish_factors:
        return "bullish", 0.7, f"Favorable macro: {reasoning}"
    elif bearish_factors > bullish_factors:
        return "bearish", 0.7, f"Challenging macro: {reasoning}"
    else:
        return "neutral", 0.5, f"Mixed macro signals: {reasoning}"


@agent("Market Regime Detector", "Identifies market conditions")
def market_regime(ticker, context):
    """
    Detect market regime (bull, bear, sideways)
    """
    indicators = context.get_macro_indicators()

    # Check VIX for fear
    vix = None
    for ind in indicators:
        if "VIX" in ind.get("indicator_name", ""):
            vix = ind.get("value", 0)
            break

    if vix:
        if vix < 15:
            return "bullish", 0.75, f"Low fear (VIX {vix:.1f}) - bull market regime"
        elif vix > 30:
            return "bearish", 0.8, f"High fear (VIX {vix:.1f}) - bear market regime"
        else:
            return "neutral", 0.6, f"Moderate volatility (VIX {vix:.1f})"

    return "neutral", 0.5, "Unable to determine market regime"


# ============================================================================
# LLM-POWERED AGENTS
# ============================================================================


@agent("AI Fundamental Analyst", "LLM-powered fundamental analysis")
def ai_fundamental_analyst(ticker, context):
    """
    Use LLM to analyze fundamentals comprehensively
    """
    llm = get_llm_provider("ollama")
    if not llm or not llm.is_available():
        return "neutral", 0.3, "LLM not available"

    fundamentals = context.get_fundamentals()
    if not fundamentals:
        return "neutral", 0.3, "No fundamental data"

    prompt = PromptTemplates.fundamental_analysis(ticker, fundamentals)
    system = PromptTemplates.FUNDAMENTAL_ANALYST

    try:
        response = llm.generate(prompt, system, temperature=0.3, max_tokens=500)
        parsed = PromptTemplates.parse_llm_response(response.content)
        return parsed["signal"], parsed["confidence"], parsed["reasoning"]
    except Exception as e:
        return "neutral", 0.4, f"LLM analysis failed: {str(e)}"


@agent("AI SEC Filing Analyst", "RAG-powered SEC analysis")
def ai_sec_analyst(ticker, context):
    """
    Use RAG to analyze SEC filings with LLM
    """
    llm = get_llm_provider("ollama")
    if not llm or not llm.is_available():
        return "neutral", 0.3, "LLM not available"

    # Create RAG engine
    rag = RAGEngine(
        db=context.db, embedding="sentence-transformers", vectorstore="faiss"
    )

    try:
        # Index and search
        rag.index_sec_filings(ticker)
        results = rag.search_sec_filings(
            query="financial performance, growth outlook, and key risks",
            ticker=ticker,
            top_k=3,
        )

        if not results:
            return "neutral", 0.3, "No SEC filing data"

        # Build context
        context_text = "\n\n".join(
            [f"[Excerpt {i+1}] {r['text']}" for i, r in enumerate(results)]
        )

        # Analyze with LLM
        prompt = f"""Based on these SEC filing excerpts for {ticker}, provide a trading signal:

{context_text}

Focus on: growth trajectory, profitability trends, management outlook, and risks.

Provide: SIGNAL, CONFIDENCE, REASONING"""

        response = llm.generate(
            prompt, PromptTemplates.ANALYST_SYSTEM, temperature=0.3, max_tokens=500
        )
        parsed = PromptTemplates.parse_llm_response(response.content)

        return parsed["signal"], parsed["confidence"], parsed["reasoning"]

    except Exception as e:
        return "neutral", 0.4, f"RAG analysis failed: {str(e)}"


@agent("AI Market Commentator", "LLM-powered comprehensive view")
def ai_market_commentator(ticker, context):
    """
    Synthesize all available data into comprehensive analysis
    """
    llm = get_llm_provider("ollama")
    if not llm or not llm.is_available():
        return "neutral", 0.3, "LLM not available"

    # Gather all data
    fundamentals = context.get_fundamentals()
    prices = context.get_price_data(days=5)
    news = context.get_news(limit=3)

    # Build comprehensive prompt
    prompt = f"""Analyze {ticker} across multiple dimensions:

FUNDAMENTALS:
- P/E: {fundamentals.get('pe_ratio', 'N/A')}
- Revenue Growth: {fundamentals.get('revenue_growth', 'N/A')}%
- Profit Margin: {fundamentals.get('profit_margin', 'N/A')}%
- Debt/Equity: {fundamentals.get('debt_to_equity', 'N/A')}

TECHNICAL:
- Current Price: ${prices[0]['close'] if prices else 'N/A'}
- RSI: {prices[0].get('rsi_14', 'N/A') if prices else 'N/A'}

SENTIMENT:
- Recent news articles: {len(news)}
- Average sentiment: {sum(n.get('sentiment_score', 0) for n in news) / len(news) if news else 'N/A'}

Provide holistic analysis: SIGNAL, CONFIDENCE, REASONING"""

    try:
        response = llm.generate(
            prompt, PromptTemplates.ANALYST_SYSTEM, temperature=0.4, max_tokens=600
        )
        parsed = PromptTemplates.parse_llm_response(response.content)
        return parsed["signal"], parsed["confidence"], parsed["reasoning"]
    except Exception as e:
        return "neutral", 0.4, f"Comprehensive analysis failed: {str(e)}"


# ============================================================================
# SUPERVISOR AGENT (For Hierarchical Orchestration)
# ============================================================================


@agent("Lead Investment Analyst", "Supervises and synthesizes worker agents")
def lead_analyst(ticker, context):
    """
    Supervisor agent that reviews worker signals and makes final call

    Used in hierarchical orchestration
    """
    # Get worker signals if available
    worker_signals = getattr(context, "worker_signals", [])

    if not worker_signals:
        # No workers, do own analysis
        fundamentals = context.get_fundamentals()
        pe = fundamentals.get("pe_ratio", 25)
        growth = fundamentals.get("revenue_growth", 0)

        if pe < 20 and growth > 10:
            return "bullish", 0.75, "Attractive valuation with growth"
        else:
            return "neutral", 0.6, "Monitoring situation"

    # Analyze worker consensus
    bullish = sum(1 for s in worker_signals if s["signal_type"] == "bullish")
    bearish = sum(1 for s in worker_signals if s["signal_type"] == "bearish")
    total = len(worker_signals)

    avg_confidence = sum(s["confidence"] for s in worker_signals) / total

    # Check for strong dissent
    high_confidence_dissent = [
        s
        for s in worker_signals
        if s["confidence"] > 0.8
        and s["signal_type"] != ("bullish" if bullish > bearish else "bearish")
    ]

    # Supervisor decision logic
    if bullish > total * 0.7:
        # Strong consensus bullish
        return (
            "bullish",
            min(0.9, avg_confidence + 0.1),
            f"Strong team consensus: {bullish}/{total} bullish",
        )

    elif bearish > total * 0.7:
        # Strong consensus bearish
        return (
            "bearish",
            min(0.9, avg_confidence + 0.1),
            f"Strong team consensus: {bearish}/{total} bearish",
        )

    elif high_confidence_dissent:
        # Notable dissent from high-confidence agent
        dissenter = high_confidence_dissent[0]
        return (
            "neutral",
            0.6,
            f"Split decision - {dissenter['agent_name']} dissents with {dissenter['confidence']:.0%} confidence",
        )

    else:
        # Moderate consensus
        signal = (
            "bullish"
            if bullish > bearish
            else "bearish" if bearish > bullish else "neutral"
        )
        return (
            signal,
            avg_confidence,
            f"Team split: {bullish} bullish, {bearish} bearish, {total - bullish - bearish} neutral",
        )


# ============================================================================
# SPECIALIZED AGENTS
# ============================================================================


@agent("Dividend Investor", "Focus on dividend yield and safety")
def dividend_investor(ticker, context):
    """
    Dividend-focused investment strategy
    """
    div_yield = context.get_fundamental("dividend_yield", 0)
    payout_ratio = context.get_fundamental("payout_ratio", 100)
    debt_eq = context.get_fundamental("debt_to_equity", 2.0)

    if div_yield > 3 and payout_ratio < 60 and debt_eq < 1.0:
        return (
            "bullish",
            0.8,
            f"Attractive dividend {div_yield:.1f}% with safe payout ratio {payout_ratio:.0f}%",
        )
    elif div_yield < 1:
        return "neutral", 0.4, "Low dividend yield"
    elif payout_ratio > 80:
        return "bearish", 0.6, "Unsustainable dividend payout"
    else:
        return "neutral", 0.6, f"Moderate dividend {div_yield:.1f}%"


@agent("Contrarian Investor", "Buy fear, sell greed")
def contrarian(ticker, context):
    """
    Contrarian strategy - buy when others panic
    """
    news = context.get_news(limit=10)
    prices = context.get_price_data(days=20)

    if not news or not prices:
        return "neutral", 0.3, "Insufficient data"

    # Calculate sentiment
    avg_sentiment = sum(n.get("sentiment_score", 0) for n in news) / len(news)

    # Calculate price change
    current = prices[0]["close"]
    past = prices[-1]["close"]
    pct_change = ((current - past) / past) * 100

    # Contrarian logic: Buy on fear after decline
    if avg_sentiment < -0.4 and pct_change < -10:
        return (
            "bullish",
            0.75,
            f"Extreme negative sentiment ({avg_sentiment:.2f}) after {pct_change:.1f}% decline - contrarian buy",
        )

    # Sell on euphoria after rally
    elif avg_sentiment > 0.6 and pct_change > 20:
        return (
            "bearish",
            0.7,
            f"Excessive optimism ({avg_sentiment:.2f}) after {pct_change:.1f}% rally - contrarian sell",
        )

    else:
        return "neutral", 0.5, "No extreme sentiment to exploit"


@agent("Sector Rotation", "Monitors sector strength")
def sector_rotation(ticker, context):
    """
    Sector rotation strategy
    """
    fundamentals = context.get_fundamentals()
    sector = fundamentals.get("sector", "Unknown")

    # Get macro indicators
    indicators = context.get_macro_indicators()

    # Simplified sector rotation logic
    gdp = None
    for ind in indicators:
        if "GDP" in ind.get("indicator_name", ""):
            gdp = ind.get("value", 0)
            break

    if gdp and gdp > 2.5:
        # Strong economy - favor cyclicals
        cyclical_sectors = ["Technology", "Consumer Cyclical", "Industrials"]
        if sector in cyclical_sectors:
            return "bullish", 0.7, f"Favorable macro for {sector} sector"
    elif gdp and gdp < 1.5:
        # Weak economy - favor defensives
        defensive_sectors = ["Healthcare", "Utilities", "Consumer Staples"]
        if sector in defensive_sectors:
            return "bullish", 0.7, f"Defensive {sector} sector in weak economy"

    return "neutral", 0.5, f"{sector} sector - neutral rotation signal"


# ============================================================================
# REGISTRATION FUNCTION
# ============================================================================


def register_production_agents():
    """Register all production agents"""
    registry = get_registry()

    print("\n" + "=" * 70)
    print("REGISTERING PRODUCTION AGENT SUITE")
    print("=" * 70)

    # Fundamental agents
    registry.register(value_investor.agent, weight=1.2, tags=["fundamental", "value"])
    registry.register(growth_investor.agent, weight=1.2, tags=["fundamental", "growth"])
    registry.register(
        quality_investor.agent, weight=1.1, tags=["fundamental", "quality"]
    )
    print("✅ Fundamental agents: 3")

    # Technical agents
    registry.register(trend_follower.agent, weight=1.0, tags=["technical", "trend"])
    registry.register(momentum_trader.agent, weight=1.0, tags=["technical", "momentum"])
    print("✅ Technical agents: 2")

    # Sentiment agents
    registry.register(news_sentiment.agent, weight=0.9, tags=["sentiment", "news"])
    registry.register(
        analyst_consensus.agent, weight=1.0, tags=["sentiment", "analyst"]
    )
    print("✅ Sentiment agents: 2")

    # Risk agents
    registry.register(volatility_risk.agent, weight=1.1, tags=["risk", "volatility"])
    registry.register(insider_activity.agent, weight=0.8, tags=["risk", "insider"])
    print("✅ Risk agents: 2")

    # Macro agents
    registry.register(macro_analyst.agent, weight=1.0, tags=["macro", "economy"])
    registry.register(market_regime.agent, weight=0.9, tags=["macro", "regime"])
    registry.register(sector_rotation.agent, weight=0.8, tags=["macro", "sector"])
    print("✅ Macro agents: 3")

    # LLM agents
    registry.register(
        ai_fundamental_analyst.agent, weight=1.3, tags=["llm", "fundamental"]
    )
    registry.register(ai_sec_analyst.agent, weight=1.4, tags=["llm", "rag", "sec"])
    registry.register(
        ai_market_commentator.agent, weight=1.2, tags=["llm", "comprehensive"]
    )
    print("✅ LLM agents: 3")

    # Specialized agents
    registry.register(
        dividend_investor.agent, weight=0.9, tags=["specialized", "dividend"]
    )
    registry.register(contrarian.agent, weight=0.8, tags=["specialized", "contrarian"])
    print("✅ Specialized agents: 2")

    # Supervisor
    registry.register(lead_analyst.agent, weight=1.5, tags=["supervisor"], enabled=True)
    print("✅ Supervisor agent: 1")

    stats = registry.stats()
    print(f"\n📊 Total agents: {stats['total']}")
    print(f"📊 Enabled agents: {stats['enabled']}")
    print("=" * 70 + "\n")


# ============================================================================
# STANDALONE TEST
# ============================================================================

if __name__ == "__main__":
    """Test production agents"""
    from agent_builder.core.config import Config
    from agent_builder.core.database import DatabasePool, Database
    from agent_builder.agents.context import AgentContext

    print("\n🧪 TESTING PRODUCTION AGENTS\n")

    # Setup
    config = Config.from_env()
    pool = DatabasePool(config.database)
    db = Database(pool)

    # Register agents
    register_production_agents()

    # Test ticker
    ticker = "AAPL"
    context = AgentContext(ticker, db)

    # Test each category
    categories = {
        "Fundamental": [value_investor, growth_investor, quality_investor],
        "Technical": [trend_follower, momentum_trader],
        "Sentiment": [news_sentiment, analyst_consensus],
        "Risk": [volatility_risk, insider_activity],
        "Macro": [macro_analyst, market_regime],
    }

    for category, agents in categories.items():
        print(f"\n{category} Agents:")
        print("-" * 50)
        for agent_func in agents:
            try:
                signal = agent_func.agent.analyze(ticker, context)
                print(f"  {agent_func.agent.name}:")
                print(f"    Signal: {signal.signal_type}")
                print(f"    Confidence: {signal.confidence:.0%}")
                print(f"    Reasoning: {signal.reasoning[:80]}...")
            except Exception as e:
                print(f"  {agent_func.agent.name}: ❌ {e}")

    pool.close()
    print("\n✅ Production agent test complete\n")
