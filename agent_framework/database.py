"""PostgreSQL database with connection pooling, transactions, and error handling.

Compatible with thesis-data-fabric production database schema.
"""

import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional

import asyncpg

from .models import DatabaseConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Base exception for database errors."""

    pass


class DBConnectionError(DatabaseError):
    """Database connection error."""

    pass


class QueryError(DatabaseError):
    """Database query error."""

    pass


class Database:
    """PostgreSQL database with connection pooling.

    Compatible with thesis-data-fabric schema (thesis_data.*).

    Features:
    - Connection pooling (2-10 connections by default)
    - Transaction support for atomic operations
    - Comprehensive error handling
    - Async operations with asyncpg
    """

    def __init__(self, connection_string: str, config: Optional[DatabaseConfig] = None):
        self.connection_string = connection_string
        self.config = config or DatabaseConfig(connection_string=connection_string)
        self._pool: Optional[asyncpg.Pool] = None

    async def connect(self) -> None:
        """Create connection pool."""
        if self._pool is not None:
            logger.warning("Database already connected")
            return
        try:
            self._pool = await asyncpg.create_pool(
                self.connection_string,
                min_size=self.config.min_pool_size,
                max_size=self.config.max_pool_size,
                command_timeout=self.config.command_timeout,
                max_queries=self.config.max_queries,
                max_inactive_connection_lifetime=self.config.max_inactive_connection_lifetime,
            )
            logger.info(
                f"Database connected (pool: {self.config.min_pool_size}-{self.config.max_pool_size})"
            )
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise DBConnectionError(f"Could not connect to database: {e}") from e

    async def disconnect(self) -> None:
        """Close connection pool."""
        if self._pool:
            await self._pool.close()
            self._pool = None
            logger.info("Database disconnected")

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    @asynccontextmanager
    async def acquire(self):
        """Acquire connection from pool."""
        if self._pool is None:
            raise DBConnectionError("Database not connected. Call connect() first.")
        try:
            async with self._pool.acquire() as connection:
                yield connection
        except asyncpg.PostgresError as e:
            logger.error(f"Database connection error: {e}")
            raise DBConnectionError(f"Failed to acquire connection: {e}") from e

    @asynccontextmanager
    async def transaction(self):
        """Context manager for database transactions."""
        async with self.acquire() as conn:
            async with conn.transaction():
                yield conn

    # =========================================================================
    # QUERY METHODS - Updated for thesis-data-fabric schema
    # =========================================================================

    async def get_fundamentals(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Get fundamental data for ticker from the fundamentals view."""
        try:
            async with self.acquire() as conn:
                row = await conn.fetchrow(
                    """
                    SELECT ticker, name, sector, market_cap, pe_ratio, pb_ratio,
                           roe, profit_margin, revenue_growth, debt_to_equity,
                           current_ratio, dividend_yield, updated_at
                    FROM thesis_data.fundamentals
                    WHERE ticker = $1
                    """,
                    ticker,
                )
                if not row:
                    logger.debug(f"No fundamentals found for {ticker}")
                    return None
                return dict(row)
        except asyncpg.PostgresError as e:
            logger.error(f"Failed to fetch fundamentals for {ticker}: {e}")
            raise QueryError(f"Could not retrieve fundamentals for {ticker}") from e

    async def get_prices(self, ticker: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get recent price history from thesis_data.prices."""
        try:
            async with self.acquire() as conn:
                rows = await conn.fetch(
                    """
                    SELECT price_date AS date, open, high, low, close, volume
                    FROM thesis_data.prices
                    WHERE ticker = $1
                    ORDER BY price_date DESC
                    LIMIT $2
                    """,
                    ticker,
                    days,
                )
                return [dict(row) for row in rows]
        except asyncpg.PostgresError as e:
            logger.error(f"Failed to fetch prices for {ticker}: {e}")
            raise QueryError(f"Could not retrieve prices for {ticker}") from e

    async def get_news(self, ticker: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent news from thesis_data.stock_news."""
        try:
            async with self.acquire() as conn:
                rows = await conn.fetch(
                    """
                    SELECT 
                        published_at AS date,
                        headline,
                        summary,
                        sentiment_score,
                        sentiment_label AS sentiment,
                        source
                    FROM thesis_data.stock_news
                    WHERE ticker = $1
                    ORDER BY published_at DESC
                    LIMIT $2
                    """,
                    ticker,
                    limit,
                )
                return [dict(row) for row in rows]
        except asyncpg.PostgresError as e:
            logger.error(f"Failed to fetch news for {ticker}: {e}")
            raise QueryError(f"Could not retrieve news for {ticker}") from e

    async def get_filing(self, ticker: str, filing_type: str = "10-K") -> Optional[str]:
        """Get latest SEC filing content by concatenating chunks."""
        try:
            async with self.acquire() as conn:
                # Get the latest filing ID
                filing = await conn.fetchrow(
                    """
                    SELECT filing_id
                    FROM thesis_data.edgar_filings
                    WHERE ticker = $1 AND filing_type = $2
                    ORDER BY filing_date DESC
                    LIMIT 1
                    """,
                    ticker,
                    filing_type,
                )
                if not filing:
                    logger.debug(f"No {filing_type} filing found for {ticker}")
                    return None

                # Get all chunks and concatenate
                chunks = await conn.fetch(
                    """
                    SELECT chunk_text
                    FROM thesis_data.edgar_filing_chunks
                    WHERE filing_id = $1
                    ORDER BY chunk_index
                    """,
                    filing["filing_id"],
                )
                if not chunks:
                    return None
                return "".join(row["chunk_text"] for row in chunks)
        except asyncpg.PostgresError as e:
            logger.error(f"Failed to fetch filing for {ticker}: {e}")
            raise QueryError(f"Could not retrieve filing for {ticker}") from e

    async def get_filing_metadata(
        self, ticker: str, filing_type: str = "10-K"
    ) -> Optional[Dict[str, Any]]:
        """Get SEC filing metadata without content."""
        try:
            async with self.acquire() as conn:
                row = await conn.fetchrow(
                    """
                    SELECT filing_id, ticker, cik, company_name, filing_type,
                           filing_date, filing_url, is_xbrl, sections, financial_data
                    FROM thesis_data.edgar_filings
                    WHERE ticker = $1 AND filing_type = $2
                    ORDER BY filing_date DESC
                    LIMIT 1
                    """,
                    ticker,
                    filing_type,
                )
                return dict(row) if row else None
        except asyncpg.PostgresError as e:
            logger.error(f"Failed to fetch filing metadata for {ticker}: {e}")
            raise QueryError(f"Could not retrieve filing metadata for {ticker}") from e

    async def get_macro_indicators(self, indicator: str, days: int = 365) -> List[Dict[str, Any]]:
        """Get macro economic indicator data from thesis_data.macro_indicators.

        Args:
            indicator: One of 'cpi', 'unemployment', 'fed_funds', '10y_yield', 'gdp', 'inflation'
            days: Number of days of history
        """
        try:
            async with self.acquire() as conn:
                rows = await conn.fetch(
                    """
                    SELECT date, value, units, indicator_name, series_id
                    FROM thesis_data.macro_indicators
                    WHERE indicator_name = $1
                    ORDER BY date DESC
                    LIMIT $2
                    """,
                    indicator,
                    days,
                )
                return [dict(row) for row in rows]
        except asyncpg.PostgresError as e:
            logger.error(f"Failed to fetch macro indicator {indicator}: {e}")
            raise QueryError(f"Could not retrieve macro indicator {indicator}") from e

    async def list_macro_indicators(self) -> List[str]:
        """List all available macro indicator names."""
        try:
            async with self.acquire() as conn:
                rows = await conn.fetch(
                    """
                    SELECT DISTINCT indicator_name
                    FROM thesis_data.macro_indicators
                    ORDER BY indicator_name
                    """
                )
                return [row["indicator_name"] for row in rows]
        except asyncpg.PostgresError as e:
            logger.error(f"Failed to list macro indicators: {e}")
            raise QueryError("Could not retrieve macro indicator list") from e

    async def list_tickers(self) -> List[str]:
        """Get all available tickers from filings."""
        try:
            async with self.acquire() as conn:
                rows = await conn.fetch(
                    """
                    SELECT DISTINCT ticker
                    FROM thesis_data.edgar_filings
                    ORDER BY ticker
                    """
                )
                return [row["ticker"] for row in rows]
        except asyncpg.PostgresError as e:
            logger.error(f"Failed to list tickers: {e}")
            raise QueryError("Could not retrieve ticker list") from e

    # =========================================================================
    # INSERT METHODS - Updated for thesis-data-fabric schema
    # =========================================================================

    async def add_filing(self, data: Dict[str, Any]) -> bool:
        """Insert SEC filing with metadata and financial_data JSON."""
        try:
            async with self.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO thesis_data.edgar_filings (
                        filing_id, ticker, cik, company_name, filing_type,
                        filing_date, filing_url, is_xbrl, sections, financial_data
                    )
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                    ON CONFLICT (filing_id) DO UPDATE SET
                        company_name = EXCLUDED.company_name,
                        filing_url = EXCLUDED.filing_url,
                        sections = EXCLUDED.sections,
                        financial_data = EXCLUDED.financial_data
                    """,
                    data["filing_id"],
                    data["ticker"],
                    data.get("cik"),
                    data.get("company_name"),
                    data["filing_type"],
                    data["filing_date"],
                    data.get("filing_url"),
                    data.get("is_xbrl", False),
                    data.get("sections"),
                    data.get("financial_data"),
                )
                logger.debug(f"Added filing {data['filing_id']} for {data['ticker']}")
                return True
        except asyncpg.PostgresError as e:
            logger.error(f"Failed to add filing: {e}")
            raise QueryError("Could not insert filing") from e

    async def add_filing_chunk(self, filing_id: str, chunk_index: int, chunk_text: str) -> bool:
        """Insert a filing text chunk."""
        try:
            async with self.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO thesis_data.edgar_filing_chunks (filing_id, chunk_index, chunk_text)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (filing_id, chunk_index) DO UPDATE SET
                        chunk_text = EXCLUDED.chunk_text
                    """,
                    filing_id,
                    chunk_index,
                    chunk_text,
                )
                return True
        except asyncpg.PostgresError as e:
            logger.error(f"Failed to add filing chunk: {e}")
            raise QueryError("Could not insert filing chunk") from e

    async def add_price(self, ticker: str, price_data: Dict[str, Any]) -> bool:
        """Insert price data into thesis_data.prices."""
        try:
            async with self.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO thesis_data.prices 
                        (ticker, price_date, open, high, low, close, volume, source)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    ON CONFLICT (ticker, price_date) DO UPDATE SET
                        open = EXCLUDED.open,
                        high = EXCLUDED.high,
                        low = EXCLUDED.low,
                        close = EXCLUDED.close,
                        volume = EXCLUDED.volume,
                        source = EXCLUDED.source
                    """,
                    ticker,
                    price_data["date"],
                    price_data["open"],
                    price_data["high"],
                    price_data["low"],
                    price_data["close"],
                    price_data["volume"],
                    price_data.get("source", "mock"),
                )
                return True
        except asyncpg.PostgresError as e:
            logger.error(f"Failed to add price for {ticker}: {e}")
            raise QueryError("Could not insert price data") from e

    async def add_news(self, ticker: str, news_data: Dict[str, Any]) -> bool:
        """Insert news article into thesis_data.stock_news."""
        try:
            async with self.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO thesis_data.stock_news (
                        article_id, ticker, headline, summary, url, published_at,
                        source, sentiment_score, sentiment_label,
                        has_earnings_keyword, has_acquisition_keyword, has_regulatory_keyword
                    )
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                    ON CONFLICT (article_id) DO UPDATE SET
                        headline = EXCLUDED.headline,
                        sentiment_score = EXCLUDED.sentiment_score,
                        sentiment_label = EXCLUDED.sentiment_label
                    """,
                    news_data.get("article_id"),
                    ticker,
                    news_data["headline"],
                    news_data.get("summary"),
                    news_data.get("url"),
                    news_data["published_at"],
                    news_data.get("source"),
                    news_data.get("sentiment_score"),
                    news_data.get("sentiment_label"),
                    news_data.get("has_earnings_keyword", False),
                    news_data.get("has_acquisition_keyword", False),
                    news_data.get("has_regulatory_keyword", False),
                )
                return True
        except asyncpg.PostgresError as e:
            logger.error(f"Failed to add news for {ticker}: {e}")
            raise QueryError("Could not insert news") from e

    async def add_macro_indicator(self, data: Dict[str, Any]) -> bool:
        """Insert macro indicator data."""
        try:
            async with self.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO thesis_data.macro_indicators (
                        indicator_name, series_id, date, value, units, year, month, quarter
                    )
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    ON CONFLICT (indicator_name, date) DO UPDATE SET
                        value = EXCLUDED.value
                    """,
                    data["indicator_name"],
                    data.get("series_id"),
                    data["date"],
                    data["value"],
                    data.get("units"),
                    data.get("year"),
                    data.get("month"),
                    data.get("quarter"),
                )
                return True
        except asyncpg.PostgresError as e:
            logger.error(f"Failed to add macro indicator: {e}")
            raise QueryError("Could not insert macro indicator") from e

    # =========================================================================
    # UTILITY METHODS
    # =========================================================================

    async def health_check(self) -> bool:
        """Check database connection health."""
        try:
            async with self.acquire() as conn:
                await conn.fetchval("SELECT 1")
                return True
        except Exception:
            return False

    # =========================================================================
    # BACKWARD COMPATIBILITY - Deprecated methods
    # =========================================================================

    async def add_fundamental(self, data: Dict[str, Any]) -> bool:
        """DEPRECATED: Use add_filing() with financial_data JSON instead.

        This method creates a filing record with fundamentals stored in financial_data.
        """
        import json
        import uuid

        filing_id = (
            f"{data['ticker']}-10K-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8]}"
        )
        financial_data = {
            "sector": data.get("sector"),
            "market_cap": data.get("market_cap"),
            "pe_ratio": data.get("pe_ratio"),
            "pb_ratio": data.get("pb_ratio"),
            "roe": data.get("roe"),
            "profit_margin": data.get("profit_margin"),
            "revenue_growth": data.get("revenue_growth"),
            "debt_to_equity": data.get("debt_to_equity"),
            "current_ratio": data.get("current_ratio"),
            "dividend_yield": data.get("dividend_yield"),
        }

        filing_data = {
            "filing_id": filing_id,
            "ticker": data["ticker"],
            "company_name": data.get("name"),
            "filing_type": "10-K",
            "filing_date": datetime.now().date(),
            "financial_data": json.dumps(financial_data),
        }

        return await self.add_filing(filing_data)
