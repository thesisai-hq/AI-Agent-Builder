"""
Advanced Macro Economic Analyst Agent

Analyzes macroeconomic conditions and their impact on stocks/sectors using:
1. Economic indicator analysis (Fed rate, inflation, GDP, employment)
2. Market regime detection (bull/bear/risk-on/risk-off)
3. Sector rotation recommendations
4. LLM-powered synthesis of macro outlook

References business cycle theory, monetary policy impact, and sector rotation strategies.
"""

from typing import Dict, Any, Tuple, List, Optional
import logging
from datetime import datetime
from agent_builder import agent, get_registry
from agent_builder.llm import get_llm_provider, PromptTemplates

logger = logging.getLogger(__name__)


# ============================================================================
# ADVANCED MACRO ANALYST AGENT
# ============================================================================


@agent("Advanced Macro Analyst", "Comprehensive macroeconomic analysis with AI")
def advanced_macro_analyst(ticker: str, context) -> Tuple[str, float, str]:
    """
    Multi-stage macro economic analysis:

    Stage 1: Economic Indicator Analysis (Fed, Inflation, Growth, Employment)
    Stage 2: Market Regime Detection (Bull/Bear/Risk-On/Risk-Off)
    Stage 3: Sector Impact Analysis (How macro affects this sector)
    Stage 4: LLM Synthesis (AI-powered macro outlook)
    Stage 5: Final Recommendation

    Returns: (signal, confidence, reasoning)
    """

    print(f"\n{'='*70}")
    print(f"ADVANCED MACRO ECONOMIC ANALYSIS: {ticker}")
    print(f"{'='*70}\n")

    # Get company sector for context
    fundamentals = context.get_fundamentals()
    sector = fundamentals.get("sector", "Unknown") if fundamentals else "Unknown"

    # ========================================================================
    # STAGE 1: ECONOMIC INDICATOR ANALYSIS
    # ========================================================================

    print("📊 Stage 1: Economic Indicator Analysis...")
    econ_result = analyze_economic_indicators(context)

    print(f"   Economic Score: {econ_result['score']:.1f}/10")
    print(f"   Stance: {econ_result['stance']}")
    print(f"   Key factors: {', '.join(econ_result['key_factors'][:3])}")

    # ========================================================================
    # STAGE 2: MARKET REGIME DETECTION
    # ========================================================================

    print("\n📈 Stage 2: Market Regime Detection...")
    regime_result = detect_market_regime(context)

    print(f"   Regime: {regime_result['regime']}")
    print(f"   Confidence: {regime_result['confidence']:.0%}")
    print(f"   Characteristics: {', '.join(regime_result['characteristics'])}")

    # ========================================================================
    # STAGE 3: SECTOR IMPACT ANALYSIS
    # ========================================================================

    print(f"\n🏭 Stage 3: Sector Impact Analysis ({sector})...")
    sector_result = analyze_sector_impact(sector, econ_result, regime_result)

    print(f"   Sector outlook: {sector_result['outlook']}")
    print(f"   Favorability: {sector_result['favorability']}")
    print(f"   Reasoning: {sector_result['reasoning'][:80]}...")

    # ========================================================================
    # STAGE 4: LLM SYNTHESIS
    # ========================================================================

    print("\n🤖 Stage 4: AI Macro Synthesis...")
    synthesis = synthesize_macro_outlook_with_llm(
        ticker, sector, econ_result, regime_result, sector_result, context
    )

    if synthesis["success"]:
        print(f"   AI Signal: {synthesis['signal']}")
        print(f"   AI Confidence: {synthesis['confidence']:.0%}")
        print(f"   Macro View: {synthesis['reasoning'][:80]}...")
    else:
        print(f"   AI synthesis unavailable: {synthesis['error']}")

    # ========================================================================
    # STAGE 5: FINAL RECOMMENDATION
    # ========================================================================

    print("\n🎯 Stage 5: Final Macro Recommendation...")
    final_signal, final_confidence, final_reasoning = calculate_macro_recommendation(
        ticker, sector, econ_result, regime_result, sector_result, synthesis
    )

    print(f"\n{'='*70}")
    print(f"FINAL MACRO SIGNAL: {final_signal.upper()}")
    print(f"Confidence: {final_confidence:.0%}")
    print(f"{'='*70}\n")

    return final_signal, final_confidence, final_reasoning


# ============================================================================
# STAGE 1: ECONOMIC INDICATOR ANALYSIS
# ============================================================================


