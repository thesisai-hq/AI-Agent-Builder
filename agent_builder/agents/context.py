"""
Agent Context - UPDATED with new data access methods
"""

from typing import Dict, Any, List
from agent_builder.config import Config
from agent_builder.utils import safe_execute
from agent_builder.repositories.connection import get_db_cursor
import logging

logger = logging.getLogger(__name__)


class AgentContext:
    """Context object for agents to fetch data"""

    def __init__(self, ticker: str):
        self.ticker = ticker
        self._cache = {}
        self._use_db = Config.is_postgres()

    # ========================================================================
    # FUNDAMENTAL DATA
    # ========================================================================

    @safe_execute(default_return=0)
    def get_metric(self, metric_name: str, default: Any = 0) -> Any:
        """Get fundamental metric"""
        cache_key = f"metric_{metric_name}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        if not self._use_db:
            return default

        with get_db_cursor() as cursor:
            if cursor is None:
                return default

            # Whitelist of allowed metrics
            allowed_metrics = {
                "pe_ratio",
                "pb_ratio",
                "ps_ratio",
                "market_cap",
                "revenue",
                "net_income",
                "profit_margin",
                "roe",
                "roa",
                "roic",
                "debt_to_equity",
                "current_ratio",
                "beta",
                "dividend_yield",
                "earnings_per_share",
                "revenue_growth",
                "earnings_growth",
                "sector",
                "industry",
                "company_name",
            }

            if metric_name not in allowed_metrics:
                logger.warning(f"Invalid metric name: {metric_name}")
                return default

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
        """Get all fundamentals"""
        cache_key = "fundamentals"
        if cache_key in self._cache:
            return self._cache[cache_key]

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
    def get_balance_sheet(self, quarter: str = None) -> Dict[str, Any]:
        """Get balance sheet data"""
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
                return dict(zip(columns, result))
            return {}

    @safe_execute(default_return={})
    def get_cash_flow(self, quarter: str = None) -> Dict[str, Any]:
        """Get cash flow data"""
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
                return dict(zip(columns, result))
            return {}

    @safe_execute(default_return={})
    def get_earnings(self, quarter: str = None) -> Dict[str, Any]:
        """Get earnings data"""
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
                return dict(zip(columns, result))
            return {}

    # ========================================================================
    # TECHNICAL DATA
    # ========================================================================

    @safe_execute(default_return=[])
    def get_price_data(self, days: int = 30) -> List[Dict]:
        """Get recent price data"""
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
                return [dict(zip(columns, row)) for row in results]

            return []

    @safe_execute(default_return=[])
    def get_technical_indicators(self, days: int = 30) -> List[Dict]:
        """Get technical indicators"""
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
                return [dict(zip(columns, row)) for row in results]
            return []

    @safe_execute(default_return={})
    def get_latest_technicals(self) -> Dict[str, Any]:
        """Get latest technical indicators"""
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
                return dict(zip(columns, result))
            return {}

    # ========================================================================
    # SENTIMENT DATA
    # ========================================================================

    @safe_execute(default_return=[])
    def get_news(self, limit: int = 10) -> List[Dict]:
        """Get recent news"""
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
                return [dict(zip(columns, row)) for row in results]

            return []

    @safe_execute(default_return=[])
    def get_analyst_ratings(self, limit: int = 15) -> List[Dict]:
        """Get analyst ratings"""
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
                return [dict(zip(columns, row)) for row in results]
            return []

    @safe_execute(default_return=[])
    def get_insider_trades(self, limit: int = 15) -> List[Dict]:
        """Get insider trades"""
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
                return [dict(zip(columns, row)) for row in results]

            return []

    # ========================================================================
    # RISK DATA
    # ========================================================================

    @safe_execute(default_return={})
    def get_latest_risk_metrics(self) -> Dict[str, Any]:
        """Get latest risk metrics"""
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
                return dict(zip(columns, result))
            return {}

    @safe_execute(default_return={})
    def get_latest_options_data(self) -> Dict[str, Any]:
        """Get latest options data"""
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
                return dict(zip(columns, result))
            return {}

    # ========================================================================
    # MACRO DATA
    # ========================================================================

    @safe_execute(default_return={})
    def get_macro_indicators(self) -> Dict[str, Any]:
        """Get latest macro indicators"""
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
                return dict(zip(columns, result))
            return {}

    # ========================================================================
    # SEC FILINGS
    # ========================================================================

    @safe_execute(default_return=[])
    def get_sec_filings(self, filing_type: str = None, limit: int = 5) -> List[Dict]:
        """Get SEC filings"""
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
                return [dict(zip(columns, row)) for row in results]
            return []

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def get_latest_price(self) -> float:
        """Get latest closing price"""
        prices = self.get_price_data(days=1)
        if prices:
            return prices[0].get("close", 0)
        return 0
