"""Tool implementations for LLM agents.

Provides actual functionality for the tools that can be enabled:
- web_search: Search for company information
- financial_data: Get additional financial metrics
- document_analysis: Analyze text documents (placeholder)
- calculator: Mathematical calculations
"""

import yfinance as yf
from typing import Dict, Any, Optional, List


class ToolRegistry:
    """Registry of available tools for LLM agents."""
    
    def __init__(self):
        self.tools = {
            'web_search': self.web_search,
            'financial_data': self.financial_data,
            'document_analysis': self.document_analysis,
            'calculator': self.calculator,
        }
    
    def execute(self, tool_name: str, **kwargs) -> str:
        """Execute a tool by name.
        
        Args:
            tool_name: Name of the tool
            **kwargs: Tool arguments
            
        Returns:
            Tool result as string
        """
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not available"
        
        try:
            return self.tools[tool_name](**kwargs)
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"
    
    def get_tool_descriptions(self, enabled_tools: List[str]) -> str:
        """Get descriptions of enabled tools for LLM prompt.
        
        Args:
            enabled_tools: List of enabled tool names
            
        Returns:
            Formatted tool descriptions
        """
        descriptions = []
        
        if 'web_search' in enabled_tools:
            descriptions.append("""
WEB_SEARCH: Search for recent company news and information
- Use this to get latest news, analyst opinions, company developments
- Example: Recent earnings announcements, product launches, management changes
""")
        
        if 'financial_data' in enabled_tools:
            descriptions.append("""
FINANCIAL_DATA: Access additional detailed financial metrics
- Get analyst targets, recommendations, institutional holders
- View financial statements (income, balance sheet, cash flow)
- See trading volume, 52-week ranges, beta
""")
        
        if 'document_analysis' in enabled_tools:
            descriptions.append("""
DOCUMENT_ANALYSIS: Analyze company documents and filings
- Review SEC filings, annual reports, earnings transcripts
- Extract key information from documents
""")
        
        if 'calculator' in enabled_tools:
            descriptions.append("""
CALCULATOR: Perform complex financial calculations
- Calculate intrinsic value, DCF models, custom ratios
- Mathematical operations beyond basic metrics
""")
        
        if descriptions:
            return "\nYou have access to these tools:\n" + "\n".join(descriptions)
        return ""
    
    def web_search(self, ticker: str, query: Optional[str] = None) -> str:
        """Search for company news and information.
        
        Args:
            ticker: Stock ticker
            query: Optional specific query
            
        Returns:
            News and information as string
        """
        try:
            stock = yf.Ticker(ticker)
            
            # Get news
            news = stock.news
            
            if not news:
                return f"No recent news found for {ticker}"
            
            # Format top 5 news items
            news_items = []
            for item in news[:5]:
                title = item.get('title', 'No title')
                publisher = item.get('publisher', 'Unknown')
                news_items.append(f"- {title} ({publisher})")
            
            return "Recent News:\n" + "\n".join(news_items)
            
        except Exception as e:
            return f"Error fetching news: {str(e)}"
    
    def financial_data(self, ticker: str) -> str:
        """Get additional financial data and metrics.
        
        Args:
            ticker: Stock ticker
            
        Returns:
            Additional financial data as string
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            data = []
            
            # Analyst data
            target_high = info.get('targetHighPrice', 0)
            target_low = info.get('targetLowPrice', 0)
            target_mean = info.get('targetMeanPrice', 0)
            recommendations = info.get('recommendationKey', 'N/A')
            
            if target_mean:
                data.append(f"Analyst Target: ${target_mean:.2f} (Range: ${target_low:.2f} - ${target_high:.2f})")
            if recommendations:
                data.append(f"Analyst Recommendation: {recommendations}")
            
            # Trading data
            volume = info.get('volume', 0)
            avg_volume = info.get('averageVolume', 0)
            week_52_high = info.get('fiftyTwoWeekHigh', 0)
            week_52_low = info.get('fiftyTwoWeekLow', 0)
            beta = info.get('beta', 0)
            
            if volume:
                data.append(f"Volume: {volume:,} (Avg: {avg_volume:,})")
            if week_52_high and week_52_low:
                data.append(f"52-Week Range: ${week_52_low:.2f} - ${week_52_high:.2f}")
            if beta:
                data.append(f"Beta: {beta:.2f}")
            
            # Institutional holdings
            inst_holdings = info.get('heldPercentInstitutions', 0)
            if inst_holdings:
                data.append(f"Institutional Ownership: {inst_holdings * 100:.1f}%")
            
            # Business description
            business = info.get('longBusinessSummary', '')
            if business:
                # Truncate to first 200 chars
                summary = business[:200] + "..." if len(business) > 200 else business
                data.append(f"\nBusiness: {summary}")
            
            return "\n".join(data) if data else "No additional data available"
            
        except Exception as e:
            return f"Error fetching financial data: {str(e)}"
    
    def document_analysis(self, ticker: str, document_type: str = "earnings") -> str:
        """Analyze company documents (placeholder - basic implementation).
        
        Args:
            ticker: Stock ticker
            document_type: Type of document to analyze
            
        Returns:
            Document analysis as string
        """
        # Placeholder - in a full implementation, this would:
        # 1. Fetch SEC filings from EDGAR
        # 2. Download earnings transcripts
        # 3. Parse and summarize documents
        
        # For now, get basic info from yfinance
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get earnings data
            earnings = stock.earnings
            if earnings is not None and not earnings.empty:
                recent_earnings = earnings.tail(4)
                return f"Recent Earnings (Last 4 Quarters):\n{recent_earnings.to_string()}"
            
            return "No earnings document data available via yfinance. Full document analysis requires SEC EDGAR integration."
            
        except Exception as e:
            return f"Error in document analysis: {str(e)}"
    
    def calculator(self, expression: str) -> str:
        """Perform mathematical calculations.
        
        Args:
            expression: Math expression to evaluate
            
        Returns:
            Calculation result as string
        """
        try:
            from simpleeval import simple_eval
            import math
            
            functions = {
                'sqrt': math.sqrt,
                'abs': abs,
                'log': math.log,
                'exp': math.exp,
                'pow': pow,
                'max': max,
                'min': min,
            }
            
            result = simple_eval(expression, functions=functions)
            return f"Calculation result: {result}"
            
        except Exception as e:
            return f"Calculation error: {str(e)}"


# Global tool registry
tool_registry = ToolRegistry()
