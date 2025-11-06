"""Data formatters for different consumers."""

from typing import Dict, Any


class DataFormatter:
    """Format stock data for various consumers (LLM, UI, etc)."""
    
    @staticmethod
    def for_llm(data: Dict[str, Any]) -> str:
        """Format data for LLM consumption.
        
        Args:
            data: Stock data dictionary
            
        Returns:
            Formatted string for LLM
        """
        sections = [
            DataFormatter._format_company_info(data),
            DataFormatter._format_valuation(data),
            DataFormatter._format_profitability(data),
            DataFormatter._format_growth(data),
            DataFormatter._format_dividends(data),
            DataFormatter._format_financial_health(data)
        ]
        return '\n\n'.join(sections)
    
    @staticmethod
    def _format_company_info(data: Dict[str, Any]) -> str:
        """Format company information."""
        return f"""=== COMPANY INFO ===
Company: {data.get('company_name', 'Unknown')}
Sector: {data.get('sector', 'Unknown')}
Industry: {data.get('industry', 'Unknown')}"""
    
    @staticmethod
    def _format_valuation(data: Dict[str, Any]) -> str:
        """Format valuation metrics."""
        return f"""=== VALUATION ===
Price: ${data.get('price', 0):.2f}
Market Cap: ${data.get('market_cap', 0):,.0f}
P/E Ratio: {data.get('pe_ratio', 0):.2f}
P/B Ratio: {data.get('pb_ratio', 0):.2f}
PEG Ratio: {data.get('peg_ratio', 0):.2f}"""
    
    @staticmethod
    def _format_profitability(data: Dict[str, Any]) -> str:
        """Format profitability metrics."""
        return f"""=== PROFITABILITY ===
Profit Margin: {data.get('profit_margin', 0):.2f}%
ROE: {data.get('roe', 0):.2f}%
ROA: {data.get('roa', 0):.2f}%"""
    
    @staticmethod
    def _format_growth(data: Dict[str, Any]) -> str:
        """Format growth metrics."""
        return f"""=== GROWTH ===
Revenue Growth: {data.get('revenue_growth', 0):.2f}%
Earnings Growth: {data.get('earnings_growth', 0):.2f}%"""
    
    @staticmethod
    def _format_dividends(data: Dict[str, Any]) -> str:
        """Format dividend metrics."""
        return f"""=== DIVIDENDS ===
Dividend Yield: {data.get('dividend_yield', 0):.2f}%
Payout Ratio: {data.get('payout_ratio', 0):.2f}%"""
    
    @staticmethod
    def _format_financial_health(data: Dict[str, Any]) -> str:
        """Format financial health metrics."""
        return f"""=== FINANCIAL HEALTH ===
Debt/Equity: {data.get('debt_to_equity', 0):.2f}
Current Ratio: {data.get('current_ratio', 0):.2f}"""
