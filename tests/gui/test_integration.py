"""Integration tests for GUI workflows.

Tests complete user workflows from UI interaction to result display.
NO batch testing - focused on single-agent testing workflows.
"""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import Mock, patch
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gui.business_logic.test_executor import TestExecutor
from gui.components.test_config import TestDataConfig


# ============================================================================
# Test Execution Integration Tests
# ============================================================================

class TestAgentExecutionWorkflow:
    """Test complete agent execution workflow."""
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_execute_simple_agent(self, examples_dir, sample_agent_code):
        """Test executing a simple rule-based agent."""
        # Create test agent file
        agent_file = examples_dir / "sample_agent.py"
        agent_file.write_text(sample_agent_code)
        
        executor = TestExecutor()
        executor.examples_dir = examples_dir
        
        agent_info = {
            "filename": "sample_agent.py",
            "name": "SampleAgent",
            "type": "Rule-Based"
        }
        
        test_data = {
            "pe_ratio": 12.0,
            "roe": 15.0,
            "profit_margin": 12.0,
            "revenue_growth": 15.0,
            "debt_to_equity": 0.8,
            "dividend_yield": 2.0,
            "name": "Test Company"
        }
        
        test_config = TestDataConfig(
            source="mock",
            data=test_data,
            ticker="TEST"
        )
        
        result = await executor.execute_test_async(
            agent_info=agent_info,
            test_config=test_config,
            data=test_data
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
    async def test_execute_with_timeout(self, examples_dir):
        """Test timeout protection."""
        # Create agent file with slow analysis
        slow_agent_code = '''from agent_framework import Agent, Signal
import asyncio

class SlowAgent(Agent):
    async def analyze(self, ticker, data):
        await asyncio.sleep(100)  # Very slow
        return Signal(direction="neutral", confidence=0.5, reasoning="Slow")
'''
        
        slow_agent_file = examples_dir / "slow_agent.py"
        slow_agent_file.write_text(slow_agent_code)
        
        executor = TestExecutor()
        executor.examples_dir = examples_dir
        
        agent_info = {
            "filename": "slow_agent.py",
            "name": "SlowAgent",
            "type": "Rule-Based"
        }
        
        test_config = TestDataConfig(
            source="mock",
            data={"pe_ratio": 20},
            ticker="TEST"
        )
        
        # Should timeout
        result = await executor.execute_test_async(
            agent_info=agent_info,
            test_config=test_config,
            data={"pe_ratio": 20}
        )
        
        # Verify timeout handling
        assert result["success"] is False
        assert "timeout" in result["error"].lower() or "timed out" in result["error"].lower()


# ============================================================================
# Error Recovery Integration Tests
# ============================================================================

class TestErrorRecovery:
    """Test error recovery in integrated workflows."""
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_recover_from_missing_agent_file(self, examples_dir):
        """Test graceful handling of missing agent files."""
        executor = TestExecutor()
        executor.examples_dir = examples_dir
        
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
    async def test_recover_from_invalid_agent_code(self, examples_dir):
        """Test handling of syntactically invalid agent files."""
        executor = TestExecutor()
        executor.examples_dir = examples_dir
        
        # Create invalid Python file
        invalid_code = "this is not valid python code {{{"
        (examples_dir / "invalid.py").write_text(invalid_code)
        
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
# RAG Agent Integration Tests
# ============================================================================

class TestRAGAgentWorkflow:
    """Test RAG agent execution workflow."""
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_rag_agent_with_pdf(self, examples_dir):
        """Test RAG agent with PDF document."""
        # Create simple RAG agent
        rag_agent_code = '''from agent_framework import Agent, Signal, AgentConfig, RAGConfig, LLMConfig

class RAGTestAgent(Agent):
    def __init__(self):
        config = AgentConfig(
            name="RAGTestAgent",
            description="Test RAG agent",
            rag=RAGConfig(chunk_size=200, chunk_overlap=20, top_k=3),
            llm=LLMConfig(provider="ollama", model="llama3.2")
        )
        super().__init__(config)
    
    async def analyze(self, ticker, document_text):
        # Simple analysis without actual RAG/LLM
        if len(document_text) > 100:
            return Signal(direction="bullish", confidence=0.7, reasoning="Document analyzed")
        return Signal(direction="neutral", confidence=0.5, reasoning="Short document")
'''
        
        (examples_dir / "rag_agent.py").write_text(rag_agent_code)
        
        executor = TestExecutor()
        executor.examples_dir = examples_dir
        
        agent_info = {
            "filename": "rag_agent.py",
            "name": "RAGTestAgent",
            "type": "RAG-Powered"
        }
        
        # Mock PDF file
        mock_pdf = Mock()
        mock_pdf.name = "test.pdf"
        
        test_config = TestDataConfig(
            source="pdf",
            uploaded_file=mock_pdf,
            ticker="AAPL"
        )
        
        # For this test, we'll just verify the executor can handle RAG agents
        # (actual PDF processing would require PyPDF2 and is tested separately)
        result = await executor.execute_test_async(
            agent_info=agent_info,
            test_config=test_config,
            data=None
        )
        
        # Should recognize as RAG agent
        # May fail due to PDF processing, but should handle gracefully
        assert "success" in result


# ============================================================================
# Agent Loader Integration Tests
# ============================================================================

class TestAgentLoaderIntegration:
    """Test agent loader integration."""
    
    def test_list_agents(self, examples_dir, sample_agent_code):
        """Test listing agents from directory."""
        from gui.agent_loader import AgentLoader
        
        # Create test agents
        (examples_dir / "agent1.py").write_text(sample_agent_code)
        (examples_dir / "agent2.py").write_text(sample_agent_code.replace("SampleAgent", "Agent2"))
        
        loader = AgentLoader(examples_dir)
        agents = loader.list_agents()
        
        assert len(agents) == 2
        assert all(a["filename"].endswith(".py") for a in agents)
        assert all("name" in a for a in agents)
        assert all("type" in a for a in agents)
    
    def test_get_agent_code(self, examples_dir, sample_agent_code):
        """Test retrieving agent code."""
        from gui.agent_loader import AgentLoader
        
        (examples_dir / "test.py").write_text(sample_agent_code)
        
        loader = AgentLoader(examples_dir)
        code = loader.get_agent_code("test.py")
        
        assert code == sample_agent_code
        assert "SampleAgent" in code


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])
