"""
Macro Economic Analysis Agents
Focus on economic cycles, interest rates, market indices, and macro conditions
"""

from agent_builder.agents import simple_agent
from agent_builder.repositories.connection import get_db_cursor
import logging

logger = logging.getLogger(__name__)


# =============================================================================
# ECONOMIC CYCLE AGENTS
# =============================================================================


@simple_agent("Economic Cycle Analyzer", weight=0.10)
def economic_cycle_agent(ticker, context):
    """
    Position based on economic cycle stage

    Strategy:
    - Expansion: GDP > 2.5%, unemployment < 4.5% = bullish
    - Recession: GDP < 1%, unemployment > 5.5% = bearish
    - Stagflation: Low GDP + high inflation = bearish
    """
    macro = context.get_macro_indicators()
    sector = context.get_metric("sector")

    if not macro:
        return "neutral", 0.5

    gdp_growth = macro.get("gdp_growth", 0)
    unemployment = macro.get("unemployment_rate", 0)
    inflation = macro.get("inflation_rate", 0)

    # Identify cycle stage
    score = 0

    # Strong economy
    if gdp_growth > 3.0 and unemployment < 4.0:
        score += 3  # Strong expansion
    elif gdp_growth > 2.5 and unemployment < 4.5:
        score += 2  # Moderate expansion
    elif gdp_growth > 2.0:
        score += 1  # Slow growth

    # Weak economy
    if gdp_growth < 0:
        score -= 3  # Recession
    elif gdp_growth < 1.0:
        score -= 2  # Near recession
    elif gdp_growth < 1.5:
        score -= 1  # Slow growth

    # Unemployment impact
    if unemployment > 6.0:
        score -= 2
    elif unemployment > 5.5:
        score -= 1
    elif unemployment < 4.0:
        score += 1

    # Stagflation check (worst case)
    if gdp_growth < 2.0 and inflation > 4.5:
        score -= 2  # Stagflation penalty

    # Sector-specific adjustments
    if sector in ["Technology", "Consumer Discretionary"]:
        # These sectors need strong economy
        if score < 0:
            score -= 1  # Extra bearish in weak economy
    elif sector in ["Utilities", "Consumer Staples"]:
        # Defensive sectors do better in weak economy
        if score < 0:
            score += 1  # Less bearish in weak economy

    # Decision
    if score >= 4:
        return "bullish", 0.85
    elif score >= 2:
        return "bullish", 0.70
    elif score >= 0:
        return "neutral", 0.55
    elif score >= -2:
        return "bearish", 0.65
    else:
        return "bearish", 0.80


@simple_agent("Recession Predictor", weight=0.09)
def recession_predictor_agent(ticker, context):
    """
    Predict recession using leading indicators

    Strategy:
    - Inverted yield curve = recession warning
    - Rising unemployment = recession risk
    - Falling GDP = recession signal
    """
    macro = context.get_macro_indicators()

    if not macro:
        return "neutral", 0.5

    treasury_10y = macro.get("treasury_10y", 0)
    treasury_2y = macro.get("treasury_2y", 0)
    gdp_growth = macro.get("gdp_growth", 0)
    unemployment = macro.get("unemployment_rate", 0)

    recession_signals = 0

    # Yield curve inversion (strongest signal)
    yield_spread = treasury_10y - treasury_2y
    if yield_spread < -0.5:
        recession_signals += 3  # Deeply inverted
    elif yield_spread < -0.2:
        recession_signals += 2  # Inverted
    elif yield_spread < 0:
        recession_signals += 1  # Slightly inverted

    # GDP weakness
    if gdp_growth < 0:
        recession_signals += 2  # Already in recession
    elif gdp_growth < 1.0:
        recession_signals += 1  # Very weak growth

    # Rising unemployment
    if unemployment > 5.5:
        recession_signals += 1
    elif unemployment > 6.0:
        recession_signals += 2

    # Decision
    if recession_signals >= 5:
        return "bearish", 0.90  # High recession risk
    elif recession_signals >= 3:
        return "bearish", 0.75  # Moderate recession risk
    elif recession_signals >= 1:
        return "bearish", 0.60  # Some recession risk
    else:
        return "neutral", 0.50


