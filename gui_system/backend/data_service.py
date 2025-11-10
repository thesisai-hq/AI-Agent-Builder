"""Data service using yfinance with caching and timeout protection.

Caches stock data for 5 minutes to reduce API calls and improve response times.
Includes timeout protection to prevent hanging requests.
"""

import yfinance as yf
import logging
from typing import Dict, Any, Optional
from .data_cache import data_cache, price_history_cache
from .constants import (
    YFINANCE_TIMEOUT_SECONDS,
    YFINANCE_MAX_RETRIES,
    YFINANCE_BACKOFF_FACTOR
)

# Setup logging
logger = logging.getLogger(__name__)


class YFinanceDataService:
    """Fetch stock data from Yahoo Finance with caching and timeout protection."""
    
    def get_stock_data(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive stock data for a ticker.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
            
        Returns:
            Dictionary with normalized financial data, or None if failed
        """
        # Check cache first
        ticker_upper = ticker.upper()
        cached_data = data_cache.get(ticker_upper)
        if cached_data is not None:
            logger.debug(f"Cache hit for {ticker_upper}")
            return cached_data
        
        # Fetch from API with timeout protection
        logger.info(f"Fetching data for {ticker_upper} from yfinance")
        try:
            # Note: yfinance doesn't directly support timeout in Ticker()
            # but requests library underneath does. We set a reasonable timeout.
            stock = yf.Ticker(ticker, session=self._get_session_with_timeout())
            info = stock.info
            
            # Normalize data to match agent field names
            data = {
                'ticker': ticker_upper,
                
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
            
            # Cache the result
            data_cache.set(ticker_upper, data)
            logger.info(f"Successfully fetched and cached data for {ticker_upper}")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {e}", exc_info=True)
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
        # Check cache first
        cache_key = f"{ticker.upper()}_{period}_{interval}"
        cached_history = price_history_cache.get(cache_key)
        if cached_history is not None:
            logger.debug(f"Cache hit for price history: {cache_key}")
            return cached_history
        
        # Fetch from API with timeout protection
        logger.info(f"Fetching price history for {cache_key} from yfinance")
        try:
            stock = yf.Ticker(ticker, session=self._get_session_with_timeout())
            history = stock.history(period=period, interval=interval)
            
            # Cache the result
            price_history_cache.set(cache_key, history)
            logger.info(f"Successfully fetched and cached price history for {cache_key}")
            return history
        except Exception as e:
            logger.error(f"Error fetching history for {ticker}: {e}", exc_info=True)
            return None
    
    def validate_ticker(self, ticker: str) -> bool:
        """Check if ticker exists and has data.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            True if ticker is valid and has data
        """
        try:
            stock = yf.Ticker(ticker, session=self._get_session_with_timeout())
            info = stock.info
            # Check if has meaningful data (has a market cap or price)
            is_valid = bool(info.get('marketCap') or info.get('currentPrice') or info.get('regularMarketPrice'))
            if is_valid:
                logger.debug(f"Ticker {ticker} validated successfully")
            else:
                logger.warning(f"Ticker {ticker} validation failed: no market data")
            return is_valid
        except Exception as e:
            logger.error(f"Ticker validation error for {ticker}: {e}")
            return False
    
    def clear_cache(self, ticker: Optional[str] = None) -> None:
        """Clear cache for specific ticker or all cached data.
        
        Args:
            ticker: Specific ticker to clear, or None to clear all
        """
        if ticker:
            ticker_upper = ticker.upper()
            data_cache.clear(ticker_upper)
            logger.info(f"Cleared cache for {ticker_upper}")
        else:
            data_cache.clear()
            price_history_cache.clear()
            logger.info("Cleared all caches")
    
    @staticmethod
    def _get_session_with_timeout():
        """Create requests session with timeout.
        
        Returns:
            requests.Session with timeout configured
        """
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        session = requests.Session()
        
        # Configure retries
        retry_strategy = Retry(
            total=YFINANCE_MAX_RETRIES,
            backoff_factor=YFINANCE_BACKOFF_FACTOR,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set timeout for all requests
        # This is a monkey-patch approach since yfinance doesn't expose timeout directly
        original_request = session.request
        
        def request_with_timeout(*args, **kwargs):
            kwargs.setdefault('timeout', YFINANCE_TIMEOUT_SECONDS)
            return original_request(*args, **kwargs)
        
        session.request = request_with_timeout
        
        return session


# Global instance (simple, no DI for now)
data_service = YFinanceDataService()
