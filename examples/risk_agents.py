"""
Risk Analysis Agents
Focus on volatility, downside protection, risk-adjusted returns, and portfolio risk
"""

from agent_builder.agents import simple_agent
from agent_builder.repositories.connection import get_db_cursor
import logging

logger = logging.getLogger(__name__)


# =============================================================================
# VOLATILITY RISK AGENTS
# =============================================================================


@simple_agent("Volatility Risk Monitor", weight=0.10)
def volatility_risk_agent(ticker, context):
    """
    Monitor volatility levels and trends

    Strategy:
    - Low volatility = stable, prefer for risk-off
    - High volatility = risky, avoid or trade carefully
    - Rising volatility = increasing risk
    """
    risk_metrics = context.get_latest_risk_metrics()

    if not risk_metrics:
        return "neutral", 0.5

    hist_vol_30d = risk_metrics.get("historical_volatility_30d", 0)
    hist_vol_90d = risk_metrics.get("historical_volatility_90d", 0)
    implied_vol = risk_metrics.get("implied_volatility", 0)

    # Volatility assessment
    # Low: < 15%, Moderate: 15-25%, High: 25-40%, Extreme: > 40%

    score = 0

    # Current volatility level
    if hist_vol_30d < 15:
        score += 2  # Low volatility = stable
    elif hist_vol_30d < 25:
        score += 1  # Moderate volatility
    elif hist_vol_30d < 40:
        score -= 1  # High volatility = risk
    else:
        score -= 3  # Extreme volatility = high risk

    # Volatility trend (30d vs 90d)
    if hist_vol_90d > 0:
        vol_change = ((hist_vol_30d - hist_vol_90d) / hist_vol_90d) * 100
        if vol_change > 30:
            score -= 2  # Rapidly increasing volatility
        elif vol_change > 15:
            score -= 1  # Rising volatility
        elif vol_change < -15:
            score += 1  # Falling volatility (stabilizing)

    # Implied vs historical (fear gauge)
    if implied_vol > 0 and hist_vol_30d > 0:
        iv_hv_ratio = implied_vol / hist_vol_30d
        if iv_hv_ratio > 1.3:
            score -= 1  # Market pricing more risk than realized
        elif iv_hv_ratio < 0.8:
            score += 1  # Market complacent (contrarian positive)

    # Decision
    if score >= 3:
        return "bullish", 0.80  # Low stable volatility
    elif score >= 1:
        return "bullish", 0.65  # Acceptable volatility
    elif score >= -1:
        return "neutral", 0.55  # Moderate risk
    elif score >= -3:
        return "bearish", 0.70  # High volatility risk
    else:
        return "bearish", 0.85  # Extreme volatility risk


@simple_agent("Volatility Regime Shift", weight=0.09)
def volatility_regime_agent(ticker, context):
    """
    Detect volatility regime changes

    Strategy:
    - Shift from low to high vol = risk increase, bearish
    - Shift from high to low vol = stabilizing, bullish
    - Persistent high vol = avoid
    """
    # Get multiple risk metric points
    with get_db_cursor() as cursor:
        if cursor is None:
            return "neutral", 0.5

        cursor.execute(
            """
            SELECT historical_volatility_30d, date
            FROM mock_risk_metrics
            WHERE ticker = %s
            ORDER BY date DESC
            LIMIT 10
        """,
            (ticker,),
        )

        results = cursor.fetchall()

        if len(results) < 5:
            return "neutral", 0.5

        vols = [r[0] for r in results if r[0] is not None]

        if len(vols) < 5:
            return "neutral", 0.5

        # Recent vs older volatility
        recent_avg_vol = sum(vols[:3]) / 3
        older_avg_vol = sum(vols[-3:]) / 3

        # Detect regime shift
        if older_avg_vol > 0:
            vol_change_pct = ((recent_avg_vol - older_avg_vol) / older_avg_vol) * 100
        else:
            vol_change_pct = 0

        # Classify regimes
        # Low: < 20%, Moderate: 20-30%, High: > 30%
        recent_regime = (
            "low"
            if recent_avg_vol < 20
            else "moderate" if recent_avg_vol < 30 else "high"
        )
        older_regime = (
            "low"
            if older_avg_vol < 20
            else "moderate" if older_avg_vol < 30 else "high"
        )

        # Decision based on regime transition
        if recent_regime == "low" and older_regime == "high":
            return "bullish", 0.85  # Stabilizing from high vol
        elif recent_regime == "low" and older_regime == "moderate":
            return "bullish", 0.70  # Stabilizing
        elif recent_regime == "low":
            return "bullish", 0.65  # Stable low vol
        elif recent_regime == "high" and older_regime == "low":
            return "bearish", 0.85  # Destabilizing
        elif recent_regime == "high" and older_regime == "moderate":
            return "bearish", 0.75  # Increasing volatility
        elif recent_regime == "high":
            return "bearish", 0.80  # Persistent high vol
        else:
            return "neutral", 0.50


