"""
Fundamental Analysis Agents
Focus on company financials, valuation, and business quality
"""

from agent_builder.agents import simple_agent
from agent_builder.repositories.connection import get_db_cursor
import logging

logger = logging.getLogger(__name__)


# =============================================================================
# VALUE INVESTING AGENTS
# =============================================================================


@simple_agent("Value Investor", weight=0.15)
def value_investor_agent(ticker, context):
    """
    Warren Buffett style value investing

    Strategy:
    - Look for undervalued companies
    - Strong fundamentals at fair prices
    - Low P/E, high ROE, low debt
    """
    pe_ratio = context.get_metric("pe_ratio")
    pb_ratio = context.get_metric("pb_ratio")
    roe = context.get_metric("roe")
    debt_to_equity = context.get_metric("debt_to_equity")
    dividend_yield = context.get_metric("dividend_yield")

    # Score the stock
    score = 0

    # Valuation metrics
    if pe_ratio < 15:
        score += 3
    elif pe_ratio < 20:
        score += 2
    elif pe_ratio < 25:
        score += 1

    if pb_ratio < 1.5:
        score += 2
    elif pb_ratio < 3:
        score += 1

    # Quality metrics
    if roe > 20:
        score += 3
    elif roe > 15:
        score += 2
    elif roe > 10:
        score += 1

    # Financial health
    if debt_to_equity < 0.5:
        score += 2
    elif debt_to_equity < 1.0:
        score += 1

    # Dividend bonus
    if dividend_yield > 2.5:
        score += 1

    # Decision
    if score >= 8:
        return "bullish", 0.9
    elif score >= 6:
        return "bullish", 0.75
    elif score >= 4:
        return "neutral", 0.6
    elif score >= 2:
        return "bearish", 0.65
    else:
        return "bearish", 0.8


@simple_agent("Deep Value Screener", weight=0.12)
def deep_value_agent(ticker, context):
    """
    Deep value investing - extreme undervaluation

    Strategy:
    - Very low P/E and P/B ratios
    - Trading below book value
    - Margin of safety approach
    """
    pe_ratio = context.get_metric("pe_ratio")
    pb_ratio = context.get_metric("pb_ratio")
    ps_ratio = context.get_metric("ps_ratio")
    current_ratio = context.get_metric("current_ratio")

    # Deep value criteria
    deep_value_signals = 0

    if pe_ratio < 10:
        deep_value_signals += 1

    if pb_ratio < 1.0:  # Trading below book value
        deep_value_signals += 1

    if ps_ratio < 1.0:  # Trading below sales
        deep_value_signals += 1

    if current_ratio > 1.5:  # Good liquidity
        deep_value_signals += 1

    # Deep value opportunity
    if deep_value_signals >= 3:
        return "bullish", 0.85
    elif deep_value_signals >= 2:
        return "bullish", 0.7
    elif deep_value_signals >= 1:
        return "neutral", 0.5
    else:
        return "bearish", 0.6


# =============================================================================
# GROWTH INVESTING AGENTS
# =============================================================================


@simple_agent("Growth Investor", weight=0.15)
def growth_investor_agent(ticker, context):
    """
    Growth at reasonable price (GARP)

    Strategy:
    - High revenue and earnings growth
    - PEG ratio < 2
    - Strong profit margins
    """
    revenue_growth = context.get_metric("revenue_growth")
    earnings_growth = context.get_metric("earnings_growth")
    peg_ratio = context.get_metric("peg_ratio")
    profit_margin = context.get_metric("profit_margin")
    roe = context.get_metric("roe")

    # Growth score
    score = 0

    # Revenue growth
    if revenue_growth > 20:
        score += 3
    elif revenue_growth > 15:
        score += 2
    elif revenue_growth > 10:
        score += 1

    # Earnings growth
    if earnings_growth > 20:
        score += 3
    elif earnings_growth > 15:
        score += 2
    elif earnings_growth > 10:
        score += 1

    # Reasonable valuation (PEG)
    if peg_ratio < 1.0:
        score += 3
    elif peg_ratio < 1.5:
        score += 2
    elif peg_ratio < 2.0:
        score += 1

    # Profitability
    if profit_margin > 20:
        score += 2
    elif profit_margin > 15:
        score += 1

    if roe > 20:
        score += 1

    # Decision
    if score >= 9:
        return "bullish", 0.9
    elif score >= 7:
        return "bullish", 0.8
    elif score >= 5:
        return "bullish", 0.65
    elif score >= 3:
        return "neutral", 0.5
    else:
        return "bearish", 0.7