def analyze_economic_indicators(context) -> Dict[str, Any]:
    """
    Analyze key economic indicators

    Indicators analyzed:
    - Federal Funds Rate (Monetary policy stance)
    - Inflation (CPI) (Price stability)
    - GDP Growth (Economic growth)
    - Unemployment (Labor market health)
    - 10Y Treasury Yield (Risk-free rate, recession signal)
    - VIX (Market fear gauge)

    Scoring: Each indicator scored 0-2, total 0-10

    References:
    - Taylor Rule for Fed policy assessment
    - Yield curve inversion as recession predictor (Estrella & Mishkin, 1998)
    - VIX levels and market returns (Whaley, 2000)
    """

    indicators = context.get_macro_indicators()

    if not indicators:
        return {
            "score": 5.0,
            "stance": "neutral",
            "key_factors": ["No macro data available"],
            "detailed_scores": {},
            "bullish_factors": [],
            "bearish_factors": [],
        }

    # Parse indicators into dict
    macro_data = {}
    for ind in indicators:
        name = ind.get("indicator_name", "")
        macro_data[name] = {
            "value": ind.get("value", 0),
            "previous": ind.get("previous_value", 0),
            "change": ind.get("value", 0) - ind.get("previous_value", 0),
            "date": ind.get("date"),
        }

    scores = {}
    bullish_factors = []
    bearish_factors = []

    # ========================================================================
    # 1. FEDERAL FUNDS RATE (Monetary Policy)
    # ========================================================================

    # Thresholds based on Taylor Rule and historical data
    # Source: Taylor (1993), Fed historical data

    ffr = macro_data.get("Federal Funds Rate", {})
    if ffr:
        rate = ffr["value"]
        change = ffr["change"]

        # Scoring logic
        if rate < 2.0:
            scores["fed_policy"] = 2  # Very accommodative - bullish
            bullish_factors.append(f"Very low Fed rate ({rate:.2f}%)")
        elif rate < 3.5:
            scores["fed_policy"] = 1.5  # Accommodative
            bullish_factors.append(f"Accommodative Fed policy ({rate:.2f}%)")
        elif rate < 5.0:
            scores["fed_policy"] = 1  # Neutral
        elif rate < 6.0:
            scores["fed_policy"] = 0.5  # Restrictive
            bearish_factors.append(f"Restrictive Fed policy ({rate:.2f}%)")
        else:
            scores["fed_policy"] = 0  # Very restrictive - bearish
            bearish_factors.append(f"Very high Fed rate ({rate:.2f}%)")

        # Rate direction matters more than level sometimes
        if change < -0.25:
            scores["fed_policy"] += 0.5  # Cutting = bullish
            bullish_factors.append("Fed cutting rates")
        elif change > 0.25:
            scores["fed_policy"] -= 0.5  # Hiking = bearish
            bearish_factors.append("Fed hiking rates")

    # ========================================================================
    # 2. INFLATION (CPI)
    # ========================================================================

    # Thresholds based on Fed's 2% target
    # Source: Federal Reserve policy framework

    cpi = macro_data.get("Consumer Price Index", {})
    if cpi:
        inflation = cpi["value"]
        change = cpi["change"]

        if inflation < 2.0:
            scores["inflation"] = 2  # Below target - good
            bullish_factors.append(f"Low inflation ({inflation:.1f}%)")
        elif inflation < 2.5:
            scores["inflation"] = 1.5  # Near target
            bullish_factors.append("Inflation near target")
        elif inflation < 3.5:
            scores["inflation"] = 1  # Moderate
        elif inflation < 5.0:
            scores["inflation"] = 0.5  # Elevated
            bearish_factors.append(f"Elevated inflation ({inflation:.1f}%)")
        else:
            scores["inflation"] = 0  # High - bearish
            bearish_factors.append(f"High inflation ({inflation:.1f}%)")

        # Falling inflation is good
        if change < -0.5:
            scores["inflation"] += 0.5
            bullish_factors.append("Disinflation trend")

    # ========================================================================
    # 3. GDP GROWTH
    # ========================================================================

    # Thresholds based on long-term US GDP growth (~2-3%)
    # Source: BEA historical data, Ibbotson Associates

    gdp = macro_data.get("GDP Growth Rate", {})
    if gdp:
        growth = gdp["value"]

        if growth > 3.5:
            scores["gdp"] = 2  # Strong growth
            bullish_factors.append(f"Strong GDP growth ({growth:.1f}%)")
        elif growth > 2.5:
            scores["gdp"] = 1.5  # Above trend
            bullish_factors.append(f"Above-trend growth ({growth:.1f}%)")
        elif growth > 1.5:
            scores["gdp"] = 1  # Trend growth
        elif growth > 0:
            scores["gdp"] = 0.5  # Weak
            bearish_factors.append(f"Weak GDP growth ({growth:.1f}%)")
        else:
            scores["gdp"] = 0  # Recession
            bearish_factors.append(f"GDP contraction ({growth:.1f}%)")

    # ========================================================================
    # 4. UNEMPLOYMENT RATE
    # ========================================================================

    # Thresholds based on NAIRU (non-accelerating inflation rate)
    # Source: CBO estimates (~4-5% for US)

    unemployment = macro_data.get("Unemployment Rate", {})
    if unemployment:
        rate = unemployment["value"]
        change = unemployment["change"]

        if rate < 3.5:
            scores["employment"] = 2  # Very low - tight labor market
            bullish_factors.append(f"Very low unemployment ({rate:.1f}%)")
        elif rate < 4.5:
            scores["employment"] = 1.5  # Low
            bullish_factors.append(f"Low unemployment ({rate:.1f}%)")
        elif rate < 5.5:
            scores["employment"] = 1  # Normal
        elif rate < 7.0:
            scores["employment"] = 0.5  # Elevated
            bearish_factors.append(f"Rising unemployment ({rate:.1f}%)")
        else:
            scores["employment"] = 0  # High - recession signal
            bearish_factors.append(f"High unemployment ({rate:.1f}%)")

        # Rising unemployment is concerning
        if change > 0.5:
            scores["employment"] -= 0.5
            bearish_factors.append("Unemployment rising")

    # ========================================================================
    # 5. 10-YEAR TREASURY YIELD
    # ========================================================================

    # Yield curve analysis
    # Source: Estrella & Mishkin (1998) - yield curve predicts recessions

    treasury = macro_data.get("10-Year Treasury Yield", {})
    if treasury:
        yield_10y = treasury["value"]

        # High yields = attractive bonds, competition for stocks
        if yield_10y < 2.5:
            scores["treasury"] = (
                2  # Low yields favor stocks (TINA - There Is No Alternative)
            )
            bullish_factors.append("Low bond yields favor equities")
        elif yield_10y < 3.5:
            scores["treasury"] = 1.5
        elif yield_10y < 4.5:
            scores["treasury"] = 1  # Moderate competition
        elif yield_10y < 5.5:
            scores["treasury"] = 0.5
            bearish_factors.append(
                f"High bond yields ({yield_10y:.2f}%) compete with stocks"
            )
        else:
            scores["treasury"] = 0  # Very high - bonds very attractive
            bearish_factors.append(f"Very high bond yields ({yield_10y:.2f}%)")

    # ========================================================================
    # 6. VIX (VOLATILITY INDEX)
    # ========================================================================

    # VIX thresholds based on historical percentiles
    # Source: CBOE VIX White Paper, Whaley (2000)

    vix = macro_data.get("VIX Index", {})
    if vix:
        vix_level = vix["value"]

        if vix_level < 12:
            scores["vix"] = 2  # Very low fear - complacency warning
            bullish_factors.append(f"Very low VIX ({vix_level:.1f}) - calm market")
        elif vix_level < 15:
            scores["vix"] = 1.5  # Low fear
            bullish_factors.append(f"Low volatility (VIX {vix_level:.1f})")
        elif vix_level < 20:
            scores["vix"] = 1  # Normal
        elif vix_level < 30:
            scores["vix"] = 0.5  # Elevated fear
            bearish_factors.append(f"Elevated volatility (VIX {vix_level:.1f})")
        else:
            scores["vix"] = 0  # High fear - but contrarian opportunity
            # Note: Extreme VIX can be contrarian bullish
            if vix_level > 40:
                bearish_factors.append(
                    f"Extreme fear (VIX {vix_level:.1f}) - capitulation?"
                )
            else:
                bearish_factors.append(f"High market fear (VIX {vix_level:.1f})")

    # ========================================================================
    # CALCULATE OVERALL ECONOMIC SCORE
    # ========================================================================

    # Weighted average (Fed policy and GDP most important)
    weights = {
        "fed_policy": 0.30,  # Most important (drives everything)
        "inflation": 0.20,  # Affects Fed policy
        "gdp": 0.25,  # Economic health
        "employment": 0.15,  # Labor market
        "treasury": 0.05,  # Less important
        "vix": 0.05,  # Sentiment indicator
    }

    total_score = (
        sum(scores.get(k, 1.0) * weights[k] for k in weights) * 5
    )  # Scale to 0-10

    # Determine economic stance
    if total_score >= 7.0:
        stance = "expansionary"  # Strong economy, bullish
    elif total_score >= 5.0:
        stance = "neutral"
    else:
        stance = "contractionary"  # Weak economy, bearish

    return {
        "score": total_score,
        "stance": stance,
        "detailed_scores": scores,
        "bullish_factors": bullish_factors,
        "bearish_factors": bearish_factors,
        "key_factors": (
            bullish_factors[:3]
            if len(bullish_factors) > len(bearish_factors)
            else bearish_factors[:3]
        ),
        "macro_data": macro_data,
    }


