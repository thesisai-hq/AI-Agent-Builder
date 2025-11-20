"""Integration tests for GUI workflows.

Tests complete user workflows from UI interaction to result display.
"""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gui.business_logic.test_executor import TestExecutor
from gui.components.test_config import TestDataConfig
from gui.pages.batch_test_page import BatchTestExecutor, BatchTestConfig


# ============================================================================
# Test Execution Integration Tests
# ============================================================================

class TestAgentExecutionWorkflow:
    """Test complete agent execution workflow."""
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_execute_simple_agent(self, sample_agent_file, sample_test_data):
        """Test executing a simple rule-based agent."""
        executor = TestExecutor()
        executor.examples_dir = sample_agent_file.parent
        
        agent_info = {
            "filename": sample_agent_file.name,
            "name": "SampleAgent",
            "type": "Rule-Based"
        }
        
        test_config = TestDataConfig(
            source="mock",
            data=sample_test_data,
            ticker="TEST"
        )
        
        result = await executor.execute_test_async(
            agent_info=agent_info,
            test_config=test_config,
            data=sample_test_data
        )
        
        # Verify result structure
        assert result["success"] is True
        assert "signal" in result
        assert result["signal"]["direction"] in ["bullish", "bearish", "neutral"]
        assert 0.0 <= result["signal"]["confidence"] <= 1.0
        assert len(result["signal"]["reasoning"]) > 0
        assert result["execution_time"] > 0
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_execute_with_timeout(self, sample_agent_file, sample_test_data):
        """Test timeout protection."""
        executor = TestExecutor()
        executor.examples_dir = sample_agent_file.parent
        
        # Create agent file with slow analysis
        slow_agent_code = '''
from agent_framework import Agent, Signal
import asyncio

class SlowAgent(Agent):
    async def analyze(self, ticker, data):
        await asyncio.sleep(100)  # Very slow
        return Signal("neutral", 0.5, "Slow")
'''
        
        slow_agent_file = sample_agent_file.parent / "slow_agent.py"
        slow_agent_file.write_text(slow_agent_code)
        
        agent_info = {
            "filename": "slow_agent.py",
            "name": "SlowAgent",
            "type": "Rule-Based"
        }
        
        test_config = TestDataConfig(
            source="mock",
            data=sample_test_data,
            ticker="TEST"
        )
        
        # Should timeout
        result = await executor.execute_test_async(
            agent_info=agent_info,
            test_config=test_config,
            data=sample_test_data
        )
        
        # Verify timeout handling
        assert result["success"] is False
        assert "timeout" in result["error"].lower()


# ============================================================================
# Batch Testing Integration Tests
# ============================================================================

class TestBatchTestingWorkflow:
    """Test batch testing workflow."""
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_batch_test_multiple_agents_tickers(
        self, 
        temp_examples_dir,
        sample_test_data
    ):
        """Test batch testing with multiple agents and tickers."""
        # Create two test agents
        agent1_code = '''
from agent_framework import Agent, Signal

class Agent1(Agent):
    async def analyze(self, ticker, data):
        if data.get("pe_ratio", 0) < 20:
            return Signal("bullish", 0.8, "Value")
        return Signal("neutral", 0.6, "Fair")
'''
        
        agent2_code = '''
from agent_framework import Agent, Signal

class Agent2(Agent):
    async def analyze(self, ticker, data):
        if data.get("revenue_growth", 0) > 10:
            return Signal("bullish", 0.7, "Growth")
        return Signal("neutral", 0.5, "Slow")
'''
        
        (temp_examples_dir / "agent1.py").write_text(agent1_code)
        (temp_examples_dir / "agent2.py").write_text(agent2_code)
        
        # Setup batch test
        batch_executor = BatchTestExecutor()
        batch_executor.executor.examples_dir = temp_examples_dir
        
        config = BatchTestConfig(
            agents=[
                {"filename": "agent1.py", "name": "Agent1"},
                {"filename": "agent2.py", "name": "Agent2"}
            ],
            tickers=["AAPL", "MSFT"],
            test_data_config=TestDataConfig(
                source="mock",
                data=sample_test_data,
                ticker="AAPL"
            ),
            max_concurrent=2
        )
        
        results = await batch_executor.run_batch_test(config)
        
        # Verify results
        assert results["total_tests"] == 4  # 2 agents × 2 tickers
        assert results["successful"] >= 0
        assert results["successful"] + results["failed"] == 4
        
        # Verify aggregation
        assert "by_agent" in results
        assert "by_ticker" in results
        assert "signal_distribution" in results
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_batch_test_with_failures(self, temp_examples_dir, sample_test_data):
        """Test batch testing handles failures gracefully."""
        # Create one good agent and one bad agent
        good_agent = '''
from agent_framework import Agent, Signal

class GoodAgent(Agent):
    async def analyze(self, ticker, data):
        return Signal("bullish", 0.8, "Good")
'''
        
        bad_agent = '''
from agent_framework import Agent, Signal

class BadAgent(Agent):
    async def analyze(self, ticker, data):
        raise ValueError("Intentional error")
'''
        
        (temp_examples_dir / "good.py").write_text(good_agent)
        (temp_examples_dir / "bad.py").write_text(bad_agent)
        
        batch_executor = BatchTestExecutor()
        batch_executor.executor.examples_dir = temp_examples_dir
        
        config = BatchTestConfig(
            agents=[
                {"filename": "good.py", "name": "GoodAgent"},
                {"filename": "bad.py", "name": "BadAgent"}
            ],
            tickers=["AAPL"],
            test_data_config=TestDataConfig(
                source="mock",
                data=sample_test_data,
                ticker="AAPL"
            ),
            max_concurrent=2
        )
        
        results = await batch_executor.run_batch_test(config)
        
        # One should succeed, one should fail
        assert results["successful"] == 1
        assert results["failed"] == 1
        assert results["total_tests"] == 2


