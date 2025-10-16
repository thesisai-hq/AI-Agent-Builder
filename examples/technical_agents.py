"""
Technical Analysis Agents
Focus on price patterns, indicators, and chart analysis
"""

from agent_builder.agents import simple_agent
from agent_builder.repositories.connection import get_db_cursor
import logging

logger = logging.getLogger(__name__)


# =============================================================================
# MOVING AVERAGE AGENTS
# =============================================================================


@simple_agent("Moving Average Crossover", weight=0.12)
def ma_crossover_agent(ticker, context):
    """
    Golden Cross / Death Cross strategy

    Strategy:
    - Golden Cross: 50 MA crosses above 200 MA = bullish
    - Death Cross: 50 MA crosses below 200 MA = bearish
    - Price position relative to MAs
    """
    technicals = context.get_technical_indicators(days=5)

    if len(technicals) < 2:
        return "neutral", 0.5

    current = technicals[0]
    previous = technicals[1]

    sma_20 = current.get("sma_20", 0)
    sma_50 = current.get("sma_50", 0)
    sma_200 = current.get("sma_200", 0)

    prev_sma_50 = previous.get("sma_50", 0)
    prev_sma_200 = previous.get("sma_200", 0)

    # Get current price
    prices = context.get_price_data(days=1)
    if not prices:
        return "neutral", 0.5

    current_price = prices[0].get("close", 0)

    if not all([sma_50, sma_200, prev_sma_50, prev_sma_200, current_price]):
        return "neutral", 0.5

    score = 0

    # Golden Cross / Death Cross
    if prev_sma_50 < prev_sma_200 and sma_50 > sma_200:
        score += 4  # Golden Cross - very bullish
    elif prev_sma_50 > prev_sma_200 and sma_50 < sma_200:
        score -= 4  # Death Cross - very bearish

    # MA alignment (all MAs in order)
    if sma_20 > sma_50 > sma_200:
        score += 2  # Bullish alignment
    elif sma_20 < sma_50 < sma_200:
        score -= 2  # Bearish alignment

    # Price relative to MAs
    if current_price > sma_20 and current_price > sma_50:
        score += 2  # Above key MAs
    elif current_price < sma_20 and current_price < sma_50:
        score -= 2  # Below key MAs

    # Price vs 200 MA
    if current_price > sma_200:
        score += 1  # Long-term uptrend
    else:
        score -= 1  # Long-term downtrend

    # Decision
    if score >= 6:
        return "bullish", 0.90
    elif score >= 4:
        return "bullish", 0.80
    elif score >= 2:
        return "bullish", 0.70
    elif score >= 0:
        return "neutral", 0.55
    elif score >= -2:
        return "bearish", 0.70
    elif score >= -4:
        return "bearish", 0.80
    else:
        return "bearish", 0.90


@simple_agent("Price vs Moving Averages", weight=0.10)
def price_ma_position_agent(ticker, context):
    """
    Analyze price position relative to moving averages

    Strategy:
    - Price above all MAs = strong uptrend
    - Price below all MAs = strong downtrend
    - Price between MAs = consolidation
    """
    technicals = context.get_technical_indicators(days=1)
    prices = context.get_price_data(days=1)

    if not technicals or not prices:
        return "neutral", 0.5

    latest_tech = technicals[0]
    current_price = prices[0].get("close", 0)

    sma_20 = latest_tech.get("sma_20", 0)
    sma_50 = latest_tech.get("sma_50", 0)
    sma_200 = latest_tech.get("sma_200", 0)

    if not all([current_price, sma_20, sma_50, sma_200]):
        return "neutral", 0.5

    # Count how many MAs price is above
    above_count = 0
    if current_price > sma_20:
        above_count += 1
    if current_price > sma_50:
        above_count += 1
    if current_price > sma_200:
        above_count += 1

    # Distance from 20 MA (momentum)
    distance_from_20ma = ((current_price - sma_20) / sma_20) * 100 if sma_20 > 0 else 0

    # Decision
    if above_count == 3:
        # Above all MAs
        if distance_from_20ma > 5:
            return "bullish", 0.85  # Strong momentum
        else:
            return "bullish", 0.75  # Solid uptrend
    elif above_count == 2:
        return "bullish", 0.65  # Moderate uptrend
    elif above_count == 1:
        return "neutral", 0.55  # Mixed
    else:
        # Below all MAs
        if distance_from_20ma < -5:
            return "bearish", 0.85  # Strong downtrend
        else:
            return "bearish", 0.75  # Solid downtrend


