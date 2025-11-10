"""Financial calculator tool with valuation models.

Provides financial calculations and valuation models.
"""

import logging
import yfinance as yf
import math
from typing import Optional, Dict, Any
from simpleeval import simple_eval

logger = logging.getLogger(__name__)


def calculator(
    expression: Optional[str] = None,
    ticker: Optional[str] = None,
    model: Optional[str] = None,
    **kwargs
) -> str:
    """Enhanced financial calculator with valuation models.
    
    Args:
        expression: Mathematical expression to evaluate
        ticker: Stock ticker (required for valuation models)
        model: Valuation model to use (dcf, pe, graham, altman)
        **kwargs: Additional parameters for valuation models
        
    Returns:
        Calculation result as string
    """
    try:
        # If expression provided, evaluate it
        if expression:
            return _evaluate_expression(expression)
        
        # If no ticker, can't do valuation
        if not ticker:
            return _help_message()
        
        # Run valuation model
        if model == 'dcf':
            return dcf_valuation(ticker, **kwargs)
        elif model == 'pe':
            return pe_valuation(ticker, **kwargs)
        elif model == 'graham':
            return graham_number(ticker)
        elif model == 'altman':
            return altman_z_score(ticker)
        else:
            return _help_message()
            
    except Exception as e:
        error_msg = f"Calculator error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg


def _evaluate_expression(expression: str) -> str:
    """Evaluate mathematical expression safely.
    
    Args:
        expression: Math expression to evaluate
        
    Returns:
        Calculation result
    """
    try:
        # Safe functions
        functions = {
            'sqrt': math.sqrt,
            'abs': abs,
            'log': math.log,
            'log10': math.log10,
            'exp': math.exp,
            'pow': pow,
            'max': max,
            'min': min,
            'round': round,
        }
        
        result = simple_eval(expression, functions=functions)
        return f"Calculation: {expression} = {result}"
    except Exception as e:
        return f"Expression evaluation error: {str(e)}"


def dcf_valuation(
    ticker: str,
    growth_rate: float = 0.10,
    discount_rate: float = 0.10,
    terminal_growth: float = 0.03,
    years: int = 5
) -> str:
    """Discounted Cash Flow valuation model.
    
    Args:
        ticker: Stock ticker
        growth_rate: Expected FCF growth rate (default 10%)
        discount_rate: Discount rate / WACC (default 10%)
        terminal_growth: Terminal growth rate (default 3%)
        years: Projection period (default 5 years)
        
    Returns:
        DCF valuation results
    """
    try:
        logger.info(f"Running DCF valuation for {ticker}")
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Get current free cash flow
        fcf = info.get('freeCashflow', 0)
        if not fcf or fcf <= 0:
            return f"DCF Error: No positive free cash flow data available for {ticker}"
        
        # Get shares outstanding and current price
        shares = info.get('sharesOutstanding', 0)
        current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        
        if not shares or not current_price:
            return f"DCF Error: Missing shares or price data for {ticker}"
        
        output = []
        output.append(f"=== DCF VALUATION FOR {ticker.upper()} ===")
        output.append("")
        output.append("Input Parameters:")
        output.append(f"  Current FCF: ${fcf / 1e9:.2f}B")
        output.append(f"  Growth Rate: {growth_rate * 100:.1f}%")
        output.append(f"  Discount Rate: {discount_rate * 100:.1f}%")
        output.append(f"  Terminal Growth: {terminal_growth * 100:.1f}%")
        output.append(f"  Projection Period: {years} years")
        output.append("")
        
        # Project cash flows
        output.append("Projected Cash Flows:")
        projected_fcf = fcf
        pv_sum = 0
        
        for year in range(1, years + 1):
            projected_fcf *= (1 + growth_rate)
            discount_factor = (1 + discount_rate) ** year
            pv = projected_fcf / discount_factor
            pv_sum += pv
            output.append(f"  Year {year}: ${projected_fcf / 1e9:.2f}B (PV: ${pv / 1e9:.2f}B)")
        
        output.append("")
        
        # Terminal value
        terminal_fcf = projected_fcf * (1 + terminal_growth)
        terminal_value = terminal_fcf / (discount_rate - terminal_growth)
        terminal_pv = terminal_value / ((1 + discount_rate) ** years)
        
        output.append("Terminal Value:")
        output.append(f"  Terminal FCF: ${terminal_fcf / 1e9:.2f}B")
        output.append(f"  Terminal Value: ${terminal_value / 1e9:.2f}B")
        output.append(f"  Present Value: ${terminal_pv / 1e9:.2f}B")
        output.append("")
        
        # Enterprise value
        enterprise_value = pv_sum + terminal_pv
        
        # Adjust for cash and debt
        cash = info.get('totalCash', 0)
        debt = info.get('totalDebt', 0)
        
        equity_value = enterprise_value + cash - debt
        value_per_share = equity_value / shares
        
        output.append("Valuation Results:")
        output.append(f"  Enterprise Value: ${enterprise_value / 1e9:.2f}B")
        output.append(f"  Cash: ${cash / 1e9:.2f}B")
        output.append(f"  Debt: ${debt / 1e9:.2f}B")
        output.append(f"  Equity Value: ${equity_value / 1e9:.2f}B")
        output.append(f"  Shares Outstanding: {shares / 1e9:.2f}B")
        output.append("")
        output.append(f"  Fair Value per Share: ${value_per_share:.2f}")
        output.append(f"  Current Price: ${current_price:.2f}")
        
        # Upside/downside
        upside = ((value_per_share - current_price) / current_price * 100)
        if upside > 0:
            output.append(f"  Upside: +{upside:.1f}% (UNDERVALUED)")
        else:
            output.append(f"  Downside: {upside:.1f}% (OVERVALUED)")
        
        return "\n".join(output)
        
    except Exception as e:
        error_msg = f"DCF calculation error for {ticker}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg


