"""Utility functions and decorators"""

from functools import wraps
from contextlib import contextmanager
import logging
import uuid

logger = logging.getLogger(__name__)


def safe_execute(default_return=None, log_error=True):
    """
    Decorator for safe execution with error handling

    Usage:
        @safe_execute(default_return=0)
        def risky_operation():
            return 1 / 0  # Returns 0 instead of crashing
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_error:
                    logger.error(f"Error in {func.__name__}: {e}")
                return default_return

        return wrapper

    return decorator


def generate_id() -> str:
    """Generate unique ID"""
    return str(uuid.uuid4())


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safe division (handles zero division)"""
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ZeroDivisionError):
        return default