# =============================================================================
# INTEREST RATE AGENTS
# =============================================================================


@simple_agent("Interest Rate Sensitivity", weight=0.10)
def interest_rate_sensitivity_agent(ticker, context):
    """
    Analyze impact of interest rates on sector

    Strategy:
    - Rising rates hurt tech, real estate
    - Rising rates help financials
    - Falling rates help growth stocks
    """
    macro = context.get_macro_indicators()
    sector = context.get_metric("sector")

    if not macro:
        return "neutral", 0.5

    fed_funds = macro.get("fed_funds_rate", 0)

    # Determine rate direction (comparing to typical levels)
    # Fed funds > 4% = restrictive, < 2% = accommodative
    if fed_funds > 5.0:
        rate_environment = "very_restrictive"
    elif fed_funds > 4.0:
        rate_environment = "restrictive"
    elif fed_funds > 2.5:
        rate_environment = "neutral"
    elif fed_funds > 1.0:
        rate_environment = "accommodative"
    else:
        rate_environment = "very_accommodative"

    # Sector-specific impact
    rate_sensitive_sectors = {
        "Banking": {
            "very_restrictive": ("bullish", 0.80),
            "restrictive": ("bullish", 0.75),
            "neutral": ("neutral", 0.50),
            "accommodative": ("bearish", 0.60),
            "very_accommodative": ("bearish", 0.70),
        },
        "Financial Services": {
            "very_restrictive": ("bullish", 0.75),
            "restrictive": ("bullish", 0.70),
            "neutral": ("neutral", 0.50),
            "accommodative": ("bearish", 0.60),
            "very_accommodative": ("bearish", 0.65),
        },
        "Technology": {
            "very_restrictive": ("bearish", 0.75),
            "restrictive": ("bearish", 0.70),
            "neutral": ("neutral", 0.50),
            "accommodative": ("bullish", 0.65),
            "very_accommodative": ("bullish", 0.75),
        },
        "Real Estate": {
            "very_restrictive": ("bearish", 0.80),
            "restrictive": ("bearish", 0.75),
            "neutral": ("neutral", 0.50),
            "accommodative": ("bullish", 0.70),
            "very_accommodative": ("bullish", 0.80),
        },
        "Utilities": {
            "very_restrictive": ("bearish", 0.65),
            "restrictive": ("bearish", 0.60),
            "neutral": ("neutral", 0.50),
            "accommodative": ("bullish", 0.60),
            "very_accommodative": ("bullish", 0.65),
        },
    }

    if sector in rate_sensitive_sectors:
        signal, confidence = rate_sensitive_sectors[sector][rate_environment]
        return signal, confidence
    else:
        # Less rate-sensitive sectors
        return "neutral", 0.50


@simple_agent("Fed Policy Tracker", weight=0.09)
def fed_policy_agent(ticker, context):
    """
    Track Federal Reserve policy stance

    Strategy:
    - Hawkish Fed (raising rates) = bearish for growth
    - Dovish Fed (cutting rates) = bullish for growth
    - Neutral Fed = follow fundamentals
    """
    macro = context.get_macro_indicators()

    if not macro:
        return "neutral", 0.5

    fed_funds = macro.get("fed_funds_rate", 0)
    inflation = macro.get("inflation_rate", 0)

    # Determine Fed stance
    # If inflation high and rates high = hawkish (fighting inflation)
    # If inflation low and rates low = dovish (supporting growth)

    if inflation > 4.0 and fed_funds > 4.5:
        # Hawkish: High rates to fight inflation
        return "bearish", 0.70
    elif inflation > 3.5 and fed_funds > 4.0:
        # Moderately hawkish
        return "bearish", 0.60
    elif inflation < 2.5 and fed_funds < 3.0:
        # Dovish: Low rates to support growth
        return "bullish", 0.70
    elif inflation < 3.0 and fed_funds < 3.5:
        # Moderately dovish
        return "bullish", 0.60
    else:
        # Neutral policy
        return "neutral", 0.50


@simple_agent("Yield Curve Analyzer", weight=0.09)
def yield_curve_agent(ticker, context):
    """
    Analyze yield curve shape

    Strategy:
    - Steep curve (10Y - 2Y > 1%) = healthy economy, bullish
    - Flat curve (spread < 0.5%) = caution
    - Inverted curve (spread < 0) = recession warning, bearish
    """
    macro = context.get_macro_indicators()

    if not macro:
        return "neutral", 0.5

    treasury_10y = macro.get("treasury_10y", 0)
    treasury_2y = macro.get("treasury_2y", 0)

    yield_spread = treasury_10y - treasury_2y

    # Analyze curve shape
    if yield_spread > 1.5:
        return "bullish", 0.80  # Very steep (strong growth expected)
    elif yield_spread > 1.0:
        return "bullish", 0.70  # Steep (healthy economy)
    elif yield_spread > 0.5:
        return "bullish", 0.60  # Normal positive slope
    elif yield_spread > 0.2:
        return "neutral", 0.55  # Flattening
    elif yield_spread > 0:
        return "bearish", 0.60  # Very flat (warning sign)
    elif yield_spread > -0.3:
        return "bearish", 0.75  # Inverted (recession warning)
    else:
        return "bearish", 0.85  # Deeply inverted (strong recession signal)


# =============================================================================
# INFLATION AGENTS
# =============================================================================


@simple_agent("Inflation Monitor", weight=0.08)
def inflation_monitor_agent(ticker, context):
    """
    Monitor inflation impact on stocks

    Strategy:
    - Moderate inflation (2-3%) = goldilocks, bullish
    - High inflation (>4%) = bearish (Fed tightening)
    - Deflation (<1%) = bearish (weak demand)
    """
    macro = context.get_macro_indicators()
    sector = context.get_metric("sector")

    if not macro:
        return "neutral", 0.5

    inflation = macro.get("inflation_rate", 0)

    # Inflation impact
    if 2.0 <= inflation <= 3.0:
        # Goldilocks scenario
        base_signal = "bullish"
        base_confidence = 0.70
    elif inflation > 5.0:
        # High inflation (Fed will tighten)
        base_signal = "bearish"
        base_confidence = 0.75
    elif inflation > 4.0:
        # Elevated inflation
        base_signal = "bearish"
        base_confidence = 0.65
    elif inflation < 1.0:
        # Deflation risk (weak demand)
        base_signal = "bearish"
        base_confidence = 0.70
    elif inflation < 1.5:
        # Low inflation
        base_signal = "neutral"
        base_confidence = 0.55
    else:
        # Normal range
        base_signal = "neutral"
        base_confidence = 0.50

    # Sector-specific adjustments
    # Energy and commodities benefit from inflation
    if sector in ["Energy", "Materials"] and inflation > 3.5:
        return "bullish", 0.75

    # Tech and growth hurt by high inflation
    if sector == "Technology" and inflation > 4.5:
        return "bearish", 0.80

    return base_signal, base_confidence


@simple_agent("Pricing Power Analyzer", weight=0.07)
def pricing_power_agent(ticker, context):
    """
    Analyze company's pricing power in inflationary environment

    Strategy:
    - High margins + high inflation = pricing power, bullish
    - Low margins + high inflation = margin squeeze, bearish
    """
    macro = context.get_macro_indicators()
    profit_margin = context.get_metric("profit_margin")
    gross_margin = context.get_metric("gross_margin")

    if not macro:
        return "neutral", 0.5

    inflation = macro.get("inflation_rate", 0)

    # Only relevant in high inflation environment
    if inflation < 3.0:
        return "neutral", 0.50

    # High margins = pricing power
    has_pricing_power = gross_margin > 40 and profit_margin > 15
    weak_pricing_power = gross_margin < 25 or profit_margin < 8

    if has_pricing_power:
        return "bullish", 0.75  # Can pass costs to customers
    elif weak_pricing_power:
        return "bearish", 0.70  # Margin squeeze risk
    else:
        return "neutral", 0.55


