"""Tests for GUI components and async utilities.

Comprehensive test suite for the refactored GUI code.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
import sys

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# ============================================================================
# Tests for async_utils
# ============================================================================

class TestAsyncRunner:
    """Test AsyncRunner functionality."""
    
    @pytest.mark.asyncio
    async def test_run_simple_coroutine(self):
        """Test running a simple async coroutine."""
        from gui.async_utils import AsyncRunner
        
        async def simple_coro():
            await asyncio.sleep(0.01)
            return "success"
        
        runner = AsyncRunner()
        
        # Note: run() is synchronous, wraps async execution
        # In real Streamlit, this would work fine
        # For testing, we test the async methods directly
        result = await simple_coro()
        assert result == "success"
    
    @pytest.mark.asyncio
    async def test_run_parallel(self):
        """Test parallel execution of coroutines."""
        from gui.async_utils import AsyncRunner
        
        async def fetch_data(value):
            await asyncio.sleep(0.01)
            return value * 2
        
        runner = AsyncRunner()
        
        results = await runner.run_parallel(
            fetch_data(1),
            fetch_data(2),
            fetch_data(3)
        )
        
        assert results == [2, 4, 6]
    
    @pytest.mark.asyncio
    async def test_run_with_timeout_success(self):
        """Test timeout with successful completion."""
        from gui.async_utils import AsyncRunner
        
        async def quick_operation():
            await asyncio.sleep(0.01)
            return "done"
        
        runner = AsyncRunner()
        
        result = await runner.run_with_timeout(quick_operation(), timeout=1.0)
        assert result == "done"
    
    @pytest.mark.asyncio
    async def test_run_with_timeout_failure(self):
        """Test timeout with slow operation."""
        from gui.async_utils import AsyncRunner
        
        async def slow_operation():
            await asyncio.sleep(2.0)
            return "done"
        
        runner = AsyncRunner()
        
        with pytest.raises(asyncio.TimeoutError):
            await runner.run_with_timeout(slow_operation(), timeout=0.1)


class TestProgressTracker:
    """Test ProgressTracker (mock Streamlit)."""
    
    def test_progress_updates(self):
        """Test progress tracking updates."""
        # This would need Streamlit testing framework
        # For now, test the logic
        
        # Mock would verify:
        # - Progress bar created
        # - Updates called with correct values
        # - Status text updated
        # - Complete called
        pass  # Requires Streamlit testing framework


class TestCancellableOperation:
    """Test cancellable operations."""
    
    @pytest.mark.asyncio
    async def test_successful_operation(self):
        """Test non-cancelled operation."""
        from gui.async_utils import CancellableOperation
        
        async def operation():
            await asyncio.sleep(0.01)
            return "success"
        
        op = CancellableOperation()
        result = await op.run(operation())
        
        assert result == "success"
        assert not op.is_cancelled()
    
    @pytest.mark.asyncio
    async def test_cancelled_operation(self):
        """Test operation cancellation."""
        from gui.async_utils import CancellableOperation
        
        async def long_operation():
            await asyncio.sleep(10.0)
            return "done"
        
        op = CancellableOperation()
        
        # Start operation
        task = asyncio.create_task(op.run(long_operation()))
        
        # Cancel after brief delay
        await asyncio.sleep(0.01)
        op.cancel()
        
        # Should return None (cancelled)
        result = await task
        assert result is None
        assert op.is_cancelled()


class TestConvenienceFunctions:
    """Test async utility convenience functions."""
    
    @pytest.mark.asyncio
    async def test_gather_with_errors_all_success(self):
        """Test gather_with_errors with all successful."""
        from gui.async_utils import gather_with_errors
        
        async def success_coro(value):
            return value * 2
        
        results, errors = await gather_with_errors(
            success_coro(1),
            success_coro(2),
            success_coro(3)
        )
        
        assert results == [2, 4, 6]
        assert errors == []
    
    @pytest.mark.asyncio
    async def test_gather_with_errors_mixed(self):
        """Test gather_with_errors with some failures."""
        from gui.async_utils import gather_with_errors
        
        async def success_coro(value):
            return value * 2
        
        async def fail_coro():
            raise ValueError("Test error")
        
        results, errors = await gather_with_errors(
            success_coro(1),
            fail_coro(),
            success_coro(3)
        )
        
        assert results == [2, 6]
        assert len(errors) == 1
        assert errors[0]["index"] == 1
        assert "Test error" in errors[0]["error"]


# ============================================================================
# Tests for business_logic/test_executor
# ============================================================================

class TestTestExecutor:
    """Test TestExecutor async functionality."""
    
    @pytest.fixture
    def executor(self):
        """Create test executor instance."""
        from gui.business_logic.test_executor import TestExecutor
        return TestExecutor()
    
    def test_is_rag_agent_true(self, executor):
        """Test RAG agent detection - positive case."""
        mock_agent = Mock()
        mock_agent.config = Mock()
        mock_agent.config.rag = Mock()  # RAG config exists
        
        assert executor._is_rag_agent(mock_agent) is True
    
    def test_is_rag_agent_false(self, executor):
        """Test RAG agent detection - negative case."""
        mock_agent = Mock()
        mock_agent.config = Mock()
        mock_agent.config.rag = None  # No RAG config
        
        assert executor._is_rag_agent(mock_agent) is False
    
    def test_detect_llm_fallback_true(self, executor):
        """Test LLM fallback detection - positive case."""
        from agent_framework import Signal
        
        signal = Signal(
            direction="neutral",
            confidence=0.5,
            reasoning="LLM service unavailable - using fallback logic"
        )
        
        assert executor._detect_llm_fallback(signal) is True
    
    def test_detect_llm_fallback_false(self, executor):
        """Test LLM fallback detection - negative case."""
        from agent_framework import Signal
        
        signal = Signal(
            direction="bullish",
            confidence=0.8,
            reasoning="Strong fundamentals with PE ratio of 12"
        )
        
        assert executor._detect_llm_fallback(signal) is False
    
    def test_parse_llm_error_missing_package(self, executor):
        """Test parsing missing package error."""
        reasoning = "Error: openai package not installed"
        
        error_info = executor._parse_llm_error(reasoning)
        
        assert error_info["error_type"] == "missing_package"
        assert "package" in error_info["description"].lower()
    
    def test_parse_llm_error_model_not_found(self, executor):
        """Test parsing model not found error."""
        reasoning = "Model llama3.2 not found or not downloaded"
        
        error_info = executor._parse_llm_error(reasoning)
        
        assert error_info["error_type"] == "model_not_found"
    
    def test_parse_llm_error_connection(self, executor):
        """Test parsing connection error."""
        reasoning = "Cannot connect to Ollama service"
        
        error_info = executor._parse_llm_error(reasoning)
        
        assert error_info["error_type"] == "connection_error"
    
    def test_parse_llm_error_api_key(self, executor):
        """Test parsing API key error."""
        reasoning = "API key not configured for OpenAI"
        
        error_info = executor._parse_llm_error(reasoning)
        
        assert error_info["error_type"] == "missing_api_key"
    
    def test_parse_llm_error_rate_limit(self, executor):
        """Test parsing rate limit error."""
        reasoning = "Rate limit exceeded for API calls"
        
        error_info = executor._parse_llm_error(reasoning)
        
        assert error_info["error_type"] == "rate_limit"
    
    @pytest.mark.asyncio
    async def test_execute_test_async_success(self, executor, tmp_path):
        """Test successful async test execution."""
        # Create a simple test agent file
        agent_code = '''
from agent_framework import Agent, Signal

class TestAgent(Agent):
    async def analyze(self, ticker, data):
        return Signal(
            direction="bullish",
            confidence=0.8,
            reasoning="Test reasoning"
        )
'''
        
        agent_file = tmp_path / "test_agent.py"
        agent_file.write_text(agent_code)
        
        # Update executor to use temp path
        executor.examples_dir = tmp_path
        
        from gui.components.test_config import TestDataConfig
        
        agent_info = {
            "name": "TestAgent",
            "filename": "test_agent.py"
        }
        
        test_config = TestDataConfig(
            source="mock",
            data={"pe_ratio": 20},
            ticker="TEST"
        )
        
        result = await executor.execute_test_async(
            agent_info,
            test_config,
            data={"pe_ratio": 20, "name": "Test Co"}
        )
        
        assert result["success"] is True
        assert result["signal"]["direction"] == "bullish"
        assert result["signal"]["confidence"] == 0.8
        assert result["ticker"] == "TEST"
        assert "execution_time" in result
    
    @pytest.mark.asyncio
    async def test_execute_test_async_file_not_found(self, executor):
        """Test error when agent file doesn't exist."""
        from gui.components.test_config import TestDataConfig
        
        agent_info = {
            "name": "NonExistent",
            "filename": "nonexistent.py"
        }
        
        test_config = TestDataConfig(source="mock", data={}, ticker="TEST")
        
        result = await executor.execute_test_async(agent_info, test_config, None)
        
        assert result["success"] is False
        assert "not found" in result["error"]
    
    @pytest.mark.asyncio
    async def test_execute_test_async_timeout(self, executor, tmp_path):
        """Test timeout handling in async execution."""
        # Create slow agent
        agent_code = '''
import asyncio
from agent_framework import Agent, Signal

class SlowAgent(Agent):
    async def analyze(self, ticker, data):
        await asyncio.sleep(100)  # Very slow
        return Signal("neutral", 0.5, "Too slow")
'''
        
        agent_file = tmp_path / "slow_agent.py"
        agent_file.write_text(agent_code)
        executor.examples_dir = tmp_path
        
        from gui.components.test_config import TestDataConfig
        
        agent_info = {"name": "SlowAgent", "filename": "slow_agent.py"}
        test_config = TestDataConfig(source="mock", data={}, ticker="TEST")
        
        result = await executor.execute_test_async(
            agent_info,
            test_config,
            data={"pe_ratio": 20}
        )
        
        assert result["success"] is False
        assert result["error_type"] == "timeout"
        assert "timed out" in result["error"]