@simple_agent("High Growth Hunter", weight=0.12)
def high_growth_agent(ticker, context):
    """
    Aggressive growth investing

    Strategy:
    - Very high growth rates (>25%)
    - Accept higher valuations
    - Focus on revenue acceleration
    """
    revenue_growth = context.get_metric("revenue_growth")
    earnings_growth = context.get_metric("earnings_growth")
    operating_margin = context.get_metric("operating_margin")

    # High growth threshold
    if revenue_growth > 30 or earnings_growth > 30:
        # Super high growth
        if operating_margin > 15:
            return "bullish", 0.9
        else:
            return "bullish", 0.75
    elif revenue_growth > 20 or earnings_growth > 20:
        # Strong growth
        if operating_margin > 10:
            return "bullish", 0.8
        else:
            return "bullish", 0.65
    elif revenue_growth > 15 or earnings_growth > 15:
        # Moderate growth
        return "neutral", 0.6
    else:
        # Low growth
        return "bearish", 0.7


# =============================================================================
# QUALITY INVESTING AGENTS
# =============================================================================


@simple_agent("Quality Screener", weight=0.13)
def quality_screener_agent(ticker, context):
    """
    High quality businesses

    Strategy:
    - High ROE, ROIC, profit margins
    - Low debt
    - Consistent performance
    """
    roe = context.get_metric("roe")
    roic = context.get_metric("roic")
    profit_margin = context.get_metric("profit_margin")
    debt_to_equity = context.get_metric("debt_to_equity")
    current_ratio = context.get_metric("current_ratio")
    interest_coverage = context.get_metric("interest_coverage")

    # Quality score
    quality_score = 0

    # Profitability
    if roe > 25:
        quality_score += 3
    elif roe > 20:
        quality_score += 2
    elif roe > 15:
        quality_score += 1

    if roic > 20:
        quality_score += 3
    elif roic > 15:
        quality_score += 2
    elif roic > 10:
        quality_score += 1

    if profit_margin > 25:
        quality_score += 2
    elif profit_margin > 20:
        quality_score += 1

    # Financial strength
    if debt_to_equity < 0.3:
        quality_score += 2
    elif debt_to_equity < 0.5:
        quality_score += 1

    if current_ratio > 2.0:
        quality_score += 1

    if interest_coverage > 10:
        quality_score += 1

    # Decision
    if quality_score >= 10:
        return "bullish", 0.9
    elif quality_score >= 8:
        return "bullish", 0.8
    elif quality_score >= 6:
        return "bullish", 0.7
    elif quality_score >= 4:
        return "neutral", 0.5
    else:
        return "bearish", 0.65


@simple_agent("Moat Analyzer", weight=0.11)
def moat_analyzer_agent(ticker, context):
    """
    Economic moat analysis

    Strategy:
    - High margins indicate pricing power
    - High ROIC indicates competitive advantage
    - Low asset turnover + high margins = intangible moat
    """
    gross_margin = context.get_metric("gross_margin")
    operating_margin = context.get_metric("operating_margin")
    roic = context.get_metric("roic")
    asset_turnover = context.get_metric("asset_turnover")

    moat_score = 0

    # Pricing power (high margins)
    if gross_margin > 50:
        moat_score += 3
    elif gross_margin > 40:
        moat_score += 2
    elif gross_margin > 30:
        moat_score += 1

    if operating_margin > 25:
        moat_score += 2
    elif operating_margin > 20:
        moat_score += 1

    # Competitive advantage (high ROIC)
    if roic > 20:
        moat_score += 3
    elif roic > 15:
        moat_score += 2

    # Intangible assets moat (brand, patents)
    if asset_turnover < 1.0 and operating_margin > 20:
        moat_score += 2  # Low asset intensity + high margins = strong brand/IP

    # Decision
    if moat_score >= 8:
        return "bullish", 0.85
    elif moat_score >= 6:
        return "bullish", 0.75
    elif moat_score >= 4:
        return "neutral", 0.6
    else:
        return "bearish", 0.6


