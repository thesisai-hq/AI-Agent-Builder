"""Data access context for agents"""

from typing import Optional, Any
import logging

logger = logging.getLogger(__name__)


class AgentContext:
    def __init__(self, ticker: str, db):
        self.ticker = ticker
        self.db = db
        self._cache = {}
    
    def get_fundamental(self, metric: str, default: Any = None) -> Any:
        cache_key = f"fundamental_{metric}"
        if cache_key not in self._cache:
            try:
                value = self.db.execute_value(
                    f"SELECT {metric} FROM mock_fundamentals WHERE ticker = %s",
                    (self.ticker,), default=default
                )
                self._cache[cache_key] = value
            except Exception as e:
                logger.error(f"Error fetching {metric}: {e}")
                self._cache[cache_key] = default
        return self._cache[cache_key]
    
    def get_fundamentals(self) -> dict:
        cache_key = "fundamentals"
        if cache_key not in self._cache:
            try:
                result = self.db.execute_one(
                    "SELECT * FROM mock_fundamentals WHERE ticker = %s",
                    (self.ticker,)
                )
                self._cache[cache_key] = result or {}
            except Exception as e:
                logger.error(f"Error: {e}")
                self._cache[cache_key] = {}
        return self._cache[cache_key]
    
    def get_price_data(self, days: int = 30) -> list:
        try:
            return self.db.execute(
                """SELECT ticker, date, open, high, low, close, volume,
                   sma_20, sma_50, sma_200, rsi_14
                   FROM mock_prices WHERE ticker = %s 
                   ORDER BY date DESC LIMIT %s""",
                (self.ticker, days)
            )
        except:
            return []
    
    def get_news(self, limit: int = 10) -> list:
        try:
            return self.db.execute(
                """SELECT headline, summary, sentiment, sentiment_score,
                   published_at, source, keywords
                   FROM mock_news WHERE ticker = %s 
                   ORDER BY published_at DESC LIMIT %s""",
                (self.ticker, limit)
            )
        except:
            return []
    
    def get_analyst_ratings(self, limit: int = 10) -> list:
        try:
            return self.db.execute(
                """SELECT analyst_firm, rating, price_target,
                   previous_rating, rating_date, analyst_name
                   FROM mock_analyst_ratings WHERE ticker = %s
                   ORDER BY rating_date DESC LIMIT %s""",
                (self.ticker, limit)
            )
        except:
            return []
    
    def get_insider_trades(self, limit: int = 15) -> list:
        try:
            return self.db.execute(
                """SELECT insider_name, position, transaction_type,
                   shares, price_per_share, transaction_date
                   FROM mock_insider_trades WHERE ticker = %s
                   ORDER BY transaction_date DESC LIMIT %s""",
                (self.ticker, limit)
            )
        except:
            return []
    
    def get_sec_filings(self, limit: int = 5) -> list:
        try:
            return self.db.execute(
                """SELECT filing_type, filing_date, revenue, net_income,
                   eps, risk_factors, sentiment_score, fiscal_quarter
                   FROM mock_sec_filings WHERE ticker = %s
                   ORDER BY filing_date DESC LIMIT %s""",
                (self.ticker, limit)
            )
        except:
            return []
    
    def get_options_data(self) -> dict:
        try:
            calls = self.db.execute(
                """SELECT strike_price, implied_volatility, volume, 
                   open_interest, delta FROM mock_options 
                   WHERE ticker = %s AND option_type = 'CALL'
                   ORDER BY volume DESC LIMIT 5""",
                (self.ticker,)
            )
            puts = self.db.execute(
                """SELECT strike_price, implied_volatility, volume,
                   open_interest, delta FROM mock_options
                   WHERE ticker = %s AND option_type = 'PUT'
                   ORDER BY volume DESC LIMIT 5""",
                (self.ticker,)
            )
            return {"calls": calls, "puts": puts}
        except:
            return {"calls": [], "puts": []}
    
    def get_macro_indicators(self) -> list:
        try:
            return self.db.execute(
                """SELECT indicator_name, value, previous_value, 
                   date, unit FROM mock_macro_indicators
                   ORDER BY date DESC LIMIT 10"""
            )
        except:
            return []