# =============================================================================
# DOWNSIDE RISK AGENTS
# =============================================================================


@simple_agent("Downside Protection", weight=0.11)
def downside_protection_agent(ticker, context):
    """
    Focus on downside risk and capital preservation

    Strategy:
    - Low max drawdown = good downside protection
    - Good VaR metrics = limited tail risk
    - Prioritize capital preservation
    """
    risk_metrics = context.get_latest_risk_metrics()

    if not risk_metrics:
        return "neutral", 0.5

    max_drawdown = risk_metrics.get("max_drawdown", 0)
    var_95 = risk_metrics.get("value_at_risk_95", 0)
    var_99 = risk_metrics.get("value_at_risk_99", 0)

    score = 0

    # Max drawdown analysis (lower is better)
    if max_drawdown > -10:
        score += 3  # Very low drawdown
    elif max_drawdown > -15:
        score += 2  # Low drawdown
    elif max_drawdown > -20:
        score += 1  # Acceptable drawdown
    elif max_drawdown < -40:
        score -= 3  # Severe drawdown risk
    elif max_drawdown < -30:
        score -= 2  # High drawdown risk
    elif max_drawdown < -25:
        score -= 1  # Moderate drawdown risk

    # Value at Risk (95% confidence)
    if var_95 > -2:
        score += 2  # Very low daily risk
    elif var_95 > -3:
        score += 1  # Low daily risk
    elif var_95 < -6:
        score -= 2  # High daily risk
    elif var_95 < -5:
        score -= 1  # Moderate daily risk

    # Tail risk (99% VaR - extreme events)
    if var_99 > -5:
        score += 1  # Low tail risk
    elif var_99 < -10:
        score -= 2  # High tail risk
    elif var_99 < -8:
        score -= 1  # Moderate tail risk

    # Decision
    if score >= 5:
        return "bullish", 0.85  # Excellent downside protection
    elif score >= 3:
        return "bullish", 0.75  # Good downside protection
    elif score >= 1:
        return "bullish", 0.65  # Acceptable risk
    elif score >= -1:
        return "neutral", 0.55  # Moderate risk
    elif score >= -3:
        return "bearish", 0.70  # Concerning risk
    else:
        return "bearish", 0.85  # High downside risk


@simple_agent("Tail Risk Monitor", weight=0.09)
def tail_risk_agent(ticker, context):
    """
    Monitor extreme event risk (fat tails)

    Strategy:
    - Large gap between VaR 95% and 99% = fat tails, risky
    - VaR 99% < -10% = extreme tail risk
    - Recent large drawdowns = elevated risk
    """
    risk_metrics = context.get_latest_risk_metrics()

    if not risk_metrics:
        return "neutral", 0.5

    var_95 = risk_metrics.get("value_at_risk_95", 0)
    var_99 = risk_metrics.get("value_at_risk_99", 0)
    max_drawdown = risk_metrics.get("max_drawdown", 0)
    return_1m = risk_metrics.get("return_1m", 0)

    # Tail risk indicators
    risk_signals = 0

    # Extreme VaR 99%
    if var_99 < -12:
        risk_signals += 3  # Very high tail risk
    elif var_99 < -10:
        risk_signals += 2  # High tail risk
    elif var_99 < -8:
        risk_signals += 1  # Moderate tail risk

    # Fat tail detection (gap between VaR levels)
    var_gap = abs(var_99 - var_95)
    if var_gap > 5:
        risk_signals += 2  # Fat tails (extreme events likely)
    elif var_gap > 3:
        risk_signals += 1  # Moderate tail risk

    # Recent severe drawdown
    if max_drawdown < -50:
        risk_signals += 2  # History of severe losses
    elif max_drawdown < -40:
        risk_signals += 1

    # Recent sharp decline
    if return_1m < -15:
        risk_signals += 1  # Currently experiencing drawdown

    # Decision
    if risk_signals == 0:
        return "bullish", 0.75  # Low tail risk
    elif risk_signals <= 2:
        return "neutral", 0.55  # Moderate tail risk
    elif risk_signals <= 4:
        return "bearish", 0.70  # High tail risk
    else:
        return "bearish", 0.85  # Extreme tail risk


# =============================================================================
# RISK-ADJUSTED RETURN AGENTS
# =============================================================================


@simple_agent("Sharpe Ratio Analyzer", weight=0.11)
def sharpe_ratio_agent(ticker, context):
    """
    Analyze risk-adjusted returns via Sharpe ratio

    Strategy:
    - Sharpe > 2.0 = excellent risk-adjusted returns
    - Sharpe > 1.0 = good risk-adjusted returns
    - Sharpe < 0.5 = poor risk-adjusted returns
    - Negative Sharpe = losing money
    """
    risk_metrics = context.get_latest_risk_metrics()

    if not risk_metrics:
        return "neutral", 0.5

    sharpe_ratio = risk_metrics.get("sharpe_ratio", 0)
    sortino_ratio = risk_metrics.get("sortino_ratio", 0)
    return_ytd = risk_metrics.get("return_ytd", 0)

    # Sharpe ratio interpretation
    if sharpe_ratio > 2.5:
        return "bullish", 0.90  # Exceptional risk-adjusted returns
    elif sharpe_ratio > 2.0:
        return "bullish", 0.85  # Excellent risk-adjusted returns
    elif sharpe_ratio > 1.5:
        return "bullish", 0.75  # Very good risk-adjusted returns
    elif sharpe_ratio > 1.0:
        return "bullish", 0.70  # Good risk-adjusted returns
    elif sharpe_ratio > 0.5:
        return "bullish", 0.60  # Acceptable risk-adjusted returns
    elif sharpe_ratio > 0:
        return "neutral", 0.55  # Marginal risk-adjusted returns
    elif sharpe_ratio > -0.5:
        return "bearish", 0.65  # Poor risk-adjusted returns
    else:
        return "bearish", 0.80  # Very poor risk-adjusted returns


@simple_agent("Sortino Ratio Focus", weight=0.09)
def sortino_ratio_agent(ticker, context):
    """
    Analyze downside risk-adjusted returns (Sortino)

    Strategy:
    - Sortino focuses on downside deviation (better than Sharpe)
    - Sortino > Sharpe = asymmetric returns (good)
    - High Sortino = good downside protection with upside
    """
    risk_metrics = context.get_latest_risk_metrics()

    if not risk_metrics:
        return "neutral", 0.5

    sharpe_ratio = risk_metrics.get("sharpe_ratio", 0)
    sortino_ratio = risk_metrics.get("sortino_ratio", 0)

    # Sortino interpretation
    score = 0

    # Absolute Sortino level
    if sortino_ratio > 2.5:
        score += 3
    elif sortino_ratio > 2.0:
        score += 2
    elif sortino_ratio > 1.5:
        score += 1
    elif sortino_ratio < 0:
        score -= 2
    elif sortino_ratio < 0.5:
        score -= 1

    # Sortino vs Sharpe comparison (asymmetry)
    if sharpe_ratio > 0 and sortino_ratio > 0:
        ratio_diff = sortino_ratio - sharpe_ratio
        if ratio_diff > 0.5:
            score += 2  # Strong asymmetry (more upside than downside)
        elif ratio_diff > 0.2:
            score += 1  # Good asymmetry
        elif ratio_diff < -0.2:
            score -= 1  # Negative asymmetry (concerning)

    # Decision
    if score >= 4:
        return "bullish", 0.85
    elif score >= 2:
        return "bullish", 0.75
    elif score >= 0:
        return "neutral", 0.60
    elif score >= -2:
        return "bearish", 0.70
    else:
        return "bearish", 0.80


