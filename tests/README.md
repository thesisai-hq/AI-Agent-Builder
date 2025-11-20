# Testing Guide - AI Agent Framework

**Audience:** 💻 Framework Users | Developers | Contributors

Complete guide to testing your agents and the framework itself.

---

## Overview

AI-Agent-Framework uses **pytest** for testing with full async support.

**Test coverage:** ~85%  
**Test framework:** pytest + pytest-asyncio  
**Test database:** Separate from development (agent_framework_test)

---

## Quick Start

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=agent_framework --cov-report=html

# Run specific test file
pytest tests/test_framework.py -v

# Run specific test
pytest tests/test_framework.py::TestModels::test_signal_creation -v

# Stop on first failure
pytest tests/ -x

# Show print statements
pytest tests/ -v -s
```

---

## Prerequisites

### 1. Install Test Dependencies

```bash
# Install dev dependencies (includes pytest)
pip install -e ".[dev]"

# Or install all (includes dev)
pip install -e ".[all]"
```

**Includes:**
- pytest
- pytest-asyncio
- pytest-cov
- black (formatting)
- ruff (linting)

---

### 2. Setup Test Database

```bash
# Create test database (one-time setup)
python setup_test_db.py

# Or manually:
docker compose up -d postgres
docker exec agent_framework_db createdb -U postgres agent_framework_test
docker exec -i agent_framework_db psql -U postgres agent_framework_test < schema.sql
```

---

## Writing Your Own Tests

### Test Template

```python
"""Test your custom agent."""

import pytest
import pytest_asyncio
from agent_framework import Agent, Signal, Database, Config


class TestMyAgent:
    """Tests for MyAgent."""
    
    @pytest.mark.asyncio
    async def test_agent_analysis(self):
        """Test agent analysis logic."""
        from my_agent import MyAgent
        
        agent = MyAgent()
        
        # Mock data
        data = {'pe_ratio': 12.0, 'roe': 25.0}
        
        # Run analysis
        signal = await agent.analyze('TEST', data)
        
        # Assertions
        assert signal.direction == 'bullish'
        assert signal.confidence > 0.5
        assert len(signal.reasoning) > 0


@pytest_asyncio.fixture
async def test_db():
    """Test database fixture."""
    db = Database(Config.get_test_database_url())
    await db.connect()
    yield db
    await db.disconnect()
```

**Save as:** `tests/test_my_agent.py`

**Run:** `pytest tests/test_my_agent.py -v`

---

## Test Patterns

### Pattern 1: Unit Test (No Database)

```python
@pytest.mark.asyncio
async def test_value_logic():
    """Test agent logic without database."""
    from examples.basic import ValueAgent
    
    agent = ValueAgent()
    
    # Mock data - undervalued
    data = {'pe_ratio': 10.0}
    signal = await agent.analyze('TEST', data)
    assert signal.direction == 'bullish'
    
    # Mock data - overvalued
    data = {'pe_ratio': 35.0}
    signal = await agent.analyze('TEST', data)
    assert signal.direction == 'bearish'
```

---

### Pattern 2: Integration Test (With Database)

```python
@pytest.mark.asyncio
async def test_with_real_data(test_db):
    """Test agent with database."""
    from examples.basic import ValueAgent
    
    agent = ValueAgent()
    
    # Get real test data
    tickers = await test_db.list_tickers()
    data = await test_db.get_fundamentals(tickers[0])
    signal = await agent.analyze(tickers[0], data)
    
    # Verify valid signal
    assert signal.direction in ['bullish', 'bearish', 'neutral']
    assert 0.0 <= signal.confidence <= 1.0
```

---

### Pattern 3: Mocking LLM Calls

```python
from unittest.mock import patch

@pytest.mark.asyncio
async def test_llm_agent_mocked():
    """Test LLM agent without calling API."""
    from examples.llm_agent import QualityAgent
    
    agent = QualityAgent()
    
    # Mock LLM response
    with patch.object(agent.llm, 'chat') as mock_chat:
        mock_chat.return_value = "bullish|80|Strong quality"
        
        data = {'pe_ratio': 15}
        signal = await agent.analyze('TEST', data)
        
        assert signal.direction == 'bullish'
        assert mock_chat.called
```

---

## Coverage Reports

```bash
# Generate HTML coverage report
pytest tests/ --cov=agent_framework --cov-report=html

# Open report
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
```

**Target:** 80%+ coverage

---

## Resources

- **pytest docs:** https://docs.pytest.org/
- **pytest-asyncio:** https://pytest-asyncio.readthedocs.io/
- **Framework API:** [API_REFERENCE.md](../docs/API_REFERENCE.md)
- **Contributing:** [CONTRIBUTING.md](../CONTRIBUTING.md)

---

**Build agents with confidence through testing!** ✅