# =============================================================================
# CASH FLOW FOCUSED AGENTS
# =============================================================================


@simple_agent("Cash Flow Quality", weight=0.12)
def cash_flow_quality_agent(ticker, context):
    """
    Analyze cash generation quality

    Strategy:
    - Free cash flow > Net income (quality earnings)
    - Strong operating cash flow
    - Low capex relative to revenue
    """
    # Get latest cash flow data
    cash_flow = context.get_cash_flow()

    if not cash_flow:
        return "neutral", 0.5

    fcf = cash_flow.get("free_cash_flow", 0)
    net_income = cash_flow.get("net_income", 1)
    operating_cf = cash_flow.get("operating_cash_flow", 0)
    capex = cash_flow.get("capex", 0)

    # Avoid division by zero
    if net_income <= 0:
        return "bearish", 0.7

    # FCF to Net Income ratio (quality)
    fcf_conversion = fcf / net_income if net_income > 0 else 0

    # Operating cash flow quality
    ocf_quality = operating_cf / net_income if net_income > 0 else 0

    score = 0

    # High quality cash generation
    if fcf_conversion > 1.2:
        score += 3
    elif fcf_conversion > 1.0:
        score += 2
    elif fcf_conversion > 0.8:
        score += 1

    if ocf_quality > 1.2:
        score += 2
    elif ocf_quality > 1.0:
        score += 1

    # Low capex intensity is good
    revenue = context.get_metric("revenue")
    if revenue > 0:
        capex_intensity = abs(capex) / (revenue / 4)  # Quarterly revenue
        if capex_intensity < 0.05:
            score += 2
        elif capex_intensity < 0.08:
            score += 1

    # Decision
    if score >= 6:
        return "bullish", 0.85
    elif score >= 4:
        return "bullish", 0.7
    elif score >= 2:
        return "neutral", 0.55
    else:
        return "bearish", 0.7


@simple_agent("Capital Allocator", weight=0.10)
def capital_allocation_agent(ticker, context):
    """
    Analyze capital allocation decisions

    Strategy:
    - Share buybacks (reducing share count)
    - Dividends (returning cash)
    - Low debt issuance
    - Smart acquisitions
    """
    cash_flow = context.get_cash_flow()

    if not cash_flow:
        return "neutral", 0.5

    fcf = cash_flow.get("free_cash_flow", 0)
    buybacks = cash_flow.get("stock_buyback", 0)
    dividends = cash_flow.get("dividends_paid", 0)
    debt_issued = cash_flow.get("debt_issued", 0)

    if fcf <= 0:
        return "bearish", 0.75

    # Capital return ratio
    cash_returned = abs(buybacks) + abs(dividends)
    return_ratio = cash_returned / fcf if fcf > 0 else 0

    score = 0

    # Good capital return
    if return_ratio > 0.8:
        score += 3
    elif return_ratio > 0.6:
        score += 2
    elif return_ratio > 0.4:
        score += 1

    # Buybacks are good (shareholder-friendly)
    if buybacks > 0:
        score += 2

    # Low debt issuance
    if debt_issued < fcf * 0.2:
        score += 1

    # Decision
    if score >= 5:
        return "bullish", 0.8
    elif score >= 3:
        return "bullish", 0.65
    elif score >= 1:
        return "neutral", 0.5
    else:
        return "bearish", 0.6


# =============================================================================
# EARNINGS QUALITY AGENTS
# =============================================================================