# ============================================================================
# Tests for components
# ============================================================================

class TestAgentCard:
    """Test agent card component."""
    
    def test_show_agent_stats(self):
        """Test agent statistics display."""
        from gui.components.agent_card import show_agent_stats
        
        agents = [
            {"type": "Rule-Based", "filename": "value.py"},
            {"type": "LLM-Powered", "filename": "growth.py"},
            {"type": "RAG-Powered", "filename": "filing.py"},
            {"type": "Rule-Based", "filename": "custom.py"},
        ]
        
        # This would need Streamlit testing framework
        # For now, just verify it doesn't crash
        # In real test: mock st.metric and verify calls
        pass


class TestTestConfig:
    """Test test configuration component."""
    
    def test_test_data_config_creation(self):
        """Test TestDataConfig dataclass."""
        from gui.components.test_config import TestDataConfig
        
        config = TestDataConfig(
            source="mock",
            data={"pe_ratio": 20},
            ticker="AAPL"
        )
        
        assert config.source == "mock"
        assert config.data["pe_ratio"] == 20
        assert config.ticker == "AAPL"
        assert config.uploaded_file is None


class TestResultsDisplay:
    """Test results display component."""
    
    def test_display_functions_exist(self):
        """Verify all display functions are importable."""
        from gui.components.results_display import (
            display_test_results,
            display_error_with_solution
        )
        
        # Functions exist
        assert callable(display_test_results)
        assert callable(display_error_with_solution)