# =============================================================================
# MARKET SENTIMENT AGENTS
# =============================================================================


@simple_agent("VIX Fear Gauge", weight=0.10)
def vix_fear_gauge_agent(ticker, context):
    """
    Volatility Index as contrarian indicator

    Strategy:
    - VIX < 12 = complacency, contrarian bearish
    - VIX 12-20 = normal, neutral
    - VIX 20-30 = fear, opportunity
    - VIX > 30 = panic, contrarian bullish
    """
    macro = context.get_macro_indicators()

    if not macro:
        return "neutral", 0.5

    vix = macro.get("vix_level", 15)

    # VIX interpretation (contrarian)
    if vix < 12:
        return "bearish", 0.65  # Too complacent
    elif vix < 15:
        return "neutral", 0.50  # Low vol, normal
    elif vix < 20:
        return "neutral", 0.50  # Normal range
    elif vix < 25:
        return "bullish", 0.60  # Moderate fear = opportunity
    elif vix < 30:
        return "bullish", 0.70  # Elevated fear = good opportunity
    elif vix < 40:
        return "bullish", 0.80  # High fear = strong opportunity
    else:
        return "bullish", 0.85  # Panic = best opportunity


@simple_agent("Market Momentum", weight=0.09)
def market_momentum_agent(ticker, context):
    """
    Analyze broad market momentum (S&P 500)

    Strategy:
    - Rising market = bullish tailwind
    - Falling market = bearish headwind
    - High beta stocks amplify market moves
    """
    macro = context.get_macro_indicators()
    beta = context.get_metric("beta")

    if not macro:
        return "neutral", 0.5

    sp500_change = macro.get("sp500_change", 0)

    # Adjust for beta
    effective_momentum = sp500_change * beta if beta > 0 else sp500_change

    # Market momentum signal
    if sp500_change > 1.5:
        base_signal = "bullish"
        base_confidence = 0.75
    elif sp500_change > 0.5:
        base_signal = "bullish"
        base_confidence = 0.65
    elif sp500_change > 0:
        base_signal = "neutral"
        base_confidence = 0.55
    elif sp500_change > -0.5:
        base_signal = "neutral"
        base_confidence = 0.50
    elif sp500_change > -1.5:
        base_signal = "bearish"
        base_confidence = 0.65
    else:
        base_signal = "bearish"
        base_confidence = 0.75

    # Beta adjustment
    if beta > 1.5:
        # High beta stocks are more sensitive
        if base_signal == "bullish":
            base_confidence += 0.05
        elif base_signal == "bearish":
            base_confidence += 0.05

    return base_signal, min(base_confidence, 0.90)


# =============================================================================
# COMMODITY & CURRENCY AGENTS
# =============================================================================


@simple_agent("Oil Price Impact", weight=0.07)
def oil_price_agent(ticker, context):
    """
    Analyze oil price impact on sectors

    Strategy:
    - Energy sector: High oil = bullish
    - Airlines, transportation: High oil = bearish
    - Most sectors: Stable oil = bullish
    """
    macro = context.get_macro_indicators()
    sector = context.get_metric("sector")

    if not macro:
        return "neutral", 0.5

    oil_price = macro.get("oil_price", 75)

    # Sector-specific oil sensitivity
    if sector == "Energy":
        # Energy benefits from high oil
        if oil_price > 90:
            return "bullish", 0.80
        elif oil_price > 75:
            return "bullish", 0.70
        elif oil_price < 60:
            return "bearish", 0.70
        else:
            return "neutral", 0.55

    elif sector in ["Airlines", "Transportation"]:
        # High oil hurts these sectors
        if oil_price > 90:
            return "bearish", 0.75
        elif oil_price > 80:
            return "bearish", 0.65
        elif oil_price < 60:
            return "bullish", 0.70
        else:
            return "neutral", 0.50

    elif sector in ["Automotive", "Retail"]:
        # Moderately sensitive
        if oil_price > 100:
            return "bearish", 0.60  # Hurts consumer spending
        elif oil_price < 50:
            return "bullish", 0.60  # Helps consumers
        else:
            return "neutral", 0.50

    else:
        # Most sectors prefer stable oil
        return "neutral", 0.50