@simple_agent("Earnings Surprise Tracker", weight=0.11)
def earnings_surprise_agent(ticker, context):
    """
    Track earnings beats and misses

    Strategy:
    - Consistent earnings beats = bullish
    - Large beats = very bullish
    - Misses = bearish
    """
    earnings = context.get_earnings()

    if not earnings:
        return "neutral", 0.5

    eps_surprise = earnings.get("eps_surprise", 0)
    revenue_surprise = earnings.get("revenue_surprise", 0)

    score = 0

    # EPS surprise
    if eps_surprise > 10:
        score += 3
    elif eps_surprise > 5:
        score += 2
    elif eps_surprise > 0:
        score += 1
    elif eps_surprise < -5:
        score -= 2
    elif eps_surprise < 0:
        score -= 1

    # Revenue surprise
    if revenue_surprise > 5:
        score += 2
    elif revenue_surprise > 0:
        score += 1
    elif revenue_surprise < -3:
        score -= 2
    elif revenue_surprise < 0:
        score -= 1

    # Decision
    if score >= 4:
        return "bullish", 0.85
    elif score >= 2:
        return "bullish", 0.7
    elif score >= 0:
        return "neutral", 0.5
    elif score >= -2:
        return "bearish", 0.65
    else:
        return "bearish", 0.8


@simple_agent("Guidance Analyzer", weight=0.09)
def guidance_analyzer_agent(ticker, context):
    """
    Analyze forward guidance

    Strategy:
    - Strong guidance = bullish
    - Guidance above estimates = very bullish
    - Weak guidance = bearish
    """
    earnings = context.get_earnings()
    fundamentals = context.get_fundamentals()

    if not earnings:
        return "neutral", 0.5

    next_eps_guidance = earnings.get("next_quarter_eps_guidance", 0)
    current_eps = fundamentals.get("earnings_per_share", 0)

    if current_eps <= 0:
        return "neutral", 0.5

    # Growth implied by guidance
    guidance_growth = ((next_eps_guidance - current_eps) / current_eps) * 100

    if guidance_growth > 15:
        return "bullish", 0.85
    elif guidance_growth > 10:
        return "bullish", 0.75
    elif guidance_growth > 5:
        return "bullish", 0.65
    elif guidance_growth > 0:
        return "neutral", 0.55
    elif guidance_growth > -5:
        return "bearish", 0.6
    else:
        return "bearish", 0.75


# =============================================================================
# FINANCIAL HEALTH AGENTS
# =============================================================================


@simple_agent("Balance Sheet Strength", weight=0.10)
def balance_sheet_agent(ticker, context):
    """
    Analyze balance sheet health

    Strategy:
    - Strong cash position
    - Low debt levels
    - Good liquidity ratios
    """
    balance_sheet = context.get_balance_sheet()

    if not balance_sheet:
        # Use fundamentals as fallback
        debt_to_equity = context.get_metric("debt_to_equity")
        current_ratio = context.get_metric("current_ratio")
        quick_ratio = context.get_metric("quick_ratio")

        score = 0
        if debt_to_equity < 0.5:
            score += 2
        if current_ratio > 1.5:
            score += 2
        if quick_ratio > 1.0:
            score += 2

        if score >= 5:
            return "bullish", 0.8
        elif score >= 3:
            return "neutral", 0.6
        else:
            return "bearish", 0.65

    total_assets = balance_sheet.get("total_assets", 1)
    cash = balance_sheet.get("cash_and_equivalents", 0)
    total_liabilities = balance_sheet.get("total_liabilities", 0)
    current_assets = balance_sheet.get("current_assets", 0)
    current_liabilities = balance_sheet.get("current_liabilities", 1)
    long_term_debt = balance_sheet.get("long_term_debt", 0)

    # Calculate ratios
    cash_ratio = cash / total_assets if total_assets > 0 else 0
    debt_ratio = total_liabilities / total_assets if total_assets > 0 else 0
    current_ratio = (
        current_assets / current_liabilities if current_liabilities > 0 else 0
    )
    debt_to_equity = (
        total_liabilities / (total_assets - total_liabilities)
        if (total_assets - total_liabilities) > 0
        else 0
    )

    score = 0

    # Strong cash position
    if cash_ratio > 0.2:
        score += 3
    elif cash_ratio > 0.1:
        score += 2
    elif cash_ratio > 0.05:
        score += 1

    # Low debt
    if debt_ratio < 0.3:
        score += 2
    elif debt_ratio < 0.5:
        score += 1

    # Good liquidity
    if current_ratio > 2.0:
        score += 2
    elif current_ratio > 1.5:
        score += 1

    # Low leverage
    if debt_to_equity < 0.5:
        score += 2
    elif debt_to_equity < 1.0:
        score += 1

    # Decision
    if score >= 8:
        return "bullish", 0.85
    elif score >= 6:
        return "bullish", 0.75
    elif score >= 4:
        return "neutral", 0.6
    else:
        return "bearish", 0.7


