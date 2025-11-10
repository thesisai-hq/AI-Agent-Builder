"""Tool implementations for LLM agents.

Provides fully functional tools for AI-powered investment analysis:
- web_search: Search for company news using yfinance
- financial_data: Comprehensive financial analysis
- calculator: Financial valuation models (DCF, P/E, Graham, Altman)
- document_analysis: RAG-based document analysis (Phase 2+)
"""

import logging
from typing import Dict, Any, Optional, List

# Import enhanced tool implementations
from .web_search import web_search as web_search_impl
from .financial_data import financial_data as financial_data_impl
from .calculator import calculator as calculator_impl
from .document_analysis import document_analysis as document_analysis_impl

logger = logging.getLogger(__name__)


class ToolRegistry:
    """Registry of available tools for LLM agents."""
    
    def __init__(self):
        """Initialize tool registry with available tools."""
        self.tools = {
            'web_search': self.web_search,
            'financial_data': self.financial_data,
            'calculator': self.calculator,
            'document_analysis': self.document_analysis,
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
            available = ', '.join(self.tools.keys())
            return f"Error: Tool '{tool_name}' not available. Available tools: {available}"
        
        try:
            logger.info(f"Executing tool: {tool_name} with args: {kwargs}")
            result = self.tools[tool_name](**kwargs)
            logger.info(f"Tool {tool_name} executed successfully")
            return result
        except Exception as e:
            error_msg = f"Error executing {tool_name}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return error_msg
    
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
📰 WEB_SEARCH: Search for recent company news and information
   - Fetches latest news articles from multiple sources
   - Provides company context (sector, industry)
   - Includes publication dates and sources
   - Usage: web_search(ticker="AAPL")
   - Example results: Recent earnings announcements, product launches, management changes
""")
        
        if 'financial_data' in enabled_tools:
            descriptions.append("""
📊 FINANCIAL_DATA: Access comprehensive financial analysis
   - Complete financial statements (Income, Balance Sheet, Cash Flow)
   - Analyst ratings and price targets
   - Trading information (volume, 52-week range, beta)
   - Ownership data (institutional, insider holdings)
   - Dividend information
   - Usage: financial_data(ticker="AAPL", include_statements=True)
   - Provides deep financial insights for valuation
""")
        
        if 'calculator' in enabled_tools:
            descriptions.append("""
🧮 CALCULATOR: Financial valuation models and calculations
   - DCF Valuation: Discounted Cash Flow model
     Usage: calculator(ticker="AAPL", model="dcf", growth_rate=0.10, discount_rate=0.10)
   
   - P/E Valuation: Price-to-Earnings based valuation
     Usage: calculator(ticker="AAPL", model="pe", target_pe=20)
   
   - Graham Number: Benjamin Graham's intrinsic value formula
     Usage: calculator(ticker="AAPL", model="graham")
   
   - Altman Z-Score: Bankruptcy prediction model
     Usage: calculator(ticker="AAPL", model="altman")
   
   - Mathematical Expressions: calculator(expression="sqrt(100) + 2*5")
""")
        
        if 'document_analysis' in enabled_tools:
            descriptions.append("""
📄 DOCUMENT_ANALYSIS: Analyze uploaded documents (RAG)
   - Query knowledge from user-uploaded PDFs, DOCs, TXT files
   - Extracts relevant context for investment decisions
   - Usage: document_analysis(ticker="AAPL", agent_id="your_agent_id")
   - Note: Requires documents to be uploaded first
   - Currently in development (Phase 2+)
""")
        
        if descriptions:
            header = "\n=== AVAILABLE TOOLS ===\n"
            header += "You have access to the following tools to help with your analysis:\n"
            return header + "\n".join(descriptions)
        return ""
    
    def list_tools(self) -> Dict[str, str]:
        """List all available tools with descriptions.
        
        Returns:
            Dictionary of tool names and descriptions
        """
        return {
            'web_search': 'Search for company news and information',
            'financial_data': 'Access comprehensive financial data and analysis',
            'calculator': 'Financial valuation models (DCF, P/E, Graham, Altman)',
            'document_analysis': 'Analyze uploaded documents (RAG) - Phase 2+'
        }
    
    # Tool implementations
    
    def web_search(self, ticker: str, query: Optional[str] = None, max_results: int = 10) -> str:
        """Search for company news using yfinance.
        
        Args:
            ticker: Stock ticker symbol
            query: Optional search query (for future enhancement)
            max_results: Maximum number of news items
            
        Returns:
            Formatted news and information
        """
        return web_search_impl(ticker, query, max_results)
    
    def financial_data(self, ticker: str, include_statements: bool = True) -> str:
        """Get comprehensive financial data and analysis.
        
        Args:
            ticker: Stock ticker symbol
            include_statements: Include financial statements
            
        Returns:
            Formatted financial data
        """
        return financial_data_impl(ticker, include_statements)
    
    def calculator(
        self,
        expression: Optional[str] = None,
        ticker: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs
    ) -> str:
        """Financial calculator with valuation models.
        
        Args:
            expression: Mathematical expression to evaluate
            ticker: Stock ticker (required for valuation models)
            model: Valuation model (dcf, pe, graham, altman)
            **kwargs: Model-specific parameters
            
        Returns:
            Calculation results
        """
        return calculator_impl(expression, ticker, model, **kwargs)
    
    def document_analysis(
        self,
        ticker: str,
        agent_id: Optional[str] = None,
        query: Optional[str] = None,
        n_results: int = 5
    ) -> str:
        """Analyze documents using RAG system.
        
        Args:
            ticker: Stock ticker symbol
            agent_id: Agent ID (required for accessing agent's documents)
            query: Optional specific query
            n_results: Number of relevant chunks to retrieve
            
        Returns:
            Relevant context from uploaded documents
        """
        return document_analysis_impl(ticker, agent_id, query, n_results)


# Global tool registry
tool_registry = ToolRegistry()