# =============================================================================
# MOMENTUM INDICATORS
# =============================================================================


@simple_agent("RSI Momentum", weight=0.11)
def rsi_momentum_agent(ticker, context):
    """
    Relative Strength Index strategy

    Strategy:
    - RSI < 30 = oversold, bullish
    - RSI > 70 = overbought, bearish
    - RSI 40-60 = neutral zone
    - RSI divergences
    """
    technicals = context.get_technical_indicators(days=5)

    if not technicals:
        return "neutral", 0.5

    current_rsi = technicals[0].get("rsi_14", 50)

    # Check for RSI trend
    if len(technicals) >= 3:
        prev_rsi = technicals[2].get("rsi_14", 50)
        rsi_trend = current_rsi - prev_rsi
    else:
        rsi_trend = 0

    # RSI interpretation
    if current_rsi < 25:
        return "bullish", 0.85  # Deeply oversold
    elif current_rsi < 30:
        return "bullish", 0.80  # Oversold
    elif current_rsi < 35:
        return "bullish", 0.70  # Approaching oversold
    elif current_rsi < 40 and rsi_trend > 0:
        return "bullish", 0.65  # Turning up from oversold
    elif current_rsi > 75:
        return "bearish", 0.85  # Deeply overbought
    elif current_rsi > 70:
        return "bearish", 0.80  # Overbought
    elif current_rsi > 65:
        return "bearish", 0.70  # Approaching overbought
    elif current_rsi > 60 and rsi_trend < 0:
        return "bearish", 0.65  # Turning down from overbought
    elif 45 <= current_rsi <= 55:
        return "neutral", 0.50  # Neutral zone
    elif current_rsi > 50:
        return "bullish", 0.60  # Bullish momentum
    else:
        return "bearish", 0.60  # Bearish momentum


@simple_agent("MACD Signal", weight=0.11)
def macd_signal_agent(ticker, context):
    """
    MACD crossover and histogram strategy

    Strategy:
    - MACD crosses above signal = bullish
    - MACD crosses below signal = bearish
    - Histogram increasing = momentum strengthening
    """
    technicals = context.get_technical_indicators(days=3)

    if len(technicals) < 2:
        return "neutral", 0.5

    current = technicals[0]
    previous = technicals[1]

    macd = current.get("macd", 0)
    macd_signal = current.get("macd_signal", 0)
    macd_hist = current.get("macd_histogram", 0)

    prev_macd = previous.get("macd", 0)
    prev_signal = previous.get("macd_signal", 0)
    prev_hist = previous.get("macd_histogram", 0)

    score = 0

    # Bullish crossover
    if prev_macd < prev_signal and macd > macd_signal:
        score += 3  # Bullish crossover
    elif macd > macd_signal:
        score += 1  # Already above signal

    # Bearish crossover
    if prev_macd > prev_signal and macd < macd_signal:
        score -= 3  # Bearish crossover
    elif macd < macd_signal:
        score -= 1  # Already below signal

    # Histogram trend (momentum)
    if macd_hist > prev_hist and macd_hist > 0:
        score += 2  # Strengthening bullish momentum
    elif macd_hist > prev_hist and macd_hist < 0:
        score += 1  # Weakening bearish momentum
    elif macd_hist < prev_hist and macd_hist < 0:
        score -= 2  # Strengthening bearish momentum
    elif macd_hist < prev_hist and macd_hist > 0:
        score -= 1  # Weakening bullish momentum

    # Both MACD and signal above zero (strong trend)
    if macd > 0 and macd_signal > 0:
        score += 1
    elif macd < 0 and macd_signal < 0:
        score -= 1

    # Decision
    if score >= 5:
        return "bullish", 0.90
    elif score >= 3:
        return "bullish", 0.75
    elif score >= 1:
        return "bullish", 0.65
    elif score <= -5:
        return "bearish", 0.90
    elif score <= -3:
        return "bearish", 0.75
    elif score <= -1:
        return "bearish", 0.65
    else:
        return "neutral", 0.50