@simple_agent("Debt Sustainability", weight=0.09)
def debt_sustainability_agent(ticker, context):
    """
    Analyze debt sustainability

    Strategy:
    - Interest coverage ratio > 5
    - Debt paydown from cash flow
    - Low debt relative to earnings
    """
    interest_coverage = context.get_metric("interest_coverage")
    debt_to_equity = context.get_metric("debt_to_equity")

    cash_flow = context.get_cash_flow()
    balance_sheet = context.get_balance_sheet()

    score = 0

    # Interest coverage
    if interest_coverage > 10:
        score += 3
    elif interest_coverage > 5:
        score += 2
    elif interest_coverage > 3:
        score += 1
    elif interest_coverage < 2:
        score -= 2

    # Debt to equity
    if debt_to_equity < 0.5:
        score += 2
    elif debt_to_equity < 1.0:
        score += 1
    elif debt_to_equity > 2.0:
        score -= 2

    # Debt repayment from cash flow
    if cash_flow and balance_sheet:
        debt_repaid = cash_flow.get("debt_repaid", 0)
        debt_issued = cash_flow.get("debt_issued", 0)
        net_debt_reduction = debt_repaid - debt_issued

        if net_debt_reduction > 0:
            score += 2  # Paying down debt

    # Decision
    if score >= 6:
        return "bullish", 0.8
    elif score >= 4:
        return "bullish", 0.7
    elif score >= 2:
        return "neutral", 0.6
    elif score >= 0:
        return "bearish", 0.65
    else:
        return "bearish", 0.8


# =============================================================================
# REGISTRATION
# =============================================================================


def register_fundamental_agents():
    """Register all fundamental agents"""
    from agent_builder.agents.registry import get_registry

    registry = get_registry()

    # Value agents
    registry.register(value_investor_agent.agent, tags=["fundamental", "value"])
    registry.register(deep_value_agent.agent, tags=["fundamental", "value"])

    # Growth agents
    registry.register(growth_investor_agent.agent, tags=["fundamental", "growth"])
    registry.register(high_growth_agent.agent, tags=["fundamental", "growth"])

    # Quality agents
    registry.register(quality_screener_agent.agent, tags=["fundamental", "quality"])
    registry.register(moat_analyzer_agent.agent, tags=["fundamental", "quality"])

    # Cash flow agents
    registry.register(cash_flow_quality_agent.agent, tags=["fundamental", "cashflow"])
    registry.register(capital_allocation_agent.agent, tags=["fundamental", "cashflow"])

    # Earnings agents
    registry.register(earnings_surprise_agent.agent, tags=["fundamental", "earnings"])
    registry.register(guidance_analyzer_agent.agent, tags=["fundamental", "earnings"])

    # Financial health agents
    registry.register(balance_sheet_agent.agent, tags=["fundamental", "health"])
    registry.register(debt_sustainability_agent.agent, tags=["fundamental", "health"])

    logger.info("✅ Registered 12 fundamental agents")


if __name__ == "__main__":
    # Test agents
    from agent_builder.agents.context import AgentContext

    context = AgentContext("AAPL")

    print("Testing fundamental agents on AAPL:")
    print("-" * 60)

    agents = [
        value_investor_agent,
        growth_investor_agent,
        quality_screener_agent,
        cash_flow_quality_agent,
    ]

    for agent_func in agents:
        signal, confidence = agent_func("AAPL", context)
        print(f"{agent_func.__name__:30s} {signal:8s} ({confidence:.2f})")