@simple_agent("Dollar Strength Analyzer", weight=0.07)
def dollar_strength_agent(ticker, context):
    """
    Analyze USD strength impact

    Strategy:
    - Strong dollar hurts exporters
    - Strong dollar helps importers
    - Weak dollar helps multinationals
    """
    macro = context.get_macro_indicators()
    revenue = context.get_metric("revenue")
    sector = context.get_metric("sector")

    if not macro:
        return "neutral", 0.5

    dxy = macro.get("dxy", 103)  # Dollar Index

    # Determine dollar strength
    # DXY: 90-95 = weak, 95-105 = normal, 105+ = strong

    if dxy > 110:
        dollar_environment = "very_strong"
    elif dxy > 105:
        dollar_environment = "strong"
    elif dxy > 95:
        dollar_environment = "normal"
    elif dxy > 90:
        dollar_environment = "weak"
    else:
        dollar_environment = "very_weak"

    # Sector impact
    # Multinationals with international revenue hurt by strong dollar
    if sector in ["Technology", "Industrial"]:
        # Assume significant international exposure
        if dollar_environment in ["very_strong", "strong"]:
            return "bearish", 0.65
        elif dollar_environment in ["weak", "very_weak"]:
            return "bullish", 0.65

    # Domestic-focused companies less affected
    if sector in ["Utilities", "Banking", "Retail"]:
        return "neutral", 0.50

    return "neutral", 0.50


@simple_agent("Gold Safe Haven Monitor", weight=0.06)
def gold_safe_haven_agent(ticker, context):
    """
    Use gold as risk-off indicator

    Strategy:
    - Rising gold = risk-off, bearish for stocks
    - Falling gold = risk-on, bullish for stocks
    - Gold price reflects fear/uncertainty
    """
    macro = context.get_macro_indicators()
    sector = context.get_metric("sector")

    if not macro:
        return "neutral", 0.5

    gold_price = macro.get("gold_price", 2000)

    # Gold interpretation
    # $1800-2000 = normal
    # > $2200 = high fear
    # < $1700 = low fear

    if gold_price > 2300:
        # Extreme safe haven demand
        if sector in ["Utilities", "Consumer Staples"]:
            return "neutral", 0.55  # Defensive sectors okay
        else:
            return "bearish", 0.70  # Risk-off bad for growth

    elif gold_price > 2100:
        # Elevated safe haven demand
        return "bearish", 0.60

    elif gold_price < 1700:
        # Low safe haven demand (risk-on)
        return "bullish", 0.65

    elif gold_price < 1850:
        # Below average (moderate risk-on)
        return "bullish", 0.60

    else:
        # Normal range
        return "neutral", 0.50


# =============================================================================
# COMPOSITE MACRO AGENTS
# =============================================================================


