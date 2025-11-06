"""Simple data service using yfinance to fetch real-time stock data.

No database, no caching - just direct API calls.
Clean and simple for immediate use.
"""

import yfinance as yf
from typing import Dict, Any, Optional


class YFinanceDataService:
    """Fetch stock data from Yahoo Finance."""
    
    def get_stock_data(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive stock data for a ticker.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
            
        Returns:
            Dictionary with normalized financial data, or None if failed
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Normalize data to match agent field names
            return {
                'ticker': ticker.upper(),
                
                # Valuation metrics
                'pe_ratio': info.get('trailingPE') or info.get('forwardPE') or 0,
                'pb_ratio': info.get('priceToBook', 0),
                'peg_ratio': info.get('pegRatio', 0),
                
                # Dividend metrics
                'dividend_yield': (info.get('dividendYield', 0) * 100) if info.get('dividendYield') else 0,
                'payout_ratio': (info.get('payoutRatio', 0) * 100) if info.get('payoutRatio') else 0,
                
                # Growth metrics
                'revenue_growth': (info.get('revenueGrowth', 0) * 100) if info.get('revenueGrowth') else 0,
                'earnings_growth': (info.get('earningsGrowth', 0) * 100) if info.get('earningsGrowth') else 0,
                
                # Profitability metrics
                'profit_margin': (info.get('profitMargins', 0) * 100) if info.get('profitMargins') else 0,
                'roe': (info.get('returnOnEquity', 0) * 100) if info.get('returnOnEquity') else 0,
                'roa': (info.get('returnOnAssets', 0) * 100) if info.get('returnOnAssets') else 0,
                
                # Financial health
                'debt_to_equity': info.get('debtToEquity', 0),
                'current_ratio': info.get('currentRatio', 0),
                'quick_ratio': info.get('quickRatio', 0),
                
                # Per-share metrics
                'eps': info.get('trailingEps', 0),
                'book_value_per_share': info.get('bookValue', 0),
                
                # Price metrics
                'price': info.get('currentPrice') or info.get('regularMarketPrice', 0),
                'market_cap': info.get('marketCap', 0),
                
                # Company info
                'company_name': info.get('longName', ticker),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                
                # Additional useful fields for formulas
                'ebit': info.get('ebit', 0),
                'enterprise_value': info.get('enterpriseValue', 0),
                'free_cash_flow': info.get('freeCashflow', 0),
                
                # Metadata
                'data_source': 'yfinance',
                'currency': info.get('currency', 'USD'),
            }
            
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None
    
    def get_price_history(
        self, 
        ticker: str, 
        period: str = "1y",
        interval: str = "1d"
    ) -> Optional[Any]:
        """Get historical price data.
        
        Args:
            ticker: Stock ticker symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
            
        Returns:
            Pandas DataFrame with OHLCV data, or None if failed
        """
        try:
            stock = yf.Ticker(ticker)
            history = stock.history(period=period, interval=interval)
            return history
        except Exception as e:
            print(f"Error fetching history for {ticker}: {e}")
            return None
    
    def validate_ticker(self, ticker: str) -> bool:
        """Check if ticker exists and has data.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            True if ticker is valid and has data
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            # Check if has meaningful data (has a market cap or price)
            return bool(info.get('marketCap') or info.get('currentPrice') or info.get('regularMarketPrice'))
        except Exception:
            return False


# Global instance (simple, no DI for now)
data_service = YFinanceDataService()