@simple_agent("Return Quality Analyzer", weight=0.10)
def return_quality_agent(ticker, context):
    """
    Analyze quality of returns (consistency and risk-adjustment)

    Strategy:
    - Positive returns with low volatility = high quality
    - High returns with high volatility = low quality
    - Consistent returns = high quality
    """
    risk_metrics = context.get_latest_risk_metrics()

    if not risk_metrics:
        return "neutral", 0.5

    return_3m = risk_metrics.get("return_3m", 0)
    return_ytd = risk_metrics.get("return_ytd", 0)
    hist_vol = risk_metrics.get("historical_volatility_30d", 0)
    sharpe = risk_metrics.get("sharpe_ratio", 0)
    max_drawdown = risk_metrics.get("max_drawdown", 0)

    score = 0

    # Positive returns
    if return_3m > 10:
        score += 2
    elif return_3m > 5:
        score += 1
    elif return_3m < -10:
        score -= 2
    elif return_3m < -5:
        score -= 1

    # Low volatility (for given returns)
    if return_3m > 0 and hist_vol < 20:
        score += 2  # Good returns with low vol = high quality
    elif return_3m > 0 and hist_vol < 30:
        score += 1
    elif return_3m < 0 and hist_vol > 40:
        score -= 2  # Losing money with high vol = worst

    # Sharpe ratio (overall quality)
    if sharpe > 1.5:
        score += 2
    elif sharpe > 1.0:
        score += 1
    elif sharpe < 0:
        score -= 2

    # Limited drawdowns
    if max_drawdown > -15:
        score += 1
    elif max_drawdown < -30:
        score -= 1

    # Decision
    if score >= 6:
        return "bullish", 0.85  # High quality returns
    elif score >= 4:
        return "bullish", 0.75  # Good quality
    elif score >= 2:
        return "bullish", 0.65  # Acceptable quality
    elif score >= 0:
        return "neutral", 0.55  # Mixed quality
    elif score >= -2:
        return "bearish", 0.65  # Poor quality
    else:
        return "bearish", 0.80  # Very poor quality


# =============================================================================
# CORRELATION & PORTFOLIO RISK AGENTS
# =============================================================================


@simple_agent("Market Correlation Risk", weight=0.09)
def correlation_risk_agent(ticker, context):
    """
    Analyze correlation with market (S&P 500)

    Strategy:
    - Low correlation = good diversifier
    - High correlation + high beta = market amplifier (risky)
    - Correlation changes = risk regime shift
    """
    risk_metrics = context.get_latest_risk_metrics()
    fundamentals = context.get_fundamentals()

    if not risk_metrics:
        return "neutral", 0.5

    correlation = risk_metrics.get("correlation_sp500", 0.5)
    beta = fundamentals.get("beta", 1.0)

    score = 0

    # Correlation assessment
    if abs(correlation) < 0.3:
        score += 2  # Good diversifier
    elif abs(correlation) < 0.6:
        score += 1  # Moderate diversification
    elif abs(correlation) > 0.9:
        score -= 1  # Highly correlated (no diversification)

    # Beta assessment (market sensitivity)
    if beta < 0.8:
        score += 1  # Defensive
    elif beta > 1.5 and correlation > 0.8:
        score -= 2  # High beta + high correlation = risky
    elif beta > 1.3:
        score -= 1  # Aggressive

    # Combination assessment
    # High correlation + high beta = market amplifier (risk in downturns)
    if correlation > 0.8 and beta > 1.5:
        return "bearish", 0.70  # Will amplify market declines

    # Low correlation = good diversifier
    if abs(correlation) < 0.4:
        return "bullish", 0.70  # Portfolio diversification benefit

    # Decision based on score
    if score >= 3:
        return "bullish", 0.75
    elif score >= 1:
        return "bullish", 0.65
    elif score >= -1:
        return "neutral", 0.55
    else:
        return "bearish", 0.65


@simple_agent("Beta Risk Analyzer", weight=0.08)
def beta_risk_agent(ticker, context):
    """
    Analyze systematic risk via beta

    Strategy:
    - Low beta (< 1) = defensive, lower risk
    - High beta (> 1) = aggressive, higher risk
    - In bull markets: prefer high beta
    - In bear markets: prefer low beta
    """
    fundamentals = context.get_fundamentals()
    macro = context.get_macro_indicators()

    beta = fundamentals.get("beta", 1.0)

    # Get market direction
    if macro:
        sp500_change = macro.get("sp500_change", 0)
        market_direction = (
            "bullish"
            if sp500_change > 0.5
            else "bearish" if sp500_change < -0.5 else "neutral"
        )
    else:
        market_direction = "neutral"

    # Beta interpretation depends on market environment
    if market_direction == "bullish":
        # In bull market, high beta is good
        if beta > 1.5:
            return "bullish", 0.75  # Leverage market upside
        elif beta > 1.2:
            return "bullish", 0.65
        elif beta < 0.8:
            return "neutral", 0.55  # Missing upside
        else:
            return "neutral", 0.50

    elif market_direction == "bearish":
        # In bear market, low beta is good
        if beta < 0.8:
            return "bullish", 0.75  # Defensive protection
        elif beta < 1.0:
            return "bullish", 0.65
        elif beta > 1.5:
            return "bearish", 0.75  # Will amplify losses
        elif beta > 1.2:
            return "bearish", 0.65
        else:
            return "neutral", 0.50

    else:
        # Neutral market: moderate beta preferred
        if 0.8 <= beta <= 1.2:
            return "neutral", 0.55  # Balanced
        elif beta > 1.5:
            return "bearish", 0.60  # High systematic risk
        elif beta < 0.6:
            return "neutral", 0.55  # Very defensive
        else:
            return "neutral", 0.50


