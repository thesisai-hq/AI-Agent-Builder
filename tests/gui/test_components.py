"""Tests for GUI components.

Tests reusable UI components for correctness and edge cases.
Uses mocks to avoid requiring Streamlit runtime.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# ============================================================================
# Test Config Component Tests
# ============================================================================

class TestTestConfig:
    """Test test configuration component."""
    
    def test_prepare_mock_data(self):
        """Test mock data preparation."""
        from gui.components.test_config import TestDataConfig
        
        config = TestDataConfig(
            source="mock",
            data={"pe_ratio": 20.0, "roe": 15.0},
            ticker="TEST"
        )
        
        # Verify structure
        assert config.source == "mock"
        assert config.data["pe_ratio"] == 20.0
        assert config.ticker == "TEST"
    
    def test_prepare_database_data(self):
        """Test database data preparation."""
        from gui.components.test_config import TestDataConfig
        
        config = TestDataConfig(
            source="database",
            ticker="AAPL"
        )
        
        assert config.source == "database"
        assert config.data is None  # Will fetch from DB
        assert config.ticker == "AAPL"
    
    def test_prepare_pdf_data(self):
        """Test PDF data preparation."""
        from gui.components.test_config import TestDataConfig
        
        mock_file = Mock()
        mock_file.name = "test.pdf"
        
        config = TestDataConfig(
            source="pdf",
            uploaded_file=mock_file,
            ticker="AAPL"
        )
        
        assert config.source == "pdf"
        assert config.uploaded_file == mock_file
        assert config.data is None


# ============================================================================
# Results Display Tests
# ============================================================================

class TestResultsDisplay:
    """Test results display component."""
    
    @patch('streamlit.success')
    @patch('streamlit.metric')
    @patch('streamlit.info')
    @patch('streamlit.columns')
    def test_display_successful_results(self, mock_cols, mock_info, mock_metric, mock_success):
        """Test displaying successful test results."""
        from gui.components.results_display import display_test_results
        
        # Mock columns
        mock_col1 = Mock()
        mock_col2 = Mock()
        mock_col3 = Mock()
        mock_cols.return_value = [mock_col1, mock_col2, mock_col3]
        
        result = {
            "success": True,
            "signal": {
                "direction": "bullish",
                "confidence": 0.8,
                "reasoning": "Strong fundamentals"
            },
            "execution_time": 1.5
        }
        
        # Should not raise exception
        display_test_results(result)
        
        # Verify success message called
        mock_success.assert_called_once()
        assert "Analysis Complete" in str(mock_success.call_args)
    
    @patch('streamlit.error')
    def test_display_error_generic(self, mock_error):
        """Test displaying generic error."""
        from gui.components.results_display import display_error_with_solution
        
        result = {
            "success": False,
            "error": "Something went wrong",
            "error_type": "unknown"
        }
        
        display_error_with_solution(result)
        
        # Verify error displayed
        mock_error.assert_called()


# ============================================================================
# Agent Card Tests
# ============================================================================

class TestAgentCard:
    """Test agent card component."""
    
    @patch('streamlit.metric')
    @patch('streamlit.columns')
    def test_show_agent_stats(self, mock_cols, mock_metric):
        """Test agent statistics display."""
        from gui.components.agent_card import show_agent_stats
        
        # Mock columns
        mock_cols.return_value = [Mock(), Mock(), Mock(), Mock()]
        
        agents = [
            {"type": "Rule-Based", "filename": "01_basic.py"},
            {"type": "LLM-Powered", "filename": "02_llm.py"},
            {"type": "Rule-Based", "filename": "my_agent.py"},
        ]
        
        show_agent_stats(agents)
        
        # Should call metric 4 times (one per column)
        assert mock_metric.call_count == 4


# ============================================================================
# Test Executor Tests
# ============================================================================

class TestTestExecutor:
    """Test async test executor."""
    
    @pytest.mark.asyncio
    async def test_load_agent_async(self, tmp_path):
        """Test async agent loading."""
        from gui.business_logic.test_executor import TestExecutor
        
        # Create test agent file
        agent_code = '''
from agent_framework import Agent, Signal

class TestAgent(Agent):
    async def analyze(self, ticker, data):
        return Signal("bullish", 0.8, "Test")
'''
        
        agent_file = tmp_path / "test_agent.py"
        agent_file.write_text(agent_code)
        
        executor = TestExecutor()
        executor.examples_dir = tmp_path
        
        # Load agent
        agent_class = await executor._load_agent_async(agent_file, "TestAgent")
        
        assert agent_class is not None
        assert agent_class.__name__ == "TestAgent"
    
    def test_is_rag_agent_true(self):
        """Test RAG agent detection - positive case."""
        from gui.business_logic.test_executor import TestExecutor
        from agent_framework import RAGConfig
        
        # Mock RAG agent
        mock_agent = Mock()
        mock_agent.config = Mock()
        mock_agent.config.rag = RAGConfig()
        
        executor = TestExecutor()
        assert executor._is_rag_agent(mock_agent) is True
    
    def test_is_rag_agent_false(self):
        """Test RAG agent detection - negative case."""
        from gui.business_logic.test_executor import TestExecutor
        
        # Mock non-RAG agent
        mock_agent = Mock()
        mock_agent.config = Mock()
        mock_agent.config.rag = None
        
        executor = TestExecutor()
        assert executor._is_rag_agent(mock_agent) is False
    
    def test_detect_llm_fallback(self):
        """Test LLM fallback detection."""
        from gui.business_logic.test_executor import TestExecutor
        
        executor = TestExecutor()
        
        # Mock signal with fallback indicator
        fallback_signal = Mock()
        fallback_signal.reasoning = "LLM service unavailable - using fallback logic"
        
        assert executor._detect_llm_fallback(fallback_signal) is True
        
        # Normal signal
        normal_signal = Mock()
        normal_signal.reasoning = "Strong fundamentals indicate value"
        
        assert executor._detect_llm_fallback(normal_signal) is False
    
    def test_parse_llm_error_missing_package(self):
        """Test parsing missing package error."""
        from gui.business_logic.test_executor import TestExecutor
        
        executor = TestExecutor()
        reasoning = "Error: openai package not installed"
        
        error_info = executor._parse_llm_error(reasoning)
        
        assert error_info["error_type"] == "missing_package"
        assert "package" in error_info["description"].lower()
    
    def test_parse_llm_error_model_not_found(self):
        """Test parsing model not found error."""
        from gui.business_logic.test_executor import TestExecutor
        
        executor = TestExecutor()
        reasoning = "Error: model llama3.2 not found"
        
        error_info = executor._parse_llm_error(reasoning)
        
        assert error_info["error_type"] == "model_not_found"
    
    def test_parse_llm_error_connection(self):
        """Test parsing connection error."""
        from gui.business_logic.test_executor import TestExecutor
        
        executor = TestExecutor()
        reasoning = "Error: connection to Ollama failed"
        
        error_info = executor._parse_llm_error(reasoning)
        
        assert error_info["error_type"] == "connection_error"


# ============================================================================
# Batch Executor Tests
# ============================================================================

class TestBatchExecutor:
    """Test batch test executor."""
    
    @pytest.mark.asyncio
    async def test_aggregate_results(self):
        """Test result aggregation."""
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
                "execution_time": 1.2
            },
            {
                "success": False,
                "agent_name": "Agent2",
                "ticker": "AAPL",
                "error": "Test error"
            }
        ]
        
        # Mock config
        config = BatchTestConfig(
            agents=[{"name": "Agent1"}, {"name": "Agent2"}],
            tickers=["AAPL", "MSFT"],
            test_data_config=TestDataConfig(source="mock", ticker="AAPL"),
            max_concurrent=2
        )
        
        aggregated = executor._aggregate_results(results, config)
        
        # Verify aggregation
        assert aggregated["total_tests"] == 3
        assert aggregated["successful"] == 2
        assert aggregated["failed"] == 1
        assert aggregated["success_rate"] == pytest.approx(2/3)
        assert aggregated["avg_confidence"] == pytest.approx(0.75)
        
        # Verify distribution
        dist = aggregated["signal_distribution"]
        assert dist["bullish"] == 1
        assert dist["bearish"] == 1
        assert dist["neutral"] == 0
        
        # Verify by-agent grouping
        assert "Agent1" in aggregated["by_agent"]
        assert len(aggregated["by_agent"]["Agent1"]) == 2


# ============================================================================
# Stress Tests
# ============================================================================

class TestStress:
    """Stress tests for async operations."""
    
    @pytest.mark.asyncio
    async def test_many_parallel_operations(self):
        """Test handling many concurrent operations."""
        async def task(n):
            await asyncio.sleep(0.01)
            return n
        
        # Run 50 operations in parallel with limit of 10
        results = await run_parallel_with_limit(
            items=list(range(50)),
            async_func=task,
            max_concurrent=10,
            description="Stress test"
        )
        
        assert len(results) == 50
        assert results == list(range(50))
    
    @pytest.mark.asyncio
    async def test_timeout_recovery(self):
        """Test recovery from timeout errors."""
        runner = AsyncRunner()
        
        async def sometimes_slow(n):
            if n == 2:
                await asyncio.sleep(10.0)  # Will timeout
            else:
                await asyncio.sleep(0.01)
            return n
        
        # Test with gather (continues on errors)
        results = await asyncio.gather(
            runner.run_with_timeout(sometimes_slow(1), timeout=0.5),
            runner.run_with_timeout(sometimes_slow(2), timeout=0.5),
            runner.run_with_timeout(sometimes_slow(3), timeout=0.5),
            return_exceptions=True
        )
        
        # First and third succeed, second times out
        assert results[0] == 1
        assert isinstance(results[1], asyncio.TimeoutError)
        assert results[2] == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])