# ============================================================================
# STAGE 2: MARKET REGIME DETECTION
# ============================================================================


def detect_market_regime(context) -> Dict[str, Any]:
    """
    Detect current market regime

    Regimes:
    - BULL MARKET: Low VIX, rising GDP, accommodative Fed
    - BEAR MARKET: High VIX, recession fears, restrictive Fed
    - RISK-ON: Low volatility, growth focus
    - RISK-OFF: High volatility, defensive focus
    - TRANSITIONAL: Mixed signals

    References:
    - Ang & Bekaert (2002) - Regime switching in equity returns
    - Guidolin & Timmermann (2008) - Bull and bear markets
    """

    indicators = context.get_macro_indicators()

    if not indicators:
        return {
            "regime": "unknown",
            "confidence": 0.3,
            "characteristics": ["Insufficient data"],
            "recommendations": [],
        }

    # Extract key metrics
    vix = None
    gdp = None
    fed_rate = None

    for ind in indicators:
        name = ind.get("indicator_name", "")
        if "VIX" in name:
            vix = ind.get("value", 0)
        elif "GDP" in name:
            gdp = ind.get("value", 0)
        elif "Federal Funds Rate" in name:
            fed_rate = ind.get("value", 0)

    # Regime detection logic
    characteristics = []
    regime_scores = {"bull": 0, "bear": 0, "risk_on": 0, "risk_off": 0}

    # VIX analysis
    if vix is not None:
        if vix < 15:
            regime_scores["bull"] += 2
            regime_scores["risk_on"] += 2
            characteristics.append("Low market volatility")
        elif vix < 20:
            regime_scores["bull"] += 1
            regime_scores["risk_on"] += 1
        elif vix < 30:
            regime_scores["bear"] += 1
            regime_scores["risk_off"] += 1
            characteristics.append("Elevated volatility")
        else:
            regime_scores["bear"] += 2
            regime_scores["risk_off"] += 2
            characteristics.append("High market fear")

    # GDP analysis
    if gdp is not None:
        if gdp > 3.0:
            regime_scores["bull"] += 2
            regime_scores["risk_on"] += 1
            characteristics.append("Strong economic growth")
        elif gdp > 2.0:
            regime_scores["bull"] += 1
        elif gdp < 1.0:
            regime_scores["bear"] += 1
            regime_scores["risk_off"] += 1
            characteristics.append("Weak growth")
        elif gdp < 0:
            regime_scores["bear"] += 2
            regime_scores["risk_off"] += 2
            characteristics.append("Economic contraction")

    # Fed policy analysis
    if fed_rate is not None:
        if fed_rate < 2.0:
            regime_scores["bull"] += 1
            regime_scores["risk_on"] += 1
            characteristics.append("Accommodative monetary policy")
        elif fed_rate > 5.0:
            regime_scores["bear"] += 1
            regime_scores["risk_off"] += 1
            characteristics.append("Restrictive monetary policy")

    # Determine regime
    max_score = max(regime_scores.values())

    if max_score == 0:
        regime = "transitional"
        confidence = 0.4
    else:
        regime = max(regime_scores.items(), key=lambda x: x[1])[0]
        confidence = max_score / 6  # Max possible score is 6

        # Convert regime names
        regime_map = {
            "bull": "BULL_MARKET",
            "bear": "BEAR_MARKET",
            "risk_on": "RISK_ON",
            "risk_off": "RISK_OFF",
        }
        regime = regime_map.get(regime, "TRANSITIONAL")

    # Add regime-specific characteristics
    if regime == "BULL_MARKET":
        characteristics.insert(0, "Favorable conditions for equities")
    elif regime == "BEAR_MARKET":
        characteristics.insert(0, "Challenging conditions for equities")
    elif regime == "RISK_ON":
        characteristics.insert(0, "Growth and cyclical stocks favored")
    elif regime == "RISK_OFF":
        characteristics.insert(0, "Defensive stocks favored")

    # Recommendations based on regime
    recommendations = get_regime_recommendations(regime)

    return {
        "regime": regime,
        "confidence": round(confidence, 2),
        "characteristics": characteristics,
        "regime_scores": regime_scores,
        "recommendations": recommendations,
    }