# =============================================================================
# OPTIONS IMPLIED RISK AGENTS
# =============================================================================


@simple_agent("Put/Call Ratio Signal", weight=0.09)
def put_call_ratio_agent(ticker, context):
    """
    Options market sentiment via put/call ratio

    Strategy:
    - High P/C ratio (> 1.2) = excessive fear, contrarian bullish
    - Low P/C ratio (< 0.7) = complacency, contrarian bearish
    - Normal P/C (0.8-1.0) = balanced sentiment
    """
    options_data = context.get_latest_options_data()

    if not options_data:
        return "neutral", 0.5

    pc_ratio = options_data.get("put_call_ratio", 0.9)

    # Put/Call ratio interpretation (contrarian)
    if pc_ratio > 1.5:
        return "bullish", 0.85  # Extreme fear = opportunity
    elif pc_ratio > 1.2:
        return "bullish", 0.75  # High fear = buy signal
    elif pc_ratio > 1.0:
        return "bullish", 0.65  # Moderate fear
    elif pc_ratio < 0.6:
        return "bearish", 0.75  # Extreme complacency = risk
    elif pc_ratio < 0.7:
        return "bearish", 0.65  # Complacency = caution
    elif pc_ratio < 0.8:
        return "neutral", 0.55  # Slightly optimistic
    else:
        return "neutral", 0.50  # Normal range


@simple_agent("Implied Volatility Premium", weight=0.08)
def iv_premium_agent(ticker, context):
    """
    Compare implied vs historical volatility

    Strategy:
    - IV >> HV = market pricing high risk (fear)
    - IV << HV = market complacent
    - High IV premium can be contrarian bullish
    """
    risk_metrics = context.get_latest_risk_metrics()

    if not risk_metrics:
        return "neutral", 0.5

    hist_vol = risk_metrics.get("historical_volatility_30d", 0)
    impl_vol = risk_metrics.get("implied_volatility", 0)

    if hist_vol <= 0 or impl_vol <= 0:
        return "neutral", 0.5

    # IV / HV ratio
    iv_hv_ratio = impl_vol / hist_vol

    # Premium interpretation
    if iv_hv_ratio > 1.5:
        return "bullish", 0.75  # Market pricing excessive risk (contrarian)
    elif iv_hv_ratio > 1.3:
        return "bullish", 0.65  # Elevated fear premium
    elif iv_hv_ratio > 1.1:
        return "neutral", 0.55  # Slight premium
    elif iv_hv_ratio < 0.7:
        return "bearish", 0.70  # Complacency (risk not priced)
    elif iv_hv_ratio < 0.85:
        return "bearish", 0.60  # Market underpricing risk
    else:
        return "neutral", 0.50  # Fair pricing


# =============================================================================
# COMPOSITE RISK AGENT
# =============================================================================


