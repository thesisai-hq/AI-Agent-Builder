"""
Security utilities - UPDATED for complete database
"""

import re
from typing import Set

# Table whitelist - PREVENTS SQL INJECTION
# UPDATED with all 13 mock tables
ALLOWED_TABLES: Set[str] = frozenset(
    [
        # Analysis storage
        "analyses",
        # Fundamental data
        "mock_fundamentals",
        "mock_balance_sheet",
        "mock_cash_flow",
        "mock_earnings",
        "mock_sec_filings",
        # Technical data
        "mock_prices",
        "mock_technical_indicators",
        # Sentiment data
        "mock_news",
        "mock_analyst_ratings",
        "mock_insider_trades",
        # Risk data
        "mock_risk_metrics",
        "mock_options_data",
        # Macro data
        "mock_macro_indicators",
    ]
)


def validate_table_name(table: str) -> str:
    """
    Validate table name to prevent SQL injection

    CRITICAL: Prevents malicious table names from executing arbitrary SQL

    Args:
        table: Table name to validate

    Returns:
        Validated table name

    Raises:
        ValueError: If table name is not in whitelist

    Example:
        >>> validate_table_name('mock_fundamentals')  # OK
        'mock_fundamentals'
        >>> validate_table_name('users; DROP TABLE analyses--')  # BLOCKED
        ValueError: Invalid table name
    """
    if table not in ALLOWED_TABLES:
        raise ValueError(f"Invalid table name: {table}")
    return table


def sanitize_ticker(ticker: str) -> str:
    """
    Sanitize stock ticker symbol

    Only allows: A-Z letters, uppercase, 1-5 characters

    Args:
        ticker: Stock ticker to sanitize

    Returns:
        Sanitized ticker

    Raises:
        ValueError: If ticker format is invalid

    Example:
        >>> sanitize_ticker('AAPL')
        'AAPL'
        >>> sanitize_ticker('aapl')
        'AAPL'
        >>> sanitize_ticker('AAPL; DROP TABLE--')  # BLOCKED
        ValueError: Invalid ticker
    """
    ticker = ticker.upper().strip()

    # Only allow A-Z, 1-5 characters
    if not re.match(r"^[A-Z]{1,5}$", ticker):
        raise ValueError(f"Invalid ticker format: {ticker}")

    return ticker


def validate_agent_id(agent_id: str) -> str:
    """
    Validate agent ID format

    Only allows: a-z, 0-9, underscore, 1-50 characters

    Args:
        agent_id: Agent ID to validate

    Returns:
        Validated agent ID

    Raises:
        ValueError: If agent ID format is invalid
    """
    if not re.match(r"^[a-z0-9_]{1,50}$", agent_id):
        raise ValueError(f"Invalid agent ID format: {agent_id}")

    return agent_id