# ============================================================================
# Performance Integration Tests
# ============================================================================

class TestPerformanceIntegration:
    """Test performance characteristics."""
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_parallel_faster_than_sequential(self, temp_examples_dir):
        """Verify parallel execution is faster."""
        import time
        
        # Create simple agent
        agent_code = '''
from agent_framework import Agent, Signal
import asyncio

class TestAgent(Agent):
    async def analyze(self, ticker, data):
        await asyncio.sleep(0.1)  # Simulate work
        return Signal("neutral", 0.5, "Test")
'''
        
        (temp_examples_dir / "test.py").write_text(agent_code)
        
        batch_executor = BatchTestExecutor()
        batch_executor.executor.examples_dir = temp_examples_dir
        
        # Test with 5 tickers (would take 0.5s sequential)
        config = BatchTestConfig(
            agents=[{"filename": "test.py", "name": "TestAgent"}],
            tickers=["T1", "T2", "T3", "T4", "T5"],
            test_data_config=TestDataConfig(
                source="mock",
                data={"pe_ratio": 20},
                ticker="T1"
            ),
            max_concurrent=5  # All parallel
        )
        
        start = time.time()
        results = await batch_executor.run_batch_test(config)
        elapsed = time.time() - start
        
        # Should complete in ~0.1s (parallel) not 0.5s (sequential)
        assert elapsed < 0.3  # Allow some overhead
        assert results["total_tests"] == 5


# ============================================================================
# Error Recovery Integration Tests
# ============================================================================

class TestErrorRecovery:
    """Test error recovery in integrated workflows."""
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_recover_from_missing_agent_file(self, temp_examples_dir):
        """Test graceful handling of missing agent files."""
        executor = TestExecutor()
        executor.examples_dir = temp_examples_dir
        
        agent_info = {
            "filename": "nonexistent.py",
            "name": "NonexistentAgent",
            "type": "Rule-Based"
        }
        
        test_config = TestDataConfig(
            source="mock",
            data={"pe_ratio": 20},
            ticker="TEST"
        )
        
        result = await executor.execute_test_async(
            agent_info=agent_info,
            test_config=test_config,
            data={"pe_ratio": 20}
        )
        
        # Should return error, not crash
        assert result["success"] is False
        assert "not found" in result["error"].lower()
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_recover_from_invalid_agent_code(self, temp_examples_dir):
        """Test handling of syntactically invalid agent files."""
        executor = TestExecutor()
        executor.examples_dir = temp_examples_dir
        
        # Create invalid Python file
        invalid_code = "this is not valid python code {{{"
        (temp_examples_dir / "invalid.py").write_text(invalid_code)
        
        agent_info = {
            "filename": "invalid.py",
            "name": "InvalidAgent",
            "type": "Rule-Based"
        }
        
        test_config = TestDataConfig(
            source="mock",
            data={"pe_ratio": 20},
            ticker="TEST"
        )
        
        result = await executor.execute_test_async(
            agent_info=agent_info,
            test_config=test_config,
            data={"pe_ratio": 20}
        )
        
        # Should handle gracefully
        assert result["success"] is False
        assert "error" in result


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])