@simple_agent("Comprehensive Risk Score", weight=0.12)
def comprehensive_risk_agent(ticker, context):
    """
    Aggregate all risk factors into comprehensive score

    Strategy:
    - Combine volatility, downside risk, risk-adjusted returns
    - Weight by importance
    - Generate overall risk assessment
    """
    risk_metrics = context.get_latest_risk_metrics()
    fundamentals = context.get_fundamentals()

    if not risk_metrics:
        return "neutral", 0.5

    # Extract all risk metrics
    hist_vol = risk_metrics.get("historical_volatility_30d", 0)
    max_drawdown = risk_metrics.get("max_drawdown", 0)
    var_95 = risk_metrics.get("value_at_risk_95", 0)
    sharpe = risk_metrics.get("sharpe_ratio", 0)
    sortino = risk_metrics.get("sortino_ratio", 0)
    correlation = risk_metrics.get("correlation_sp500", 0.5)
    return_3m = risk_metrics.get("return_3m", 0)
    beta = fundamentals.get("beta", 1.0)

    score = 0

    # Volatility (weight: 2)
    if hist_vol < 15:
        score += 2
    elif hist_vol < 25:
        score += 1
    elif hist_vol > 40:
        score -= 2
    elif hist_vol > 30:
        score -= 1

    # Downside protection (weight: 3)
    if max_drawdown > -15:
        score += 3
    elif max_drawdown > -20:
        score += 2
    elif max_drawdown > -25:
        score += 1
    elif max_drawdown < -40:
        score -= 3
    elif max_drawdown < -35:
        score -= 2
    elif max_drawdown < -30:
        score -= 1

    # VaR (weight: 2)
    if var_95 > -3:
        score += 2
    elif var_95 > -4:
        score += 1
    elif var_95 < -6:
        score -= 2
    elif var_95 < -5:
        score -= 1

    # Risk-adjusted returns (weight: 3)
    if sharpe > 2.0:
        score += 3
    elif sharpe > 1.5:
        score += 2
    elif sharpe > 1.0:
        score += 1
    elif sharpe < 0:
        score -= 3
    elif sharpe < 0.5:
        score -= 1

    # Returns (weight: 1)
    if return_3m > 10:
        score += 1
    elif return_3m < -10:
        score -= 1

    # Beta risk (weight: 1)
    if beta < 0.8:
        score += 1  # Defensive
    elif beta > 1.5:
        score -= 1  # Aggressive

    # Diversification benefit (weight: 1)
    if abs(correlation) < 0.4:
        score += 1  # Good diversifier

    # Decision
    if score >= 10:
        return "bullish", 0.90  # Excellent risk profile
    elif score >= 7:
        return "bullish", 0.85  # Very good risk profile
    elif score >= 4:
        return "bullish", 0.75  # Good risk profile
    elif score >= 2:
        return "bullish", 0.65  # Acceptable risk
    elif score >= 0:
        return "neutral", 0.55  # Moderate risk
    elif score >= -3:
        return "bearish", 0.65  # Elevated risk
    elif score >= -6:
        return "bearish", 0.75  # High risk
    else:
        return "bearish", 0.85  # Very high risk


# =============================================================================
# REGISTRATION
# =============================================================================


def register_risk_agents():
    """Register all risk agents"""
    from agent_builder.agents.registry import get_registry

    registry = get_registry()

    # Volatility agents
    registry.register(volatility_risk_agent.agent, tags=["risk", "volatility"])
    registry.register(volatility_regime_agent.agent, tags=["risk", "volatility"])

    # Downside risk agents
    registry.register(downside_protection_agent.agent, tags=["risk", "downside"])
    registry.register(tail_risk_agent.agent, tags=["risk", "tail"])

    # Risk-adjusted return agents
    registry.register(sharpe_ratio_agent.agent, tags=["risk", "adjusted_returns"])
    registry.register(sortino_ratio_agent.agent, tags=["risk", "adjusted_returns"])
    registry.register(return_quality_agent.agent, tags=["risk", "quality"])

    # Correlation agents
    registry.register(correlation_risk_agent.agent, tags=["risk", "correlation"])
    registry.register(beta_risk_agent.agent, tags=["risk", "beta"])

    # Options risk agents
    registry.register(put_call_ratio_agent.agent, tags=["risk", "options"])
    registry.register(iv_premium_agent.agent, tags=["risk", "options"])

    # Composite agent
    registry.register(comprehensive_risk_agent.agent, tags=["risk", "composite"])

    logger.info("✅ Registered 12 risk agents")


if __name__ == "__main__":
    # Test agents
    from agent_builder.agents.context import AgentContext

    context = AgentContext("AAPL")

    print("Testing risk agents on AAPL:")
    print("-" * 60)

    agents = [
        volatility_risk_agent,
        downside_protection_agent,
        sharpe_ratio_agent,
        correlation_risk_agent,
        comprehensive_risk_agent,
    ]

    for agent_func in agents:
        signal, confidence = agent_func("AAPL", context)
        print(f"{agent_func.__name__:35s} {signal:8s} ({confidence:.2f})")
