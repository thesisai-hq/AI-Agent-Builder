"""Web search tool implementation using yfinance news.

Fetches and formats recent news about companies.
"""

import logging
import yfinance as yf
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)


def web_search(ticker: str, query: Optional[str] = None, max_results: int = 10) -> str:
    """Search for company news and information using yfinance.
    
    Args:
        ticker: Stock ticker symbol
        query: Optional search query (not used, for future API integration)
        max_results: Maximum number of news items to return
        
    Returns:
        Formatted news and information as string
    """
    try:
        logger.info(f"Searching news for {ticker}")
        stock = yf.Ticker(ticker)
        
        # Get company info for context
        info = stock.info
        company_name = info.get('longName', ticker)
        sector = info.get('sector', 'Unknown')
        industry = info.get('industry', 'Unknown')
        
        # Get news
        news = stock.news
        
        if not news:
            return f"No recent news found for {ticker} ({company_name})"
        
        # Format output
        output = []
        output.append(f"=== NEWS FOR {ticker.upper()} ===")
        output.append(f"Company: {company_name}")
        output.append(f"Sector: {sector} | Industry: {industry}")
        output.append("")
        output.append(f"Recent News (Top {min(len(news), max_results)}):")
        output.append("=" * 60)
        output.append("")
        
        # Format each news item
        for i, item in enumerate(news[:max_results], 1):
            title = item.get('title', 'No title')
            publisher = item.get('publisher', 'Unknown')
            publish_time = item.get('providerPublishTime', 0)
            link = item.get('link', '')
            
            # Format timestamp
            if publish_time:
                date_str = datetime.fromtimestamp(publish_time).strftime('%Y-%m-%d %H:%M')
            else:
                date_str = 'Unknown date'
            
            output.append(f"{i}. {title}")
            output.append(f"   Source: {publisher} | Date: {date_str}")
            if link:
                output.append(f"   URL: {link}")
            output.append("")
        
        result = "\n".join(output)
        logger.info(f"Successfully retrieved {len(news[:max_results])} news items for {ticker}")
        return result
        
    except Exception as e:
        error_msg = f"Error fetching news for {ticker}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg
