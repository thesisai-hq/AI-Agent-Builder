"""Async utilities for GUI operations.

Simplified async helpers focused on single-agent testing with progress tracking.
Removed batch testing complexity - keeping only essential responsive UI features.
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


class ProgressTracker:
    """Track progress of operations with Streamlit UI updates.
    
    Simple progress indicator for single operations with manual updates.
    """
    
    def __init__(self, total: int, description: str = "Processing"):
        """Initialize progress tracker.
        
        Args:
            total: Total number of items to process
            description: Progress bar description
        """
        self.total = total
        self.current = 0
        self.description = description
        self._progress_bar = st.progress(0.0)
        self._status_text = st.empty()
        self._update_display()
    
    def update(self, increment: int = 1, status: str = ""):
        """Update progress.
        
        Args:
            increment: Number of items completed
            status: Optional status message
        """
        self.current = min(self.current + increment, self.total)
        self._update_display(status)
    
    def _update_display(self, status: str = ""):
        """Update progress bar and status text."""
        progress = self.current / self.total if self.total > 0 else 0
        self._progress_bar.progress(progress)
        
        if status:
            self._status_text.text(f"{self.description}: {status}")
        else:
            self._status_text.text(
                f"{self.description}: {self.current}/{self.total} ({progress:.0%})"
            )
    
    def complete(self, message: str = "Complete!"):
        """Mark operation as complete.
        
        Args:
            message: Completion message
        """
        self._progress_bar.progress(1.0)
        self._status_text.text(message)
    
    def clear(self):
        """Clear progress indicators."""
        self._progress_bar.empty()
        self._status_text.empty()
