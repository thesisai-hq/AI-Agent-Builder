"""Test configuration and fixtures for GUI tests."""

import pytest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


@pytest.fixture
def examples_dir(tmp_path):
    """Create temporary examples directory for testing.
    
    Args:
        tmp_path: pytest temporary directory
        
    Returns:
        Path to examples directory
    """
    examples = tmp_path / "examples"
    examples.mkdir()
    return examples


@pytest.fixture
def sample_agent_code():
    """Sample agent code for testing.
    
    Returns:
        Valid Python agent code
    """
    return '''"""Sample test agent."""

from agent_framework import Agent, Signal

class SampleAgent(Agent):
    """Simple test agent."""
    
    async def analyze(self, ticker, data):
        """Basic analysis logic."""
        pe = data.get("pe_ratio", 0)
        
        if pe < 15:
            return Signal(
                direction="bullish",
                confidence=0.8,
                reasoning=f"Undervalued: PE={pe}"
            )
        
        return Signal(
            direction="neutral",
            confidence=0.5,
            reasoning="Fair value"
        )


if __name__ == "__main__":
    import asyncio
    from agent_framework import Config, Database
    
    async def main():
        agent = SampleAgent()
        data = {"pe_ratio": 12, "name": "Test Co"}
        signal = await agent.analyze("TEST", data)
        print(f"{signal.direction}: {signal.reasoning}")
    
    asyncio.run(main())
'''


@pytest.fixture
def mock_agent_info():
    """Mock agent information dictionary.
    
    Returns:
        Agent info dict
    """
    return {
        "name": "SampleAgent",
        "filename": "sample_agent.py",
        "type": "Rule-Based"
    }


@pytest.fixture
def mock_test_config():
    """Mock test configuration.
    
    Returns:
        TestDataConfig instance
    """
    from gui.components.test_config import TestDataConfig
    
    return TestDataConfig(
        source="mock",
        data={
            "pe_ratio": 20.0,
            "roe": 15.0,
            "profit_margin": 12.0,
            "revenue_growth": 15.0,
            "debt_to_equity": 0.8,
            "dividend_yield": 2.0,
            "name": "Test Company"
        },
        ticker="TEST"
    )


@pytest.fixture
def agent_loader(examples_dir):
    """Create AgentLoader instance with temp directory.
    
    Args:
        examples_dir: Temporary examples directory
        
    Returns:
        AgentLoader instance
    """
    from gui.agent_loader import AgentLoader
    return AgentLoader(examples_dir)


@pytest.fixture
def async_runner():
    """Create AsyncRunner instance.
    
    Returns:
        AsyncRunner instance
    """
    from gui.async_utils import AsyncRunner
    return AsyncRunner()


# ============================================================================
# Pytest Configuration
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers",
        "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers",
        "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers",
        "gui: marks tests that require Streamlit"
    )


# ============================================================================
# Helper Functions for Tests
# ============================================================================

def create_test_agent_file(directory: Path, filename: str, agent_code: str) -> Path:
    """Create a test agent file.
    
    Args:
        directory: Directory to create file in
        filename: Agent filename
        agent_code: Python code content
        
    Returns:
        Path to created file
    """
    agent_file = directory / filename
    agent_file.write_text(agent_code)
    return agent_file


async def mock_async_success(value):
    """Mock async function that succeeds.
    
    Args:
        value: Value to return
        
    Returns:
        The value after brief delay
    """
    await asyncio.sleep(0.01)
    return value


async def mock_async_failure(error_message: str):
    """Mock async function that fails.
    
    Args:
        error_message: Error message to raise
        
    Raises:
        ValueError with error_message
    """
    await asyncio.sleep(0.01)
    raise ValueError(error_message)