def get_regime_recommendations(regime: str) -> List[str]:
    """Get investment recommendations for each regime"""

    recommendations = {
        "BULL_MARKET": [
            "Favor growth and cyclical stocks",
            "Higher risk tolerance acceptable",
            "Consider momentum strategies",
        ],
        "BEAR_MARKET": [
            "Increase defensive positions",
            "Focus on quality and value",
            "Preserve capital, lower risk",
        ],
        "RISK_ON": [
            "Favor small-caps and emerging markets",
            "Technology and consumer discretionary",
            "Higher beta acceptable",
        ],
        "RISK_OFF": [
            "Favor large-caps and developed markets",
            "Utilities, healthcare, staples",
            "Lower beta preferred",
        ],
        "TRANSITIONAL": [
            "Balanced approach",
            "Watch for regime change signals",
            "Moderate risk positioning",
        ],
    }

    return recommendations.get(regime, ["Monitor conditions closely"])


# ============================================================================
# STAGE 3: SECTOR IMPACT ANALYSIS
# ============================================================================


def analyze_sector_impact(
    sector: str, econ_result: Dict, regime_result: Dict
) -> Dict[str, Any]:
    """
    Analyze how macroeconomic conditions affect specific sector

    Sector rotation theory:
    - Early cycle: Financials, Industrials, Materials
    - Mid cycle: Technology, Consumer Discretionary
    - Late cycle: Energy, Staples
    - Recession: Healthcare, Utilities, Consumer Staples

    References:
    - Fama & French (1997) - Industry costs of equity
    - MSCI Sector rotation research
    - Stangl, Jacobsen & Visaltanachoti (2009)
    """

    # Define sector characteristics
    SECTOR_CHARACTERISTICS = {
        "Technology": {
            "type": "growth",
            "cyclicality": "moderate",
            "best_regime": ["BULL_MARKET", "RISK_ON"],
            "worst_regime": ["BEAR_MARKET", "RISK_OFF"],
            "rate_sensitivity": "high",  # Growth stocks hurt by high rates
            "growth_sensitivity": "high",
        },
        "Consumer Discretionary": {
            "type": "cyclical",
            "cyclicality": "high",
            "best_regime": ["BULL_MARKET", "RISK_ON"],
            "worst_regime": ["BEAR_MARKET", "RISK_OFF"],
            "rate_sensitivity": "high",
            "growth_sensitivity": "high",
        },
        "Consumer Staples": {
            "type": "defensive",
            "cyclicality": "low",
            "best_regime": ["BEAR_MARKET", "RISK_OFF"],
            "worst_regime": ["BULL_MARKET"],
            "rate_sensitivity": "low",
            "growth_sensitivity": "low",
        },
        "Healthcare": {
            "type": "defensive",
            "cyclicality": "low",
            "best_regime": ["BEAR_MARKET", "RISK_OFF"],
            "worst_regime": [],
            "rate_sensitivity": "low",
            "growth_sensitivity": "low",
        },
        "Financials": {
            "type": "cyclical",
            "cyclicality": "high",
            "best_regime": ["BULL_MARKET"],
            "worst_regime": ["BEAR_MARKET"],
            "rate_sensitivity": "medium",  # Complex: higher rates can help margins
            "growth_sensitivity": "high",
        },
        "Energy": {
            "type": "cyclical",
            "cyclicality": "high",
            "best_regime": ["RISK_ON"],
            "worst_regime": ["BEAR_MARKET"],
            "rate_sensitivity": "low",
            "growth_sensitivity": "high",
        },
        "Utilities": {
            "type": "defensive",
            "cyclicality": "low",
            "best_regime": ["RISK_OFF"],
            "worst_regime": ["BULL_MARKET"],
            "rate_sensitivity": "very_high",  # Hurt badly by high rates
            "growth_sensitivity": "low",
        },
        "Industrials": {
            "type": "cyclical",
            "cyclicality": "high",
            "best_regime": ["BULL_MARKET", "RISK_ON"],
            "worst_regime": ["BEAR_MARKET"],
            "rate_sensitivity": "medium",
            "growth_sensitivity": "very_high",
        },
        "Materials": {
            "type": "cyclical",
            "cyclicality": "high",
            "best_regime": ["BULL_MARKET"],
            "worst_regime": ["BEAR_MARKET"],
            "rate_sensitivity": "medium",
            "growth_sensitivity": "very_high",
        },
        "Real Estate": {
            "type": "rate_sensitive",
            "cyclicality": "moderate",
            "best_regime": ["BULL_MARKET"],
            "worst_regime": ["RISK_OFF"],
            "rate_sensitivity": "very_high",
            "growth_sensitivity": "moderate",
        },
    }

    # Get sector characteristics
    sector_info = SECTOR_CHARACTERISTICS.get(
        sector,
        {
            "type": "unknown",
            "cyclicality": "moderate",
            "best_regime": [],
            "worst_regime": [],
            "rate_sensitivity": "medium",
            "growth_sensitivity": "medium",
        },
    )

    # Analyze regime fit
    current_regime = regime_result["regime"]

    favorability_score = 0
    reasoning_parts = []

    # Check if current regime favors this sector
    if current_regime in sector_info["best_regime"]:
        favorability_score += 2
        reasoning_parts.append(
            f"{current_regime.replace('_', ' ').title()} regime favors {sector}"
        )
    elif current_regime in sector_info["worst_regime"]:
        favorability_score -= 2
        reasoning_parts.append(
            f"{current_regime.replace('_', ' ').title()} regime challenges {sector}"
        )
    else:
        favorability_score += 0
        reasoning_parts.append(f"Neutral regime for {sector}")

    # Check rate sensitivity
    fed_score = econ_result["detailed_scores"].get("fed_policy", 1.0)

    if sector_info["rate_sensitivity"] == "very_high":
        if fed_score >= 1.5:  # Low rates
            favorability_score += 1
            reasoning_parts.append("Low rates benefit rate-sensitive sector")
        elif fed_score <= 0.5:  # High rates
            favorability_score -= 1
            reasoning_parts.append("High rates hurt rate-sensitive sector")

    # Check growth sensitivity
    gdp_score = econ_result["detailed_scores"].get("gdp", 1.0)

    if sector_info["growth_sensitivity"] in ["high", "very_high"]:
        if gdp_score >= 1.5:  # Strong growth
            favorability_score += 1
            reasoning_parts.append("Strong GDP growth benefits cyclical sector")
        elif gdp_score <= 0.5:  # Weak growth
            favorability_score -= 1
            reasoning_parts.append("Weak growth hurts cyclical sector")

    # Determine outlook
    if favorability_score >= 2:
        outlook = "favorable"
        favorability = "POSITIVE"
    elif favorability_score <= -2:
        outlook = "unfavorable"
        favorability = "NEGATIVE"
    else:
        outlook = "mixed"
        favorability = "NEUTRAL"

    reasoning = "; ".join(reasoning_parts)

    return {
        "sector": sector,
        "outlook": outlook,
        "favorability": favorability,
        "favorability_score": favorability_score,
        "reasoning": reasoning,
        "sector_type": sector_info["type"],
        "recommendations": get_sector_recommendations(sector, outlook, current_regime),
    }