@simple_agent("Macro Environment Score", weight=0.11)
def macro_environment_agent(ticker, context):
    """
    Composite macro environment assessment

    Strategy:
    - Combine all macro factors
    - Weight by importance
    - Generate overall macro score
    """
    macro = context.get_macro_indicators()

    if not macro:
        return "neutral", 0.5

    gdp = macro.get("gdp_growth", 0)
    unemployment = macro.get("unemployment_rate", 0)
    inflation = macro.get("inflation_rate", 0)
    vix = macro.get("vix_level", 15)
    treasury_10y = macro.get("treasury_10y", 0)
    treasury_2y = macro.get("treasury_2y", 0)

    score = 0

    # GDP (weight: 3)
    if gdp > 3.0:
        score += 3
    elif gdp > 2.5:
        score += 2
    elif gdp > 2.0:
        score += 1
    elif gdp < 1.0:
        score -= 2
    elif gdp < 0:
        score -= 3

    # Unemployment (weight: 2)
    if unemployment < 4.0:
        score += 2
    elif unemployment < 4.5:
        score += 1
    elif unemployment > 6.0:
        score -= 2
    elif unemployment > 5.5:
        score -= 1

    # Inflation (weight: 2)
    if 2.0 <= inflation <= 3.0:
        score += 2  # Goldilocks
    elif 1.5 <= inflation <= 3.5:
        score += 1  # Acceptable
    elif inflation > 5.0:
        score -= 2  # Too high
    elif inflation < 1.0:
        score -= 2  # Deflation risk

    # Yield curve (weight: 2)
    yield_spread = treasury_10y - treasury_2y
    if yield_spread > 1.0:
        score += 2
    elif yield_spread > 0.5:
        score += 1
    elif yield_spread < -0.2:
        score -= 2
    elif yield_spread < 0:
        score -= 1

    # VIX (weight: 1, contrarian)
    if 20 <= vix <= 30:
        score += 1  # Fear = opportunity
    elif vix < 12:
        score -= 1  # Complacency

    # Decision
    if score >= 8:
        return "bullish", 0.85
    elif score >= 5:
        return "bullish", 0.75
    elif score >= 3:
        return "bullish", 0.65
    elif score >= 0:
        return "neutral", 0.55
    elif score >= -3:
        return "bearish", 0.65
    elif score >= -5:
        return "bearish", 0.75
    else:
        return "bearish", 0.85


# =============================================================================
# REGISTRATION
# =============================================================================


def register_macro_agents():
    """Register all macro agents"""
    from agent_builder.agents.registry import get_registry

    registry = get_registry()

    # Economic cycle agents
    registry.register(economic_cycle_agent.agent, tags=["macro", "cycle"])
    registry.register(recession_predictor_agent.agent, tags=["macro", "cycle"])

    # Interest rate agents
    registry.register(interest_rate_sensitivity_agent.agent, tags=["macro", "rates"])
    registry.register(fed_policy_agent.agent, tags=["macro", "rates"])
    registry.register(yield_curve_agent.agent, tags=["macro", "rates"])

    # Inflation agents
    registry.register(inflation_monitor_agent.agent, tags=["macro", "inflation"])
    registry.register(pricing_power_agent.agent, tags=["macro", "inflation"])

    # Market sentiment agents
    registry.register(vix_fear_gauge_agent.agent, tags=["macro", "sentiment"])
    registry.register(market_momentum_agent.agent, tags=["macro", "sentiment"])

    # Commodity & currency agents
    registry.register(oil_price_agent.agent, tags=["macro", "commodities"])
    registry.register(dollar_strength_agent.agent, tags=["macro", "currency"])
    registry.register(gold_safe_haven_agent.agent, tags=["macro", "commodities"])

    # Composite agent
    registry.register(macro_environment_agent.agent, tags=["macro", "composite"])

    logger.info("✅ Registered 13 macro agents")


if __name__ == "__main__":
    # Test agents
    from agent_builder.agents.context import AgentContext

    context = AgentContext("AAPL")

    print("Testing macro agents on AAPL:")
    print("-" * 60)

    agents = [
        economic_cycle_agent,
        recession_predictor_agent,
        interest_rate_sensitivity_agent,
        vix_fear_gauge_agent,
        macro_environment_agent,
    ]

    for agent_func in agents:
        signal, confidence = agent_func("AAPL", context)
        print(f"{agent_func.__name__:35s} {signal:8s} ({confidence:.2f})")
