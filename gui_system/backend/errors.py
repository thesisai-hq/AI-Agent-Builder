"""Standardized error responses for consistent API behavior."""

from fastapi import HTTPException
from typing import Optional, Dict, Any


class APIError(HTTPException):
    """Base API error with structured response."""
    
    def __init__(
        self, 
        status_code: int, 
        message: str, 
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "message": message,
                "details": details or {},
                "error_type": self.__class__.__name__
            }
        )


class AgentNotFoundError(APIError):
    """Agent not found."""
    def __init__(self, agent_id: str):
        super().__init__(404, "Agent not found", {"agent_id": agent_id})


class TemplateNotFoundError(APIError):
    """Template not found."""
    def __init__(self, template_id: str):
        super().__init__(404, "Template not found", {"template_id": template_id})


class DataFetchError(APIError):
    """Failed to fetch stock data."""
    def __init__(self, ticker: str, reason: str):
        super().__init__(500, "Failed to fetch stock data", {
            "ticker": ticker,
            "reason": reason
        })


class InvalidTickerError(APIError):
    """Invalid ticker symbol."""
    def __init__(self, ticker: str):
        super().__init__(400, "Invalid ticker symbol", {"ticker": ticker})


class AnalysisError(APIError):
    """Analysis execution failed."""
    def __init__(self, reason: str, details: Optional[Dict] = None):
        super().__init__(500, "Analysis failed", {
            "reason": reason,
            **(details or {})
        })


class ValidationError(APIError):
    """Validation error."""
    def __init__(self, field: str, reason: str):
        super().__init__(400, "Validation error", {
            "field": field,
            "reason": reason
        })
