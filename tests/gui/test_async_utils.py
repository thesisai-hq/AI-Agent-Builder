"""Tests for GUI async utilities.

Tests async patterns, progress tracking, and parallel execution.
"""

import asyncio
import pytest
import time
from unittest.mock import Mock, patch, AsyncMock

# Add parent directory to path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gui.async_utils import (
    AsyncRunner,
    ProgressTracker,
    CancellableOperation,
    run_async,
    gather_with_errors,
    run_parallel_with_limit
)


# ============================================================================
# AsyncRunner Tests
# ============================================================================

class TestAsyncRunner:
    """Test AsyncRunner functionality."""
    
    @pytest.mark.asyncio
    async def test_run_simple_coroutine(self):
        """Test running simple async function."""
        runner = AsyncRunner()
        
        async def simple_task():
            await asyncio.sleep(0.01)
            return "success"
        
        result = runner.run(simple_task(), show_progress=False)
        assert result == "success"
    
    @pytest.mark.asyncio
    async def test_run_with_exception(self):
        """Test exception propagation."""
        runner = AsyncRunner()
        
        async def failing_task():
            await asyncio.sleep(0.01)
            raise ValueError("Test error")
        
        with pytest.raises(ValueError, match="Test error"):
            runner.run(failing_task(), show_progress=False)
    
    @pytest.mark.asyncio
    async def test_run_parallel(self):
        """Test parallel execution."""
        runner = AsyncRunner()
        
        async def task(n):
            await asyncio.sleep(0.01)
            return n * 2
        
        results = await runner.run_parallel(
            task(1),
            task(2),
            task(3)
        )
        
        assert results == [2, 4, 6]
    
    @pytest.mark.asyncio
    async def test_run_with_timeout_success(self):
        """Test timeout with fast operation."""
        runner = AsyncRunner()
        
        async def fast_task():
            await asyncio.sleep(0.01)
            return "done"
        
        result = await runner.run_with_timeout(fast_task(), timeout=1.0)
        assert result == "done"
    
    @pytest.mark.asyncio
    async def test_run_with_timeout_failure(self):
        """Test timeout with slow operation."""
        runner = AsyncRunner()
        
        async def slow_task():
            await asyncio.sleep(10.0)
            return "done"
        
        with pytest.raises(asyncio.TimeoutError):
            await runner.run_with_timeout(slow_task(), timeout=0.1)


# ============================================================================
# CancellableOperation Tests
# ============================================================================

class TestCancellableOperation:
    """Test cancellable operations."""
    
    @pytest.mark.asyncio
    async def test_run_without_cancel(self):
        """Test normal execution without cancellation."""
        operation = CancellableOperation()
        
        async def task():
            await asyncio.sleep(0.01)
            return "completed"
        
        result = await operation.run(task())
        assert result == "completed"
        assert not operation.is_cancelled()
    
    @pytest.mark.asyncio
    async def test_cancel_operation(self):
        """Test cancelling an operation."""
        operation = CancellableOperation()
        
        async def long_task():
            await asyncio.sleep(10.0)
            return "completed"
        
        # Start task
        task = asyncio.create_task(operation.run(long_task()))
        
        # Cancel after brief delay
        await asyncio.sleep(0.01)
        operation.cancel()
        
        # Wait for cancellation
        result = await task
        
        assert result is None
        assert operation.is_cancelled()
    
    @pytest.mark.asyncio
    async def test_cancel_callback(self):
        """Test cancel callback execution."""
        operation = CancellableOperation()
        callback_called = False
        
        def on_cancel():
            nonlocal callback_called
            callback_called = True
        
        async def long_task():
            await asyncio.sleep(10.0)
            return "completed"
        
        # Start and cancel
        task = asyncio.create_task(operation.run(long_task(), on_cancel=on_cancel))
        await asyncio.sleep(0.01)
        operation.cancel()
        await task
        
        assert callback_called


# ============================================================================
# Helper Function Tests
# ============================================================================