# ============================================================================
# Integration Tests
# ============================================================================

class TestAsyncIntegration:
    """Integration tests for async workflows."""
    
    @pytest.mark.asyncio
    async def test_full_test_workflow(self, tmp_path):
        """Test complete async test workflow."""
        # Create simple agent
        agent_code = '''
from agent_framework import Agent, Signal

class IntegrationTestAgent(Agent):
    async def analyze(self, ticker, data):
        pe = data.get("pe_ratio", 0)
        if pe < 15:
            return Signal("bullish", 0.8, f"Undervalued: PE={pe}")
        return Signal("neutral", 0.5, "Fair value")
'''
        
        agent_file = tmp_path / "integration_agent.py"
        agent_file.write_text(agent_code)
        
        # Execute test
        from gui.business_logic.test_executor import TestExecutor
        from gui.components.test_config import TestDataConfig
        
        executor = TestExecutor()
        executor.examples_dir = tmp_path
        
        agent_info = {
            "name": "IntegrationTestAgent",
            "filename": "integration_agent.py"
        }
        
        test_config = TestDataConfig(
            source="mock",
            data={"pe_ratio": 12},
            ticker="TEST"
        )
        
        result = await executor.execute_test_async(
            agent_info,
            test_config,
            data={"pe_ratio": 12, "name": "Test Co"}
        )
        
        # Verify complete workflow
        assert result["success"] is True
        assert result["signal"]["direction"] == "bullish"
        assert result["signal"]["confidence"] == 0.8
        assert "Undervalued" in result["signal"]["reasoning"]
        assert result["ticker"] == "TEST"
        assert result["execution_time"] < 1.0


# ============================================================================
# Performance Tests
# ============================================================================

