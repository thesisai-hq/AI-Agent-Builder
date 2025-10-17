"""
Agent Context - Complete data access layer
Provides agents with access to all data sources
"""

from typing import Dict, Any, List, Optional
from agent_builder.config import Config
from agent_builder.utils import safe_execute
from agent_builder.repositories.connection import get_db_cursor
import logging

logger = logging.getLogger(__name__)


class AgentContext:
    """
    Context object for agents to fetch data

    Provides unified interface to:
    - Fundamental data (P/E, ROE, margins, etc.)
    - Balance sheet, cash flow, earnings
    - Price data and technical indicators
    - News, analyst ratings, insider trades
    - Risk metrics and options data
    - Macroeconomic indicators
    - SEC filings
    """

    # Whitelist of allowed metric names (SQL INJECTION PREVENTION)
    ALLOWED_METRICS = frozenset(
        [
            "ticker",
            "company_name",
            "sector",
            "industry",
            "market_cap",
            "enterprise_value",
            "pe_ratio",
            "forward_pe",
            "peg_ratio",
            "pb_ratio",
            "ps_ratio",
            "pcf_ratio",
            "dividend_yield",
            "earnings_per_share",
            "revenue",
            "revenue_growth",
            "net_income",
            "profit_margin",
            "operating_margin",
            "gross_margin",
            "roe",
            "roa",
            "roic",
            "debt_to_equity",
            "current_ratio",
            "quick_ratio",
            "cash_ratio",
            "interest_coverage",
            "asset_turnover",
            "inventory_turnover",
            "earnings_growth",
            "book_value_per_share",
            "beta",
        ]
    )

    def __init__(self, ticker: str):
        self.ticker = ticker
        self._cache = {}
        self._use_db = Config.is_postgres()

        # Cache statistics
        self._cache_hits = 0
        self._cache_misses = 0

    # ========================================================================
    # FUNDAMENTAL DATA
    # ========================================================================

    @safe_execute(default_return=0)
    def get_metric(self, metric_name: str, default: Any = 0) -> Any:
        """
        Get fundamental metric with SQL injection prevention

        Args:
            metric_name: Name of metric (must be in ALLOWED_METRICS)
            default: Default value if not found

        Returns:
            Metric value or default
        """
        # SECURITY: Validate metric name to prevent SQL injection
        if metric_name not in self.ALLOWED_METRICS:
            logger.warning(f"Invalid metric name: {metric_name}")
            return default

        # Check cache
        cache_key = f"metric_{metric_name}"
        if cache_key in self._cache:
            self._cache_hits += 1
            return self._cache[cache_key]

        self._cache_misses += 1

        if not self._use_db:
            return default

        with get_db_cursor() as cursor:
            if cursor is None:
                return default

            # SAFE: metric_name is validated, ticker is parameterized
            cursor.execute(
                f"SELECT {metric_name} FROM mock_fundamentals WHERE ticker = %s",
                (self.ticker,),
            )
            result = cursor.fetchone()

            value = result[0] if result and result[0] is not None else default
            self._cache[cache_key] = value
            return value

    @safe_execute(default_return={})
    def get_fundamentals(self) -> Dict[str, Any]:
        """Get all fundamental metrics"""
        cache_key = "fundamentals"
        if cache_key in self._cache:
            self._cache_hits += 1
            return self._cache[cache_key]

        self._cache_misses += 1

        if not self._use_db:
            return {}

        with get_db_cursor() as cursor:
            if cursor is None:
                return {}

            cursor.execute(
                "SELECT * FROM mock_fundamentals WHERE ticker = %s", (self.ticker,)
            )
            result = cursor.fetchone()

            if result:
                columns = [desc[0] for desc in cursor.description]
                data = dict(zip(columns, result))
            else:
                data = {}

            self._cache[cache_key] = data
            return data

    @safe_execute(default_return={})
    def get_balance_sheet(self, quarter: Optional[str] = None) -> Dict[str, Any]:
        """
        Get balance sheet data

        Args:
            quarter: Specific quarter (e.g., "2024-Q3") or None for latest

        Returns:
            Balance sheet data dict
        """
        cache_key = f"balance_sheet_{quarter or 'latest'}"
        if cache_key in self._cache:
            self._cache_hits += 1
            return self._cache[cache_key]

        self._cache_misses += 1

        if not self._use_db:
            return {}

        with get_db_cursor() as cursor:
            if cursor is None:
                return {}

            if quarter:
                cursor.execute(
                    """
                    SELECT * FROM mock_balance_sheet 
                    WHERE ticker = %s AND quarter = %s
                """,
                    (self.ticker, quarter),
                )
            else:
                cursor.execute(
                    """
                    SELECT * FROM mock_balance_sheet 
                    WHERE ticker = %s 
                    ORDER BY filing_date DESC LIMIT 1
                """,
                    (self.ticker,),
                )

            result = cursor.fetchone()
            if result:
                columns = [desc[0] for desc in cursor.description]
                data = dict(zip(columns, result))
                self._cache[cache_key] = data
                return data
            return {}

    @safe_execute(default_return={})
    def get_cash_flow(self, quarter: Optional[str] = None) -> Dict[str, Any]:
        """
        Get cash flow statement data

        Args:
            quarter: Specific quarter or None for latest

        Returns:
            Cash flow data dict
        """
        cache_key = f"cash_flow_{quarter or 'latest'}"
        if cache_key in self._cache:
            self._cache_hits += 1
            return self._cache[cache_key]

        self._cache_misses += 1

        if not self._use_db:
            return {}

        with get_db_cursor() as cursor:
            if cursor is None:
                return {}

            if quarter:
                cursor.execute(
                    """
                    SELECT * FROM mock_cash_flow 
                    WHERE ticker = %s AND quarter = %s
                """,
                    (self.ticker, quarter),
                )
            else:
                cursor.execute(
                    """
                    SELECT * FROM mock_cash_flow 
                    WHERE ticker = %s 
                    ORDER BY filing_date DESC LIMIT 1
                """,
                    (self.ticker,),
                )

            result = cursor.fetchone()
            if result:
                columns = [desc[0] for desc in cursor.description]
                data = dict(zip(columns, result))
                self._cache[cache_key] = data
                return data
            return {}

    @safe_execute(default_return={})
    def get_earnings(self, quarter: Optional[str] = None) -> Dict[str, Any]:
        """
        Get earnings report data

        Args:
            quarter: Specific quarter or None for latest

        Returns:
            Earnings data dict with EPS, revenue, surprises
        """
        cache_key = f"earnings_{quarter or 'latest'}"
        if cache_key in self._cache:
            self._cache_hits += 1
            return self._cache[cache_key]

        self._cache_misses += 1

        if not self._use_db:
            return {}

        with get_db_cursor() as cursor:
            if cursor is None:
                return {}

            if quarter:
                cursor.execute(
                    """
                    SELECT * FROM mock_earnings 
                    WHERE ticker = %s AND quarter = %s
                """,
                    (self.ticker, quarter),
                )
            else:
                cursor.execute(
                    """
                    SELECT * FROM mock_earnings 
                    WHERE ticker = %s 
                    ORDER BY earnings_date DESC LIMIT 1
                """,
                    (self.ticker,),
                )

            result = cursor.fetchone()
            if result:
                columns = [desc[0] for desc in cursor.description]
                data = dict(zip(columns, result))
                self._cache[cache_key] = data
                return data
            return {}

    # ========================================================================
    # TECHNICAL DATA
    # ========================================================================

    @safe_execute(default_return=[])
    def get_price_data(self, days: int = 30) -> List[Dict]:
        """
        Get recent price data (OHLCV)

        Args:
            days: Number of days to retrieve

        Returns:
            List of price dicts (date, open, high, low, close, volume)
        """
        cache_key = f"prices_{days}"
        if cache_key in self._cache:
            self._cache_hits += 1
            return self._cache[cache_key]

        self._cache_misses += 1

        if not self._use_db:
            return []

        with get_db_cursor() as cursor:
            if cursor is None:
                return []

            cursor.execute(
                """
                SELECT ticker, date, open, high, low, close, volume, vwap
                FROM mock_prices
                WHERE ticker = %s
                ORDER BY date DESC
                LIMIT %s
            """,
                (self.ticker, days),
            )

            results = cursor.fetchall()

            if results:
                columns = [desc[0] for desc in cursor.description]
                data = [dict(zip(columns, row)) for row in results]
                self._cache[cache_key] = data
                return data

            return []

    @safe_execute(default_return=[])
    def get_technical_indicators(self, days: int = 30) -> List[Dict]:
        """
        Get technical indicators (RSI, MACD, Bollinger, etc.)

        Args:
            days: Number of days to retrieve

        Returns:
            List of technical indicator dicts
        """
        cache_key = f"technical_{days}"
        if cache_key in self._cache:
            self._cache_hits += 1
            return self._cache[cache_key]

        self._cache_misses += 1

        if not self._use_db:
            return []

        with get_db_cursor() as cursor:
            if cursor is None:
                return []

            cursor.execute(
                """
                SELECT * FROM mock_technical_indicators
                WHERE ticker = %s
                ORDER BY date DESC LIMIT %s
            """,
                (self.ticker, days),
            )

            results = cursor.fetchall()
            if results:
                columns = [desc[0] for desc in cursor.description]
                data = [dict(zip(columns, row)) for row in results]
                self._cache[cache_key] = data
                return data
            return []

    @safe_execute(default_return={})
    def get_latest_technicals(self) -> Dict[str, Any]:
        """Get latest technical indicators"""
        cache_key = "technicals_latest"
        if cache_key in self._cache:
            self._cache_hits += 1
            return self._cache[cache_key]

        self._cache_misses += 1

        if not self._use_db:
            return {}

        with get_db_cursor() as cursor:
            if cursor is None:
                return {}

            cursor.execute(
                """
                SELECT * FROM mock_technical_indicators
                WHERE ticker = %s
                ORDER BY date DESC LIMIT 1
            """,
                (self.ticker,),
            )

            result = cursor.fetchone()
            if result:
                columns = [desc[0] for desc in cursor.description]
                data = dict(zip(columns, result))
                self._cache[cache_key] = data
                return data
            return {}

    # ========================================================================
    # SENTIMENT DATA
    # ========================================================================

    @safe_execute(default_return=[])
    def get_news(self, limit: int = 10) -> List[Dict]:
        """
        Get recent news articles with sentiment

        Args:
            limit: Maximum number of articles

        Returns:
            List of news article dicts
        """
        cache_key = f"news_{limit}"
        if cache_key in self._cache:
            self._cache_hits += 1
            return self._cache[cache_key]

        self._cache_misses += 1

        if not self._use_db:
            return []

        with get_db_cursor() as cursor:
            if cursor is None:
                return []

            cursor.execute(
                """
                SELECT ticker, headline, summary, sentiment, sentiment_score,
                       sentiment_confidence, category, relevance_score,
                       published_at, source, author, url
                FROM mock_news 
                WHERE ticker = %s 
                ORDER BY published_at DESC 
                LIMIT %s
            """,
                (self.ticker, limit),
            )

            results = cursor.fetchall()

            if results:
                columns = [desc[0] for desc in cursor.description]
                data = [dict(zip(columns, row)) for row in results]
                self._cache[cache_key] = data
                return data

            return []

    @safe_execute(default_return=[])
    def get_analyst_ratings(self, limit: int = 15) -> List[Dict]:
        """
        Get analyst ratings and price targets

        Args:
            limit: Maximum number of ratings

        Returns:
            List of analyst rating dicts
        """
        cache_key = f"ratings_{limit}"
        if cache_key in self._cache:
            self._cache_hits += 1
            return self._cache[cache_key]

        self._cache_misses += 1

        if not self._use_db:
            return []

        with get_db_cursor() as cursor:
            if cursor is None:
                return []

            cursor.execute(
                """
                SELECT ticker, analyst_firm, analyst_name, rating,
                       rating_change, price_target, previous_price_target,
                       rating_date
                FROM mock_analyst_ratings
                WHERE ticker = %s
                ORDER BY rating_date DESC
                LIMIT %s
            """,
                (self.ticker, limit),
            )

            results = cursor.fetchall()
            if results:
                columns = [desc[0] for desc in cursor.description]
                data = [dict(zip(columns, row)) for row in results]
                self._cache[cache_key] = data
                return data
            return []

    @safe_execute(default_return=[])
    def get_insider_trades(self, limit: int = 15) -> List[Dict]:
        """
        Get insider trading transactions

        Args:
            limit: Maximum number of trades

        Returns:
            List of insider trade dicts
        """
        cache_key = f"insider_{limit}"
        if cache_key in self._cache:
            self._cache_hits += 1
            return self._cache[cache_key]

        self._cache_misses += 1

        if not self._use_db:
            return []

        with get_db_cursor() as cursor:
            if cursor is None:
                return []

            cursor.execute(
                """
                SELECT ticker, insider_name, insider_title, transaction_type,
                       shares, price_per_share, transaction_value,
                       transaction_date, filing_date
                FROM mock_insider_trades
                WHERE ticker = %s
                ORDER BY transaction_date DESC
                LIMIT %s
            """,
                (self.ticker, limit),
            )

            results = cursor.fetchall()

            if results:
                columns = [desc[0] for desc in cursor.description]
                data = [dict(zip(columns, row)) for row in results]
                self._cache[cache_key] = data
                return data

            return []

    # ========================================================================
    # RISK DATA
    # ========================================================================

    @safe_execute(default_return={})
    def get_latest_risk_metrics(self) -> Dict[str, Any]:
        """
        Get latest risk metrics

        Returns:
            Risk metrics dict (volatility, VaR, Sharpe, drawdown, etc.)
        """
        cache_key = "risk_latest"
        if cache_key in self._cache:
            self._cache_hits += 1
            return self._cache[cache_key]

        self._cache_misses += 1

        if not self._use_db:
            return {}

        with get_db_cursor() as cursor:
            if cursor is None:
                return {}

            cursor.execute(
                """
                SELECT * FROM mock_risk_metrics
                WHERE ticker = %s
                ORDER BY date DESC LIMIT 1
            """,
                (self.ticker,),
            )

            result = cursor.fetchone()
            if result:
                columns = [desc[0] for desc in cursor.description]
                data = dict(zip(columns, result))
                self._cache[cache_key] = data
                return data
            return {}

    @safe_execute(default_return={})
    def get_latest_options_data(self) -> Dict[str, Any]:
        """
        Get latest options market data

        Returns:
            Options data dict (put/call ratio, implied volatility, etc.)
        """
        cache_key = "options_latest"
        if cache_key in self._cache:
            self._cache_hits += 1
            return self._cache[cache_key]

        self._cache_misses += 1

        if not self._use_db:
            return {}

        with get_db_cursor() as cursor:
            if cursor is None:
                return {}

            cursor.execute(
                """
                SELECT * FROM mock_options_data
                WHERE ticker = %s
                ORDER BY date DESC LIMIT 1
            """,
                (self.ticker,),
            )

            result = cursor.fetchone()
            if result:
                columns = [desc[0] for desc in cursor.description]
                data = dict(zip(columns, result))
                self._cache[cache_key] = data
                return data
            return {}

    # ========================================================================
    # MACRO DATA
    # ========================================================================

    @safe_execute(default_return={})
    def get_macro_indicators(self) -> Dict[str, Any]:
        """
        Get latest macroeconomic indicators (shared across all tickers)

        Returns:
            Macro data dict (Fed rates, GDP, inflation, VIX, etc.)
        """
        cache_key = "macro_latest"
        if cache_key in self._cache:
            self._cache_hits += 1
            return self._cache[cache_key]

        self._cache_misses += 1

        if not self._use_db:
            return {}

        with get_db_cursor() as cursor:
            if cursor is None:
                return {}

            cursor.execute(
                """
                SELECT * FROM mock_macro_indicators
                ORDER BY date DESC LIMIT 1
            """
            )

            result = cursor.fetchone()
            if result:
                columns = [desc[0] for desc in cursor.description]
                data = dict(zip(columns, result))
                self._cache[cache_key] = data
                return data
            return {}

    # ========================================================================
    # SEC FILINGS
    # ========================================================================

    @safe_execute(default_return=[])
    def get_sec_filings(
        self, filing_type: Optional[str] = None, limit: int = 5
    ) -> List[Dict]:
        """
        Get SEC filings (10-K, 10-Q, 8-K)

        Args:
            filing_type: Filter by type (e.g., "10-K") or None for all
            limit: Maximum number of filings

        Returns:
            List of SEC filing dicts
        """
        cache_key = f"sec_{filing_type or 'all'}_{limit}"
        if cache_key in self._cache:
            self._cache_hits += 1
            return self._cache[cache_key]

        self._cache_misses += 1

        if not self._use_db:
            return []

        with get_db_cursor() as cursor:
            if cursor is None:
                return []

            if filing_type:
                cursor.execute(
                    """
                    SELECT * FROM mock_sec_filings
                    WHERE ticker = %s AND filing_type = %s
                    ORDER BY filing_date DESC LIMIT %s
                """,
                    (self.ticker, filing_type, limit),
                )
            else:
                cursor.execute(
                    """
                    SELECT * FROM mock_sec_filings
                    WHERE ticker = %s
                    ORDER BY filing_date DESC LIMIT %s
                """,
                    (self.ticker, limit),
                )

            results = cursor.fetchall()
            if results:
                columns = [desc[0] for desc in cursor.description]
                data = [dict(zip(columns, row)) for row in results]
                self._cache[cache_key] = data
                return data
            return []

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    @safe_execute(default_return=0.0)
    def get_latest_price(self) -> float:
        """
        Get latest closing price

        Returns:
            Latest close price as float
        """
        cache_key = "price_latest"
        if cache_key in self._cache:
            self._cache_hits += 1
            return self._cache[cache_key]

        self._cache_misses += 1

        prices = self.get_price_data(days=1)
        if prices:
            price = float(prices[0].get("close", 0))
            self._cache[cache_key] = price
            return price
        return 0.0

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache performance statistics

        Returns:
            Dict with cache size, hits, misses, hit rate
        """
        total_requests = self._cache_hits + self._cache_misses
        hit_rate = self._cache_hits / total_requests if total_requests > 0 else 0

        return {
            "size": len(self._cache),
            "hits": self._cache_hits,
            "misses": self._cache_misses,
            "hit_rate": round(hit_rate, 3),
        }