@simple_agent("ADX Trend Strength", weight=0.09)
def adx_trend_strength_agent(ticker, context):
    """
    Average Directional Index - trend strength

    Strategy:
    - ADX > 25 = strong trend (trade with trend)
    - ADX < 20 = weak trend (avoid or range trade)
    - Combine with price direction
    """
    technicals = context.get_technical_indicators(days=5)
    prices = context.get_price_data(days=10)

    if not technicals or len(prices) < 10:
        return "neutral", 0.5

    adx = technicals[0].get("adx_14", 0)

    # Determine trend direction from prices
    recent_avg = sum(p["close"] for p in prices[:5]) / 5
    older_avg = sum(p["close"] for p in prices[5:10]) / 5
    trend_direction = "up" if recent_avg > older_avg else "down"

    # ADX interpretation
    if adx > 40:
        # Very strong trend
        if trend_direction == "up":
            return "bullish", 0.85
        else:
            return "bearish", 0.85
    elif adx > 25:
        # Strong trend
        if trend_direction == "up":
            return "bullish", 0.75
        else:
            return "bearish", 0.75
    elif adx > 20:
        # Moderate trend
        if trend_direction == "up":
            return "bullish", 0.60
        else:
            return "bearish", 0.60
    else:
        # Weak trend or ranging
        return "neutral", 0.50


# =============================================================================
# VOLATILITY INDICATORS
# =============================================================================


@simple_agent("Bollinger Bands", weight=0.10)
def bollinger_bands_agent(ticker, context):
    """
    Bollinger Bands mean reversion strategy

    Strategy:
    - Price at lower band = oversold, bullish
    - Price at upper band = overbought, bearish
    - Squeeze (bands narrow) = breakout coming
    """
    technicals = context.get_technical_indicators(days=1)
    prices = context.get_price_data(days=1)

    if not technicals or not prices:
        return "neutral", 0.5

    latest_tech = technicals[0]
    current_price = prices[0].get("close", 0)

    bb_upper = latest_tech.get("bollinger_upper", 0)
    bb_middle = latest_tech.get("bollinger_middle", 0)
    bb_lower = latest_tech.get("bollinger_lower", 0)

    if not all([current_price, bb_upper, bb_middle, bb_lower]):
        return "neutral", 0.5

    # Calculate position within bands
    bb_range = bb_upper - bb_lower
    if bb_range > 0:
        position = (current_price - bb_lower) / bb_range  # 0 to 1
    else:
        position = 0.5

    # Band width (squeeze detection)
    if bb_middle > 0:
        band_width = (bb_range / bb_middle) * 100
    else:
        band_width = 0

    # Decision
    if position <= 0.05:
        return "bullish", 0.85  # At or below lower band
    elif position <= 0.15:
        return "bullish", 0.75  # Near lower band
    elif position <= 0.30:
        return "bullish", 0.65  # Below middle
    elif position >= 0.95:
        return "bearish", 0.85  # At or above upper band
    elif position >= 0.85:
        return "bearish", 0.75  # Near upper band
    elif position >= 0.70:
        return "bearish", 0.65  # Above middle
    else:
        # Middle of bands
        if band_width < 5:
            # Squeeze - anticipate breakout
            return "neutral", 0.50  # Wait for direction
        else:
            return "neutral", 0.50


@simple_agent("ATR Volatility", weight=0.08)
def atr_volatility_agent(ticker, context):
    """
    Average True Range - volatility analysis

    Strategy:
    - High ATR = high volatility (risk)
    - Rising ATR = increasing volatility
    - Low ATR = consolidation (potential breakout)
    """
    technicals = context.get_technical_indicators(days=5)

    if len(technicals) < 5:
        return "neutral", 0.5

    current_atr = technicals[0].get("atr_14", 0)
    older_atr = technicals[4].get("atr_14", 0)

    # Get average price for normalization
    prices = context.get_price_data(days=1)
    if prices:
        current_price = prices[0].get("close", 1)
        atr_pct = (current_atr / current_price) * 100 if current_price > 0 else 0
    else:
        atr_pct = 0

    # ATR trend
    if older_atr > 0:
        atr_change = ((current_atr - older_atr) / older_atr) * 100
    else:
        atr_change = 0

    # Interpretation
    if atr_pct < 2:
        # Very low volatility (consolidation)
        return "neutral", 0.55  # Potential breakout setup
    elif atr_pct > 5 and atr_change > 20:
        # Volatility spike (risk)
        return "bearish", 0.65  # High risk environment
    elif atr_pct > 4:
        # High volatility
        return "neutral", 0.50  # Caution
    else:
        # Normal volatility
        return "neutral", 0.50


# =============================================================================
# VOLUME INDICATORS
# =============================================================================


@simple_agent("Volume Analysis", weight=0.09)
def volume_analysis_agent(ticker, context):
    """
    Volume trend and confirmation

    Strategy:
    - Rising price + rising volume = bullish confirmation
    - Rising price + falling volume = weak trend
    - Falling price + rising volume = bearish confirmation
    """
    prices = context.get_price_data(days=10)

    if len(prices) < 10:
        return "neutral", 0.5

    # Recent vs older periods
    recent_prices = prices[:5]
    older_prices = prices[5:10]

    recent_avg_price = sum(p["close"] for p in recent_prices) / 5
    older_avg_price = sum(p["close"] for p in older_prices) / 5

    recent_avg_volume = sum(p["volume"] for p in recent_prices) / 5
    older_avg_volume = sum(p["volume"] for p in older_prices) / 5

    price_trend = "up" if recent_avg_price > older_avg_price else "down"
    volume_trend = "up" if recent_avg_volume > older_avg_volume * 1.1 else "down"

    # Price and volume confirmation
    if price_trend == "up" and volume_trend == "up":
        return "bullish", 0.80  # Strong confirmation
    elif price_trend == "up" and volume_trend == "down":
        return "bullish", 0.60  # Weak confirmation
    elif price_trend == "down" and volume_trend == "up":
        return "bearish", 0.80  # Strong confirmation
    elif price_trend == "down" and volume_trend == "down":
        return "bearish", 0.60  # Weak confirmation
    else:
        return "neutral", 0.50


@simple_agent("On Balance Volume", weight=0.08)
def obv_agent(ticker, context):
    """
    On Balance Volume - cumulative volume

    Strategy:
    - OBV rising = accumulation, bullish
    - OBV falling = distribution, bearish
    - OBV divergence from price = warning
    """
    technicals = context.get_technical_indicators(days=10)
    prices = context.get_price_data(days=10)

    if len(technicals) < 10 or len(prices) < 10:
        return "neutral", 0.5

    # OBV trend
    recent_obv = sum(t["obv"] for t in technicals[:5]) / 5
    older_obv = sum(t["obv"] for t in technicals[5:10]) / 5
    obv_trend = "up" if recent_obv > older_obv else "down"

    # Price trend
    recent_price = sum(p["close"] for p in prices[:5]) / 5
    older_price = sum(p["close"] for p in prices[5:10]) / 5
    price_trend = "up" if recent_price > older_price else "down"

    # OBV vs Price analysis
    if obv_trend == "up" and price_trend == "up":
        return "bullish", 0.75  # Confirmed uptrend
    elif obv_trend == "up" and price_trend == "down":
        return "bullish", 0.80  # Bullish divergence (accumulation)
    elif obv_trend == "down" and price_trend == "down":
        return "bearish", 0.75  # Confirmed downtrend
    elif obv_trend == "down" and price_trend == "up":
        return "bearish", 0.80  # Bearish divergence (distribution)
    else:
        return "neutral", 0.50


# =============================================================================
# PRICE ACTION AGENTS
# =============================================================================


@simple_agent("Support & Resistance", weight=0.10)
def support_resistance_agent(ticker, context):
    """
    Support and resistance levels

    Strategy:
    - Price near support = potential bounce, bullish
    - Price near resistance = potential rejection, bearish
    - Breakout above resistance = bullish
    - Breakdown below support = bearish
    """
    prices = context.get_price_data(days=30)

    if len(prices) < 30:
        return "neutral", 0.5

    # Get recent highs and lows
    recent_prices = [p["close"] for p in prices]
    current_price = recent_prices[0]

    # Simple support/resistance (highest high, lowest low in period)
    resistance = max(recent_prices[1:])  # Exclude current
    support = min(recent_prices[1:])

    price_range = resistance - support
    if price_range == 0:
        return "neutral", 0.5

    # Position in range
    position_in_range = (current_price - support) / price_range

    # Distance to key levels
    distance_to_resistance = ((resistance - current_price) / current_price) * 100
    distance_to_support = ((current_price - support) / current_price) * 100

    # Decision
    if current_price > resistance:
        return "bullish", 0.85  # Breakout above resistance
    elif distance_to_resistance < 2:
        return "bearish", 0.70  # Near resistance
    elif current_price < support:
        return "bearish", 0.85  # Breakdown below support
    elif distance_to_support < 2:
        return "bullish", 0.70  # Near support (bounce opportunity)
    elif position_in_range > 0.7:
        return "bearish", 0.60  # Upper part of range
    elif position_in_range < 0.3:
        return "bullish", 0.60  # Lower part of range
    else:
        return "neutral", 0.50  # Middle of range