def pe_valuation(ticker: str, target_pe: Optional[float] = None) -> str:
    """P/E based valuation.
    
    Args:
        ticker: Stock ticker
        target_pe: Target P/E ratio (uses industry average if not provided)
        
    Returns:
        P/E valuation results
    """
    try:
        logger.info(f"Running P/E valuation for {ticker}")
        stock = yf.Ticker(ticker)
        info = stock.info
        
        eps = info.get('trailingEps', 0)
        current_pe = info.get('trailingPE', 0)
        current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        forward_pe = info.get('forwardPE', 0)
        
        if not eps or not current_price:
            return f"P/E Valuation Error: Missing EPS or price data for {ticker}"
        
        output = []
        output.append(f"=== P/E VALUATION FOR {ticker.upper()} ===")
        output.append("")
        output.append("Current Metrics:")
        output.append(f"  EPS (Trailing): ${eps:.2f}")
        output.append(f"  Current Price: ${current_price:.2f}")
        output.append(f"  Current P/E: {current_pe:.2f}")
        if forward_pe:
            output.append(f"  Forward P/E: {forward_pe:.2f}")
        output.append("")
        
        # Use provided target PE or calculate from current
        if not target_pe:
            # Use industry average or current P/E
            target_pe = current_pe if current_pe > 0 else 15.0
        
        fair_value = eps * target_pe
        
        output.append("Valuation:")
        output.append(f"  Target P/E: {target_pe:.2f}")
        output.append(f"  Fair Value: ${fair_value:.2f}")
        output.append(f"  Current Price: ${current_price:.2f}")
        
        upside = ((fair_value - current_price) / current_price * 100)
        if upside > 0:
            output.append(f"  Upside: +{upside:.1f}% (UNDERVALUED)")
        else:
            output.append(f"  Downside: {upside:.1f}% (OVERVALUED)")
        
        return "\n".join(output)
        
    except Exception as e:
        error_msg = f"P/E calculation error for {ticker}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg


def graham_number(ticker: str) -> str:
    """Calculate Benjamin Graham's intrinsic value formula.
    
    Formula: √(22.5 × EPS × Book Value per Share)
    
    Args:
        ticker: Stock ticker
        
    Returns:
        Graham Number calculation
    """
    try:
        logger.info(f"Calculating Graham Number for {ticker}")
        stock = yf.Ticker(ticker)
        info = stock.info
        
        eps = info.get('trailingEps', 0)
        book_value = info.get('bookValue', 0)
        current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        
        if not eps or eps <= 0:
            return f"Graham Number Error: No positive EPS data for {ticker}"
        if not book_value or book_value <= 0:
            return f"Graham Number Error: No positive book value data for {ticker}"
        
        # Calculate Graham Number
        graham_value = math.sqrt(22.5 * eps * book_value)
        
        output = []
        output.append(f"=== GRAHAM NUMBER FOR {ticker.upper()} ===")
        output.append("")
        output.append("Input Metrics:")
        output.append(f"  EPS: ${eps:.2f}")
        output.append(f"  Book Value per Share: ${book_value:.2f}")
        output.append("")
        output.append("Calculation:")
        output.append(f"  Graham Number = √(22.5 × {eps:.2f} × {book_value:.2f})")
        output.append(f"  Graham Number = ${graham_value:.2f}")
        output.append("")
        output.append(f"  Current Price: ${current_price:.2f}")
        
        # Interpretation
        ratio = current_price / graham_value if graham_value > 0 else 0
        output.append(f"  Price/Graham Ratio: {ratio:.2f}")
        output.append("")
        
        if ratio < 1.0:
            margin = ((graham_value - current_price) / graham_value * 100)
            output.append(f"  UNDERVALUED by {margin:.1f}%")
            output.append("  Graham would consider this a potential buy.")
        elif ratio < 1.5:
            output.append("  FAIRLY VALUED")
            output.append("  Within acceptable range per Graham's criteria.")
        else:
            output.append("  OVERVALUED")
            output.append("  Above Graham's threshold for value investing.")
        
        return "\n".join(output)
        
    except Exception as e:
        error_msg = f"Graham Number calculation error for {ticker}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg


def altman_z_score(ticker: str) -> str:
    """Calculate Altman Z-Score for bankruptcy prediction.
    
    Z = 1.2×WC/TA + 1.4×RE/TA + 3.3×EBIT/TA + 0.6×MVE/TL + 1.0×Sales/TA
    
    Args:
        ticker: Stock ticker
        
    Returns:
        Altman Z-Score calculation
    """
    try:
        logger.info(f"Calculating Altman Z-Score for {ticker}")
        stock = yf.Ticker(ticker)
        info = stock.info
        balance_sheet = stock.balance_sheet
        
        if balance_sheet is None or balance_sheet.empty:
            return f"Altman Z-Score Error: No balance sheet data for {ticker}"
        
        # Get latest balance sheet data
        latest = balance_sheet.iloc[:, 0]
        
        # Extract required metrics
        current_assets = latest.get('Current Assets', 0)
        current_liabilities = latest.get('Current Liabilities', 0)
        total_assets = latest.get('Total Assets', 0)
        retained_earnings = latest.get('Retained Earnings', 0)
        total_liabilities = latest.get('Total Liabilities Net Minority Interest', 0)
        
        ebit = info.get('ebit', 0)
        market_cap = info.get('marketCap', 0)
        total_revenue = info.get('totalRevenue', 0)
        
        # Calculate components
        working_capital = current_assets - current_liabilities
        
        if not total_assets or total_assets == 0:
            return f"Altman Z-Score Error: Invalid total assets for {ticker}"
        
        # Z-Score components
        x1 = (working_capital / total_assets) if total_assets else 0
        x2 = (retained_earnings / total_assets) if total_assets else 0
        x3 = (ebit / total_assets) if total_assets else 0
        x4 = (market_cap / total_liabilities) if total_liabilities else 0
        x5 = (total_revenue / total_assets) if total_assets else 0
        
        # Calculate Z-Score
        z_score = 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 1.0 * x5
        
        output = []
        output.append(f"=== ALTMAN Z-SCORE FOR {ticker.upper()} ===")
        output.append("")
        output.append("Components:")
        output.append(f"  Working Capital / Total Assets: {x1:.4f} (Weight: 1.2)")
        output.append(f"  Retained Earnings / Total Assets: {x2:.4f} (Weight: 1.4)")
        output.append(f"  EBIT / Total Assets: {x3:.4f} (Weight: 3.3)")
        output.append(f"  Market Cap / Total Liabilities: {x4:.4f} (Weight: 0.6)")
        output.append(f"  Sales / Total Assets: {x5:.4f} (Weight: 1.0)")
        output.append("")
        output.append(f"  Z-Score: {z_score:.2f}")
        output.append("")
        
        # Interpretation
        output.append("Interpretation:")
        if z_score > 3.0:
            output.append(f"  Z-Score > 3.0: SAFE ZONE")
            output.append("  Low probability of bankruptcy. Strong financial health.")
        elif z_score > 2.6:
            output.append(f"  Z-Score 2.6-3.0: GREY ZONE (Upper)")
            output.append("  Generally safe, but monitor closely.")
        elif z_score > 1.8:
            output.append(f"  Z-Score 1.8-2.6: GREY ZONE")
            output.append("  Some financial distress possible. Caution advised.")
        else:
            output.append(f"  Z-Score < 1.8: DISTRESS ZONE")
            output.append("  High probability of bankruptcy within 2 years. HIGH RISK.")
        
        return "\n".join(output)
        
    except Exception as e:
        error_msg = f"Altman Z-Score calculation error for {ticker}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg


def _help_message() -> str:
    """Return help message for calculator tool."""
    return """
=== FINANCIAL CALCULATOR HELP ===

Available Functions:

1. Mathematical Expressions:
   calculator(expression="sqrt(100) + 2*5")

2. DCF Valuation:
   calculator(ticker="AAPL", model="dcf", growth_rate=0.10, discount_rate=0.10)

3. P/E Valuation:
   calculator(ticker="AAPL", model="pe", target_pe=20)

4. Graham Number:
   calculator(ticker="AAPL", model="graham")

5. Altman Z-Score:
   calculator(ticker="AAPL", model="altman")

Parameters:
- ticker: Stock ticker symbol (required for valuation models)
- model: dcf, pe, graham, or altman
- growth_rate: Expected FCF growth rate (default 0.10)
- discount_rate: WACC / discount rate (default 0.10)
- terminal_growth: Terminal growth rate (default 0.03)
- target_pe: Target P/E ratio for valuation
"""
