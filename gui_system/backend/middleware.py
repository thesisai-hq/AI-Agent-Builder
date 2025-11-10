"""Request validation middleware for API.

Provides centralized validation for common request patterns.
"""

import re
from fastapi import Request, HTTPException
from typing import Callable


# Validation patterns
TICKER_PATTERN = re.compile(r'^[A-Z]{1,5}$')
UUID_PATTERN = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)


async def validate_ticker_middleware(request: Request, call_next: Callable):
    """Validate ticker format in path parameters.
    
    Checks if ticker matches standard format (1-5 uppercase letters).
    
    Args:
        request: FastAPI request
        call_next: Next middleware/handler
        
    Returns:
        Response from next handler
        
    Raises:
        HTTPException: If ticker format is invalid
    """
    # Check if ticker in path
    if 'ticker' in request.path_params:
        ticker = request.path_params['ticker']
        
        if not TICKER_PATTERN.match(ticker.upper()):
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Invalid ticker format",
                    "details": {
                        "ticker": ticker,
                        "expected_format": "1-5 uppercase letters (e.g., AAPL, MSFT)"
                    }
                }
            )
    
    return await call_next(request)


async def validate_uuid_middleware(request: Request, call_next: Callable):
    """Validate UUID format in path parameters.
    
    Checks agent_id, template_id, etc. for valid UUID format.
    
    Args:
        request: FastAPI request
        call_next: Next middleware/handler
        
    Returns:
        Response from next handler
        
    Raises:
        HTTPException: If UUID format is invalid
    """
    # Check for UUID fields in path
    uuid_fields = ['agent_id', 'template_id', 'id']
    
    for field in uuid_fields:
        if field in request.path_params:
            value = request.path_params[field]
            
            if not UUID_PATTERN.match(value):
                raise HTTPException(
                    status_code=400,
                    detail={
                        "message": f"Invalid {field} format",
                        "details": {
                            field: value,
                            "expected_format": "UUID (e.g., 550e8400-e29b-41d4-a716-446655440000)"
                        }
                    }
                )
    
    return await call_next(request)


async def rate_limit_middleware(request: Request, call_next: Callable):
    """Basic rate limiting for expensive operations.
    
    Note: This is a simple in-memory implementation.
    For production, use Redis or similar.
    
    Args:
        request: FastAPI request
        call_next: Next middleware/handler
        
    Returns:
        Response from next handler
    """
    # TODO: Implement with Redis for production
    # For now, just pass through
    return await call_next(request)


# Validation helpers
def validate_ticker_format(ticker: str) -> bool:
    """Check if ticker matches valid format.
    
    Args:
        ticker: Ticker symbol
        
    Returns:
        True if valid format
    """
    return bool(TICKER_PATTERN.match(ticker.upper()))


def validate_uuid_format(uuid_str: str) -> bool:
    """Check if string is valid UUID.
    
    Args:
        uuid_str: UUID string
        
    Returns:
        True if valid UUID format
    """
    return bool(UUID_PATTERN.match(uuid_str))