@simple_agent("Trend Continuation", weight=0.09)
def trend_continuation_agent(ticker, context):
    """
    Identify and follow established trends

    Strategy:
    - Series of higher highs and higher lows = uptrend
    - Series of lower highs and lower lows = downtrend
    - Pullbacks in uptrend = buying opportunity
    """
    prices = context.get_price_data(days=20)

    if len(prices) < 20:
        return "neutral", 0.5

    # Divide into 4 periods of 5 days each
    periods = [
        prices[0:5],
        prices[5:10],
        prices[10:15],
        prices[15:20],
    ]

    # Get highs and lows for each period
    period_highs = [max(p["high"] for p in period) for period in periods]
    period_lows = [min(p["low"] for p in period) for period in periods]

    # Check for uptrend (higher highs and higher lows)
    higher_highs = all(
        period_highs[i] > period_highs[i + 1] for i in range(len(period_highs) - 1)
    )
    higher_lows = all(
        period_lows[i] > period_lows[i + 1] for i in range(len(period_lows) - 1)
    )

    # Check for downtrend (lower highs and lower lows)
    lower_highs = all(
        period_highs[i] < period_highs[i + 1] for i in range(len(period_highs) - 1)
    )
    lower_lows = all(
        period_lows[i] < period_lows[i + 1] for i in range(len(period_lows) - 1)
    )

    # Decision
    if higher_highs and higher_lows:
        return "bullish", 0.85  # Strong uptrend
    elif higher_highs or higher_lows:
        return "bullish", 0.70  # Partial uptrend
    elif lower_highs and lower_lows:
        return "bearish", 0.85  # Strong downtrend
    elif lower_highs or lower_lows:
        return "bearish", 0.70  # Partial downtrend
    else:
        return "neutral", 0.50  # No clear trend


# =============================================================================
# MULTI-TIMEFRAME AGENTS
# =============================================================================


@simple_agent("Multi-Timeframe Confluence", weight=0.11)
def multi_timeframe_agent(ticker, context):
    """
    Analyze alignment across multiple timeframes

    Strategy:
    - Short-term (5d), medium-term (20d), long-term (50d) alignment
    - All timeframes bullish = strong buy
    - Mixed signals = caution
    """
    prices = context.get_price_data(days=60)

    if len(prices) < 60:
        return "neutral", 0.5

    # Calculate trends for different timeframes
    def get_trend(start, end, prices_list):
        period_prices = prices_list[start:end]
        if not period_prices:
            return "neutral"
        first_price = period_prices[-1]["close"]  # Oldest in period
        last_price = period_prices[0]["close"]  # Most recent
        return (
            "up"
            if last_price > first_price * 1.02
            else "down" if last_price < first_price * 0.98 else "neutral"
        )

    short_term = get_trend(0, 5, prices)  # Last 5 days
    medium_term = get_trend(0, 20, prices)  # Last 20 days
    long_term = get_trend(0, 50, prices)  # Last 50 days

    # Count bullish timeframes
    bullish_count = sum([short_term == "up", medium_term == "up", long_term == "up"])

    bearish_count = sum(
        [short_term == "down", medium_term == "down", long_term == "down"]
    )

    # Decision
    if bullish_count == 3:
        return "bullish", 0.90  # All timeframes aligned bullish
    elif bullish_count == 2:
        return "bullish", 0.75  # Majority bullish
    elif bearish_count == 3:
        return "bearish", 0.90  # All timeframes aligned bearish
    elif bearish_count == 2:
        return "bearish", 0.75  # Majority bearish
    else:
        return "neutral", 0.50  # Mixed signals


# =============================================================================
# COMPOSITE TECHNICAL AGENT
# =============================================================================