def get_sector_recommendations(sector: str, outlook: str, regime: str) -> List[str]:
    """Get specific recommendations for sector given macro conditions"""

    recs = []

    if outlook == "favorable":
        recs.append(f"{sector} positioned well for current macro environment")
        recs.append("Consider overweighting this sector")
    elif outlook == "unfavorable":
        recs.append(f"{sector} faces macro headwinds")
        recs.append("Consider underweighting or avoiding")
    else:
        recs.append(f"{sector} shows mixed macro signals")
        recs.append("Neutral weight appropriate")

    return recs


# ============================================================================
# STAGE 4: LLM SYNTHESIS
# ============================================================================


def synthesize_macro_outlook_with_llm(
    ticker: str,
    sector: str,
    econ_result: Dict,
    regime_result: Dict,
    sector_result: Dict,
    context,
) -> Dict[str, Any]:
    """
    Use LLM to synthesize macro outlook

    LLM adds value by:
    - Connecting economic indicators to investment implications
    - Identifying non-obvious macro themes
    - Providing forward-looking perspective
    - Contextualizing current conditions historically
    """

    try:
        llm = get_llm_provider("ollama")

        if not llm or not llm.is_available():
            return {
                "success": False,
                "error": "LLM not available",
                "signal": "neutral",
                "confidence": 0.5,
                "reasoning": "LLM synthesis unavailable - using quantitative analysis only",
            }

        # Build comprehensive macro prompt
        prompt = f"""You are a macroeconomic strategist analyzing investment implications.

ECONOMIC INDICATORS:
Overall Economic Score: {econ_result['score']:.1f}/10
Economic Stance: {econ_result['stance']}

Bullish Factors:
{chr(10).join('- ' + f for f in econ_result['bullish_factors'])}

Bearish Factors:
{chr(10).join('- ' + f for f in econ_result['bearish_factors'])}

MARKET REGIME:
Current Regime: {regime_result['regime']}
Confidence: {regime_result['confidence']:.0%}
Characteristics: {', '.join(regime_result['characteristics'])}

SECTOR ANALYSIS:
Company: {ticker}
Sector: {sector}
Sector Outlook: {sector_result['favorability']}
Reasoning: {sector_result['reasoning']}

TASK:
Based on the current macroeconomic environment and market regime, assess the investment outlook for {ticker} ({sector} sector).

Consider:
1. How will current Fed policy affect this company/sector?
2. Is the economic growth trajectory supportive?
3. Are there macro headwinds or tailwinds?
4. How does the market regime align with this sector's characteristics?

Provide:
SIGNAL: [BULLISH/BEARISH/NEUTRAL] for {ticker} given macro conditions
CONFIDENCE: [0.0-1.0]
REASONING: [2-3 sentences explaining macro impact on this investment]

Format:
SIGNAL: [BULLISH/BEARISH/NEUTRAL]
CONFIDENCE: [0.0-1.0]
REASONING: [Your analysis]"""

        # Get LLM response
        response = llm.generate(
            prompt=prompt,
            system_prompt="You are a macro strategist who connects economic trends to investment opportunities. Be specific about cause-and-effect relationships.",
            temperature=0.4,  # Slightly higher for macro (more judgment involved)
            max_tokens=600,
        )

        # Parse response
        parsed = PromptTemplates.parse_llm_response(response.content)

        return {
            "success": True,
            "signal": parsed["signal"],
            "confidence": parsed["confidence"],
            "reasoning": parsed["reasoning"],
            "raw_response": response.content,
        }

    except Exception as e:
        logger.error(f"LLM macro synthesis failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "signal": "neutral",
            "confidence": 0.5,
            "reasoning": f"Macro synthesis failed: {str(e)}",
        }


