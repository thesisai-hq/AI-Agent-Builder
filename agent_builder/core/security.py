"""Input validation and security"""

import re


class ValidationError(ValueError):
    pass


class Validator:
    ALLOWED_TABLES = frozenset([
        "analyses", "mock_fundamentals", "mock_prices", 
        "mock_news", "mock_insider_trades", "mock_analyst_ratings",
        "mock_sec_filings", "mock_macro_indicators", "mock_options",
    ])
    
    @staticmethod
    def ticker(value: str) -> str:
        value = value.upper().strip()
        if not re.match(r"^[A-Z]{1,5}$", value):
            raise ValidationError(f"Invalid ticker: {value}")
        return value
    
    @staticmethod
    def agent_id(value: str) -> str:
        value = value.lower().strip()
        if not re.match(r"^[a-z0-9_]{1,50}$", value):
            raise ValidationError(f"Invalid agent ID: {value}")
        return value