@simple_agent("Technical Score Composite", weight=0.12)
def technical_composite_agent(ticker, context):
    """
    Aggregate all technical indicators

    Strategy:
    - Combine trend, momentum, and volume signals
    - Weight by reliability
    - Generate composite technical score
    """
    technicals = context.get_technical_indicators(days=5)
    prices = context.get_price_data(days=20)

    if not technicals or len(prices) < 20:
        return "neutral", 0.5

    latest = technicals[0]
    current_price = prices[0]["close"]

    score = 0

    # Moving averages (weight: 3)
    sma_20 = latest.get("sma_20", 0)
    sma_50 = latest.get("sma_50", 0)
    if sma_20 and sma_50:
        if current_price > sma_20 > sma_50:
            score += 3
        elif current_price < sma_20 < sma_50:
            score -= 3
        elif current_price > sma_20:
            score += 1
        elif current_price < sma_20:
            score -= 1

    # RSI (weight: 2)
    rsi = latest.get("rsi_14", 50)
    if rsi < 30:
        score += 2
    elif rsi < 40:
        score += 1
    elif rsi > 70:
        score -= 2
    elif rsi > 60:
        score -= 1

    # MACD (weight: 2)
    macd = latest.get("macd", 0)
    macd_signal = latest.get("macd_signal", 0)
    if macd > macd_signal and macd > 0:
        score += 2
    elif macd > macd_signal:
        score += 1
    elif macd < macd_signal and macd < 0:
        score -= 2
    elif macd < macd_signal:
        score -= 1

    # Volume trend (weight: 1)
    recent_volume = sum(p["volume"] for p in prices[:5]) / 5
    older_volume = sum(p["volume"] for p in prices[10:15]) / 5
    if recent_volume > older_volume * 1.2:
        # High volume - amplify existing score
        if score > 0:
            score += 1
        elif score < 0:
            score -= 1

    # Decision
    if score >= 7:
        return "bullish", 0.90
    elif score >= 5:
        return "bullish", 0.80
    elif score >= 3:
        return "bullish", 0.70
    elif score >= 1:
        return "bullish", 0.60
    elif score <= -7:
        return "bearish", 0.90
    elif score <= -5:
        return "bearish", 0.80
    elif score <= -3:
        return "bearish", 0.70
    elif score <= -1:
        return "bearish", 0.60
    else:
        return "neutral", 0.50


# =============================================================================
# REGISTRATION
# =============================================================================


def register_technical_agents():
    """Register all technical agents"""
    from agent_builder.agents.registry import get_registry

    registry = get_registry()

    # Moving average agents
    registry.register(ma_crossover_agent.agent, tags=["technical", "trend", "ma"])
    registry.register(price_ma_position_agent.agent, tags=["technical", "trend", "ma"])

    # Momentum agents
    registry.register(rsi_momentum_agent.agent, tags=["technical", "momentum"])
    registry.register(macd_signal_agent.agent, tags=["technical", "momentum"])
    registry.register(adx_trend_strength_agent.agent, tags=["technical", "trend"])

    # Volatility agents
    registry.register(bollinger_bands_agent.agent, tags=["technical", "volatility"])
    registry.register(atr_volatility_agent.agent, tags=["technical", "volatility"])

    # Volume agents
    registry.register(volume_analysis_agent.agent, tags=["technical", "volume"])
    registry.register(obv_agent.agent, tags=["technical", "volume"])

    # Price action agents
    registry.register(
        support_resistance_agent.agent, tags=["technical", "price_action"]
    )
    registry.register(trend_continuation_agent.agent, tags=["technical", "trend"])

    # Multi-timeframe agent
    registry.register(
        multi_timeframe_agent.agent, tags=["technical", "multi_timeframe"]
    )

    # Composite agent
    registry.register(technical_composite_agent.agent, tags=["technical", "composite"])

    logger.info("✅ Registered 13 technical agents")


if __name__ == "__main__":
    # Test agents
    from agent_builder.agents.context import AgentContext

    context = AgentContext("AAPL")

    print("Testing technical agents on AAPL:")
    print("-" * 60)

    agents = [
        ma_crossover_agent,
        rsi_momentum_agent,
        macd_signal_agent,
        bollinger_bands_agent,
        technical_composite_agent,
    ]

    for agent_func in agents:
        signal, confidence = agent_func("AAPL", context)
        print(f"{agent_func.__name__:35s} {signal:8s} ({confidence:.2f})")