class TestHelperFunctions:
    """Test async helper functions."""
    
    @pytest.mark.asyncio
    async def test_gather_with_errors_all_success(self):
        """Test gathering with all successful operations."""
        async def task(n):
            await asyncio.sleep(0.01)
            return n * 2
        
        results, errors = await gather_with_errors(
            task(1),
            task(2),
            task(3)
        )
        
        assert results == [2, 4, 6]
        assert errors == []
    
    @pytest.mark.asyncio
    async def test_gather_with_errors_some_fail(self):
        """Test gathering with some failures."""
        async def success_task(n):
            await asyncio.sleep(0.01)
            return n * 2
        
        async def fail_task():
            await asyncio.sleep(0.01)
            raise ValueError("Failed")
        
        results, errors = await gather_with_errors(
            success_task(1),
            fail_task(),
            success_task(3)
        )
        
        assert results == [2, 6]
        assert len(errors) == 1
        assert errors[0]["index"] == 1
        assert "Failed" in errors[0]["error"]
    
    @pytest.mark.asyncio
    async def test_run_parallel_with_limit(self):
        """Test parallel execution with concurrency limit."""
        executed = []
        
        async def task(item):
            executed.append(item)
            await asyncio.sleep(0.05)
            return item * 2
        
        results = await run_parallel_with_limit(
            items=[1, 2, 3, 4, 5],
            async_func=task,
            max_concurrent=2,
            description="Testing"
        )
        
        # All items processed
        assert len(results) == 5
        assert all(r == i * 2 for i, r in enumerate(results, 1))
        
        # All items executed
        assert sorted(executed) == [1, 2, 3, 4, 5]


# ============================================================================
# Integration Tests
# ============================================================================

class TestAsyncIntegration:
    """Integration tests for async patterns."""
    
    @pytest.mark.asyncio
    async def test_realistic_agent_workflow(self):
        """Test realistic agent testing workflow."""
        runner = AsyncRunner()
        
        # Simulate agent analysis
        async def simulate_analysis(ticker, data):
            # Simulate LLM call delay
            await asyncio.sleep(0.1)
            
            # Simple logic
            if data["pe_ratio"] < 15:
                return {
                    "direction": "bullish",
                    "confidence": 0.8,
                    "reasoning": "Undervalued"
                }
            else:
                return {
                    "direction": "neutral",
                    "confidence": 0.6,
                    "reasoning": "Fair value"
                }
        
        data = {"pe_ratio": 12.0}
        
        # Run with timeout
        result = await runner.run_with_timeout(
            simulate_analysis("AAPL", data),
            timeout=1.0
        )
        
        assert result["direction"] == "bullish"
        assert result["confidence"] == 0.8
    
    @pytest.mark.asyncio
    async def test_batch_testing_workflow(self):
        """Test batch testing multiple agents."""
        async def analyze_agent(agent_ticker_pair):
            agent_name, ticker = agent_ticker_pair
            await asyncio.sleep(0.05)
            return {
                "agent": agent_name,
                "ticker": ticker,
                "signal": "bullish"
            }
        
        pairs = [
            ("Agent1", "AAPL"),
            ("Agent1", "MSFT"),
            ("Agent2", "AAPL"),
            ("Agent2", "MSFT")
        ]
        
        # Run with concurrency limit
        results = await run_parallel_with_limit(
            pairs,
            analyze_agent,
            max_concurrent=2,
            description="Batch test"
        )
        
        assert len(results) == 4
        assert all(r["signal"] == "bullish" for r in results)


# ============================================================================
# Performance Tests
# ============================================================================

class TestPerformance:
    """Test performance improvements from async."""
    
    @pytest.mark.asyncio
    async def test_parallel_speedup(self):
        """Verify parallel execution is faster than sequential."""
        async def slow_task(n):
            await asyncio.sleep(0.1)
            return n
        
        # Sequential
        start = time.time()
        sequential_results = []
        for i in range(5):
            result = await slow_task(i)
            sequential_results.append(result)
        sequential_time = time.time() - start
        
        # Parallel
        start = time.time()
        parallel_results = await asyncio.gather(*[slow_task(i) for i in range(5)])
        parallel_time = time.time() - start
        
        # Parallel should be ~5x faster
        assert parallel_time < sequential_time / 3  # At least 3x faster
        assert sequential_results == list(parallel_results)


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])