# ============================================================================
# STAGE 5: FINAL RECOMMENDATION
# ============================================================================


def calculate_macro_recommendation(
    ticker: str,
    sector: str,
    econ_result: Dict,
    regime_result: Dict,
    sector_result: Dict,
    synthesis: Dict,
) -> Tuple[str, float, str]:
    """
    Calculate final macro-based recommendation

    Weighting:
    - Economic indicators: 35%
    - Market regime: 20%
    - Sector impact: 25%
    - AI synthesis: 20%
    """

    # Map to scores
    signal_to_score = {
        "bullish": 1.0,
        "favorable": 1.0,
        "expansionary": 1.0,
        "BULL_MARKET": 1.0,
        "RISK_ON": 0.75,
        "neutral": 0.5,
        "mixed": 0.5,
        "TRANSITIONAL": 0.5,
        "bearish": 0.0,
        "unfavorable": 0.0,
        "contractionary": 0.0,
        "BEAR_MARKET": 0.0,
        "RISK_OFF": 0.25,
    }

    # Get component scores
    econ_score = econ_result["score"] / 10  # Normalize to 0-1
    regime_score = signal_to_score.get(regime_result["regime"], 0.5)
    sector_score = signal_to_score.get(sector_result["favorability"], 0.5)
    ai_score = (
        signal_to_score.get(synthesis["signal"], 0.5) if synthesis["success"] else 0.5
    )

    # Calculate weighted average
    if synthesis["success"]:
        weights = {"econ": 0.35, "regime": 0.20, "sector": 0.25, "ai": 0.20}
        final_score = (
            econ_score * weights["econ"]
            + regime_score * weights["regime"]
            + sector_score * weights["sector"]
            + ai_score * weights["ai"]
        )
        confidence_base = synthesis["confidence"]
    else:
        # Fallback without AI
        weights = {"econ": 0.45, "regime": 0.25, "sector": 0.30}
        final_score = (
            econ_score * weights["econ"]
            + regime_score * weights["regime"]
            + sector_score * weights["sector"]
        )
        confidence_base = 0.6

    # Determine signal
    if final_score >= 0.65:
        final_signal = "bullish"
    elif final_score <= 0.35:
        final_signal = "bearish"
    else:
        final_signal = "neutral"

    # Calculate confidence based on agreement
    components = [
        econ_result["stance"],
        regime_result["regime"],
        sector_result["favorability"],
    ]
    if synthesis["success"]:
        components.append(synthesis["signal"])

    # Count how many components align with final signal
    alignment_count = 0
    for comp in components:
        comp_score = signal_to_score.get(comp, 0.5)
        if final_signal == "bullish" and comp_score >= 0.6:
            alignment_count += 1
        elif final_signal == "bearish" and comp_score <= 0.4:
            alignment_count += 1
        elif final_signal == "neutral" and 0.4 < comp_score < 0.6:
            alignment_count += 1

    agreement = alignment_count / len(components)
    final_confidence = confidence_base * agreement

    # Build reasoning
    reasoning_parts = []

    # Economic backdrop
    reasoning_parts.append(
        f"Economic: {econ_result['stance']} " f"(score: {econ_result['score']:.1f}/10)"
    )

    # Key macro factors
    if econ_result["bullish_factors"]:
        reasoning_parts.append(f"Supports: {econ_result['bullish_factors'][0]}")
    if econ_result["bearish_factors"]:
        reasoning_parts.append(f"Concerns: {econ_result['bearish_factors'][0]}")

    # Regime context
    reasoning_parts.append(
        f"Regime: {regime_result['regime'].replace('_', ' ').title()}"
    )

    # Sector implications
    reasoning_parts.append(
        f"Sector impact: {sector_result['favorability']} for {sector}"
    )

    # AI insights
    if synthesis["success"]:
        reasoning_parts.append(f"Macro view: {synthesis['reasoning'][:80]}...")

    final_reasoning = " | ".join(reasoning_parts)

    return final_signal, round(final_confidence, 2), final_reasoning


