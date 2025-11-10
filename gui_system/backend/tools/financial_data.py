"""Financial data tool implementation using yfinance.

Provides comprehensive financial analysis and metrics.
"""

import logging
import yfinance as yf
from typing import Optional
import pandas as pd

logger = logging.getLogger(__name__)


def financial_data(ticker: str, include_statements: bool = True) -> str:
    """Get comprehensive financial data and analysis.
    
    Args:
        ticker: Stock ticker symbol
        include_statements: Include financial statements (income, balance, cash flow)
        
    Returns:
        Formatted financial data as string
    """
    try:
        logger.info(f"Fetching financial data for {ticker}")
        stock = yf.Ticker(ticker)
        info = stock.info
        
        output = []
        output.append(f"=== COMPREHENSIVE FINANCIAL DATA FOR {ticker.upper()} ===")
        output.append("")
        
        # Company Overview
        output.append("--- COMPANY OVERVIEW ---")
        output.append(f"Name: {info.get('longName', 'N/A')}")
        output.append(f"Sector: {info.get('sector', 'N/A')}")
        output.append(f"Industry: {info.get('industry', 'N/A')}")
        output.append(f"Website: {info.get('website', 'N/A')}")
        output.append(f"Employees: {info.get('fullTimeEmployees', 'N/A'):,}" if info.get('fullTimeEmployees') else "Employees: N/A")
        
        # Business Summary
        summary = info.get('longBusinessSummary', '')
        if summary:
            # Limit to 300 characters
            summary_short = summary[:300] + "..." if len(summary) > 300 else summary
            output.append(f"\nBusiness: {summary_short}")
        output.append("")
        
        # Analyst Ratings & Price Targets
        output.append("--- ANALYST DATA ---")
        target_high = info.get('targetHighPrice', 0)
        target_low = info.get('targetLowPrice', 0)
        target_mean = info.get('targetMeanPrice', 0)
        current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        
        if target_mean:
            upside = ((target_mean - current_price) / current_price * 100) if current_price else 0
            output.append(f"Current Price: ${current_price:.2f}")
            output.append(f"Analyst Target: ${target_mean:.2f} (Range: ${target_low:.2f} - ${target_high:.2f})")
            output.append(f"Potential Upside: {upside:+.1f}%")
        
        recommendation = info.get('recommendationKey', '')
        num_analysts = info.get('numberOfAnalystOpinions', 0)
        if recommendation:
            output.append(f"Recommendation: {recommendation.upper()} ({num_analysts} analysts)")
        output.append("")
        
        # Trading Information
        output.append("--- TRADING INFORMATION ---")
        volume = info.get('volume', 0)
        avg_volume = info.get('averageVolume', 0)
        if volume:
            output.append(f"Volume: {volume:,} (Avg: {avg_volume:,})")
        
        week_52_high = info.get('fiftyTwoWeekHigh', 0)
        week_52_low = info.get('fiftyTwoWeekLow', 0)
        if week_52_high and week_52_low:
            output.append(f"52-Week Range: ${week_52_low:.2f} - ${week_52_high:.2f}")
        
        beta = info.get('beta', 0)
        if beta:
            output.append(f"Beta: {beta:.2f}")
        
        market_cap = info.get('marketCap', 0)
        if market_cap:
            market_cap_b = market_cap / 1e9
            output.append(f"Market Cap: ${market_cap_b:.2f}B")
        output.append("")
        
        # Ownership Information
        output.append("--- OWNERSHIP ---")
        inst_holdings = info.get('heldPercentInstitutions', 0)
        insider_holdings = info.get('heldPercentInsiders', 0)
        if inst_holdings:
            output.append(f"Institutional Ownership: {inst_holdings * 100:.1f}%")
        if insider_holdings:
            output.append(f"Insider Ownership: {insider_holdings * 100:.1f}%")
        
        shares_outstanding = info.get('sharesOutstanding', 0)
        shares_short = info.get('sharesShort', 0)
        if shares_outstanding and shares_short:
            short_ratio = (shares_short / shares_outstanding * 100)
            output.append(f"Short Interest: {short_ratio:.2f}%")
        output.append("")
        
        # Dividend Information
        output.append("--- DIVIDENDS ---")
        div_yield = info.get('dividendYield', 0)
        div_rate = info.get('dividendRate', 0)
        payout_ratio = info.get('payoutRatio', 0)
        
        if div_yield:
            output.append(f"Dividend Yield: {div_yield * 100:.2f}%")
            output.append(f"Annual Dividend: ${div_rate:.2f}")
            if payout_ratio:
                output.append(f"Payout Ratio: {payout_ratio * 100:.1f}%")
        else:
            output.append("No dividend information available")
        output.append("")
        
        # Financial Statements (if requested)
        if include_statements:
            output.append("--- FINANCIAL STATEMENTS ---")
            
            # Income Statement
            try:
                income_stmt = stock.financials
                if income_stmt is not None and not income_stmt.empty:
                    output.append("\nIncome Statement (Most Recent):")
                    # Get the most recent column (latest year/quarter)
                    latest = income_stmt.iloc[:, 0]
                    
                    # Key metrics
                    total_revenue = latest.get('Total Revenue', 0)
                    gross_profit = latest.get('Gross Profit', 0)
                    operating_income = latest.get('Operating Income', 0)
                    net_income = latest.get('Net Income', 0)
                    
                    if total_revenue:
                        output.append(f"  Total Revenue: ${total_revenue / 1e9:.2f}B")
                    if gross_profit:
                        output.append(f"  Gross Profit: ${gross_profit / 1e9:.2f}B")
                        if total_revenue:
                            gross_margin = (gross_profit / total_revenue * 100)
                            output.append(f"  Gross Margin: {gross_margin:.1f}%")
                    if operating_income:
                        output.append(f"  Operating Income: ${operating_income / 1e9:.2f}B")
                    if net_income:
                        output.append(f"  Net Income: ${net_income / 1e9:.2f}B")
                        if total_revenue:
                            profit_margin = (net_income / total_revenue * 100)
                            output.append(f"  Profit Margin: {profit_margin:.1f}%")
            except Exception as e:
                logger.warning(f"Error fetching income statement: {e}")
                output.append("\nIncome Statement: Not available")
            
            # Balance Sheet
            try:
                balance_sheet = stock.balance_sheet
                if balance_sheet is not None and not balance_sheet.empty:
                    output.append("\nBalance Sheet (Most Recent):")
                    latest = balance_sheet.iloc[:, 0]
                    
                    total_assets = latest.get('Total Assets', 0)
                    total_liabilities = latest.get('Total Liabilities Net Minority Interest', 0)
                    stockholder_equity = latest.get('Stockholders Equity', 0)
                    cash = latest.get('Cash And Cash Equivalents', 0)
                    total_debt = latest.get('Total Debt', 0)
                    
                    if total_assets:
                        output.append(f"  Total Assets: ${total_assets / 1e9:.2f}B")
                    if total_liabilities:
                        output.append(f"  Total Liabilities: ${total_liabilities / 1e9:.2f}B")
                    if stockholder_equity:
                        output.append(f"  Stockholder Equity: ${stockholder_equity / 1e9:.2f}B")
                    if cash:
                        output.append(f"  Cash & Equivalents: ${cash / 1e9:.2f}B")
                    if total_debt and stockholder_equity:
                        debt_to_equity = (total_debt / stockholder_equity)
                        output.append(f"  Debt/Equity Ratio: {debt_to_equity:.2f}")
            except Exception as e:
                logger.warning(f"Error fetching balance sheet: {e}")
                output.append("\nBalance Sheet: Not available")
            
            # Cash Flow
            try:
                cash_flow = stock.cashflow
                if cash_flow is not None and not cash_flow.empty:
                    output.append("\nCash Flow (Most Recent):")
                    latest = cash_flow.iloc[:, 0]
                    
                    operating_cf = latest.get('Operating Cash Flow', 0)
                    investing_cf = latest.get('Investing Cash Flow', 0)
                    financing_cf = latest.get('Financing Cash Flow', 0)
                    free_cf = latest.get('Free Cash Flow', 0)
                    
                    if operating_cf:
                        output.append(f"  Operating Cash Flow: ${operating_cf / 1e9:.2f}B")
                    if investing_cf:
                        output.append(f"  Investing Cash Flow: ${investing_cf / 1e9:.2f}B")
                    if financing_cf:
                        output.append(f"  Financing Cash Flow: ${financing_cf / 1e9:.2f}B")
                    if free_cf:
                        output.append(f"  Free Cash Flow: ${free_cf / 1e9:.2f}B")
            except Exception as e:
                logger.warning(f"Error fetching cash flow: {e}")
                output.append("\nCash Flow: Not available")
            
            output.append("")
        
        result = "\n".join(output)
        logger.info(f"Successfully retrieved comprehensive financial data for {ticker}")
        return result
        
    except Exception as e:
        error_msg = f"Error fetching financial data for {ticker}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg
