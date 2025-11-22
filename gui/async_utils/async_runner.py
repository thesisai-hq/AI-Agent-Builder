"""Async coroutine runner for Streamlit context.

Handles event loop management and provides progress indicators.
"""

import asyncio
from typing import Any, Coroutine, TypeVar

import streamlit as st

T = TypeVar('T')


class AsyncRunner:
    """Run async operations in Streamlit with proper event loop management."""
    
    def run(
        self, 
        coro: Coroutine[Any, Any, T],
        description: str = "Processing...",
        show_progress: bool = True
    ) -> T:
        """Run async coroutine in Streamlit context.
        
        Args:
            coro: Async coroutine to run
            description: Progress message to display
            show_progress: Whether to show spinner
            
        Returns:
            Result from coroutine
            
        Example:
            runner = AsyncRunner()
            result = runner.run(
                agent.analyze(ticker, data),
                description="Analyzing agent..."
            )
        """
        if show_progress:
            with st.spinner(description):
                return self._run_async(coro)
        else:
            return self._run_async(coro)
    
    def _run_async(self, coro: Coroutine[Any, Any, T]) -> T:
        """Internal method to run async coroutine.
        
        Handles event loop creation and management for Streamlit context.
        """
        try:
            # Get or create event loop
            try:
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Run coroutine
            return loop.run_until_complete(coro)
            
        except Exception:
            # Ensure clean error propagation
            raise


def run_async(coro: Coroutine[Any, Any, T], spinner_text: str = "Processing...") -> T:
    """Quick helper to run async coroutine in Streamlit.
    
    Convenience function for one-off async operations.
    
    Args:
        coro: Coroutine to run
        spinner_text: Spinner message (empty string to disable spinner)
        
    Returns:
        Result from coroutine
        
    Example:
        result = run_async(
            agent.analyze(ticker, data),
            spinner_text="Analyzing..."
        )
    """
    runner = AsyncRunner()
    return runner.run(coro, description=spinner_text, show_progress=bool(spinner_text))