# ============================================================================
# HELPER: DETAILED REPORT GENERATOR
# ============================================================================


def generate_macro_report(ticker: str, context) -> str:
    """Generate detailed macro analysis report"""

    fundamentals = context.get_fundamentals()
    sector = fundamentals.get("sector", "Unknown") if fundamentals else "Unknown"

    econ_result = analyze_economic_indicators(context)
    regime_result = detect_market_regime(context)
    sector_result = analyze_sector_impact(sector, econ_result, regime_result)
    synthesis = synthesize_macro_outlook_with_llm(
        ticker, sector, econ_result, regime_result, sector_result, context
    )

    final_signal, final_confidence, final_reasoning = calculate_macro_recommendation(
        ticker, sector, econ_result, regime_result, sector_result, synthesis
    )

    report = f"""
{'='*80}
MACROECONOMIC ANALYSIS REPORT: {ticker} ({sector})
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}

EXECUTIVE SUMMARY
-----------------
Macro Signal: {final_signal.upper()}
Confidence: {final_confidence:.0%}

{final_reasoning}

ECONOMIC INDICATORS ANALYSIS
-----------------------------
Overall Economic Score: {econ_result['score']:.1f}/10
Economic Stance: {econ_result['stance'].upper()}

Detailed Breakdown:
  • Fed Policy Score: {econ_result['detailed_scores'].get('fed_policy', 0):.1f}/2.0
  • Inflation Score: {econ_result['detailed_scores'].get('inflation', 0):.1f}/2.0
  • GDP Score: {econ_result['detailed_scores'].get('gdp', 0):.1f}/2.0
  • Employment Score: {econ_result['detailed_scores'].get('employment', 0):.1f}/2.0
  • Treasury Score: {econ_result['detailed_scores'].get('treasury', 0):.1f}/2.0
  • VIX Score: {econ_result['detailed_scores'].get('vix', 0):.1f}/2.0

Bullish Macro Factors:
{chr(10).join('  ✓ ' + f for f in econ_result['bullish_factors']) if econ_result['bullish_factors'] else '  (None)'}

Bearish Macro Factors:
{chr(10).join('  ✗ ' + f for f in econ_result['bearish_factors']) if econ_result['bearish_factors'] else '  (None)'}

MARKET REGIME ASSESSMENT
-------------------------
Current Regime: {regime_result['regime']}
Regime Confidence: {regime_result['confidence']:.0%}

Characteristics:
{chr(10).join('  • ' + c for c in regime_result['characteristics'])}

Regime-Specific Recommendations:
{chr(10).join('  → ' + r for r in regime_result['recommendations'])}

SECTOR-SPECIFIC IMPACT
-----------------------
Sector: {sector_result['sector']}
Sector Type: {sector_result['sector_type'].replace('_', ' ').title()}
Macro Favorability: {sector_result['favorability']}

Sector Analysis:
  {sector_result['reasoning']}

Recommendations:
{chr(10).join('  → ' + r for r in sector_result['recommendations'])}

AI MACRO SYNTHESIS
------------------
{synthesis.get('reasoning', 'Not available') if synthesis['success'] else 'LLM synthesis not available'}

MACRO INVESTMENT IMPLICATIONS
------------------------------
For {ticker} specifically:

1. Economic Backdrop: {econ_result['stance'].title()}
   → {econ_result['key_factors'][0] if econ_result['key_factors'] else 'No specific factors'}

2. Market Environment: {regime_result['regime'].replace('_', ' ').title()}
   → {regime_result['characteristics'][0] if regime_result['characteristics'] else 'No characteristics'}

3. Sector Positioning: {sector_result['favorability'].title()}
   → {sector_result['reasoning'][:100]}...

{'='*80}
FINAL MACRO ASSESSMENT: {final_signal.upper()} ({final_confidence:.0%} confidence)
{'='*80}
"""

    return report