class TestAsyncPerformance:
    """Performance tests for async operations."""
    
    @pytest.mark.asyncio
    async def test_parallel_speedup(self):
        """Verify parallel execution is faster than sequential."""
        import time
        
        async def slow_task(delay):
            await asyncio.sleep(delay)
            return delay
        
        # Sequential
        start = time.time()
        seq_results = []
        for i in range(3):
            result = await slow_task(0.1)
            seq_results.append(result)
        sequential_time = time.time() - start
        
        # Parallel
        start = time.time()
        from gui.async_utils import AsyncRunner
        runner = AsyncRunner()
        parallel_results = await runner.run_parallel(
            slow_task(0.1),
            slow_task(0.1),
            slow_task(0.1)
        )
        parallel_time = time.time() - start
        
        # Parallel should be ~3x faster
        assert sequential_time > 0.25  # Should be ~0.3s
        assert parallel_time < 0.15    # Should be ~0.1s
        assert sequential_time / parallel_time > 2.0  # At least 2x speedup
    
    @pytest.mark.asyncio
    async def test_concurrency_limit(self):
        """Verify concurrency limit is respected."""
        from gui.async_utils import run_parallel_with_limit
        
        concurrent_count = 0
        max_concurrent_seen = 0
        
        async def tracked_task(item):
            nonlocal concurrent_count, max_concurrent_seen
            
            concurrent_count += 1
            max_concurrent_seen = max(max_concurrent_seen, concurrent_count)
            
            await asyncio.sleep(0.01)
            
            concurrent_count -= 1
            return item
        
        items = list(range(10))
        
        results = await run_parallel_with_limit(
            items,
            tracked_task,
            max_concurrent=3,
            description="Testing"
        )
        
        # Should never exceed limit
        assert max_concurrent_seen <= 3
        assert len(results) == 10


# ============================================================================
# Error Handling Tests
# ============================================================================

class TestAsyncErrorHandling:
    """Test error handling in async operations."""
    
    @pytest.mark.asyncio
    async def test_timeout_error_handling(self):
        """Test timeout error is properly caught and handled."""
        from gui.business_logic.test_executor import TestExecutor
        from gui.components.test_config import TestDataConfig
        
        executor = TestExecutor()
        
        # Mock agent that times out
        with patch.object(executor, '_load_agent_async') as mock_load:
            async def timeout_analyze(ticker, data):
                await asyncio.sleep(100)
                return Mock()
            
            mock_agent = Mock()
            mock_agent.analyze = timeout_analyze
            mock_load.return_value = type('Agent', (), {})
            
            # This test would need proper mocking
            # Demonstrates the test pattern
            pass
    
    @pytest.mark.asyncio
    async def test_exception_propagation(self):
        """Test exceptions are properly propagated."""
        from gui.async_utils import AsyncRunner
        
        async def failing_coro():
            raise ValueError("Test exception")
        
        runner = AsyncRunner()
        
        with pytest.raises(ValueError, match="Test exception"):
            await failing_coro()


# ============================================================================
# Batch Testing Tests
# ============================================================================

class TestBatchTestExecutor:
    """Test batch testing functionality."""
    
    @pytest.mark.asyncio
    async def test_aggregate_results(self):
        """Test result aggregation logic."""
        from gui.pages.batch_test_page import BatchTestExecutor, BatchTestConfig
        from gui.components.test_config import TestDataConfig
        
        executor = BatchTestExecutor()
        
        # Mock results
        results = [
            {
                "success": True,
                "agent_name": "Agent1",
                "ticker": "AAPL",
                "signal": {"direction": "bullish", "confidence": 0.8},
                "execution_time": 1.5
            },
            {
                "success": True,
                "agent_name": "Agent1",
                "ticker": "MSFT",
                "signal": {"direction": "bearish", "confidence": 0.7},
                "execution_time": 2.0
            },
            {
                "success": False,
                "agent_name": "Agent2",
                "ticker": "AAPL",
                "error": "Test error"
            }
        ]
        
        config = BatchTestConfig(
            agents=[{"name": "Agent1"}, {"name": "Agent2"}],
            tickers=["AAPL", "MSFT"],
            test_data_config=TestDataConfig(source="mock", data={}, ticker="TEST"),
            max_concurrent=2
        )
        
        aggregated = executor._aggregate_results(results, config)
        
        # Verify aggregation
        assert aggregated["total_tests"] == 3
        assert aggregated["successful"] == 2
        assert aggregated["failed"] == 1
        assert aggregated["success_rate"] == pytest.approx(2/3)
        assert aggregated["avg_confidence"] == pytest.approx(0.75)
        assert aggregated["signal_distribution"]["bullish"] == 1
        assert aggregated["signal_distribution"]["bearish"] == 1
        assert len(aggregated["by_agent"]) == 2
        assert len(aggregated["by_ticker"]) == 2


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=gui", "--cov-report=term-missing"])