# ============================================================================
# REGISTRATION
# ============================================================================


def register_advanced_macro_analyst():
    """Register the advanced macro analyst"""
    registry = get_registry()
    registry.register(
        advanced_macro_analyst.agent,
        weight=1.3,  # Macro is important but not as detailed as fundamentals
        tags=["macro", "economic", "llm", "advanced"],
        enabled=True,
    )
    print("✅ Registered: Advanced Macro Analyst")


# ============================================================================
# STANDALONE TESTING
# ============================================================================

if __name__ == "__main__":
    """Test the advanced macro analyst"""
    from agent_builder.core.config import Config
    from agent_builder.core.database import DatabasePool, Database
    from agent_builder.agents.context import AgentContext

    print("\n" + "=" * 80)
    print("TESTING ADVANCED MACRO ANALYST")
    print("=" * 80 + "\n")

    # Setup
    config = Config.from_env()
    pool = DatabasePool(config.database)
    db = Database(pool)

    # Test different sectors to see macro impact
    test_cases = [
        ("AAPL", "Technology"),
        ("MSFT", "Technology"),
        ("TSLA", "Automotive"),
    ]

    for ticker, expected_sector in test_cases:
        print(f"\n{'#'*80}")
        print(f"# Testing: {ticker} ({expected_sector})")
        print(f"{'#'*80}\n")

        context = AgentContext(ticker, db)

        try:
            # Run analysis
            signal, confidence, reasoning = advanced_macro_analyst(ticker, context)

            # Print summary
            print(f"\n{'='*80}")
            print(f"MACRO SUMMARY FOR {ticker}")
            print(f"{'='*80}")
            print(f"Signal: {signal.upper()}")
            print(f"Confidence: {confidence:.0%}")
            print(f"Reasoning: {reasoning}")
            print(f"{'='*80}\n")

            # Generate detailed report
            print("\nGenerating detailed macro report...")
            report = generate_macro_report(ticker, context)
            print(report)

        except Exception as e:
            print(f"❌ Error analyzing {ticker}: {e}")
            import traceback

            traceback.print_exc()

        print("\n" + "=" * 80 + "\n")

    pool.close()

    print("\n✅ Macro analyst testing complete!\n")
