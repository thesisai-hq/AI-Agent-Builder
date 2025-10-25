# Testing Your Agents - Making Sure They Work

**What is testing?** Writing code that automatically checks if your agents work correctly. Like having a robot assistant that tests your code for you!

**Why test?** Catch bugs before they cause problems. Make sure changes don't break things.

## Simple Testing (For Beginners)

Don't want to write formal tests? Just run your agent and check the output:

```python
# test_my_agent.py
import asyncio
from agent_framework import Database, Config
from my_agent import MyAgent

async def test_manually():
    """Quick test of your agent."""
    db = Database(Config.get_database_url())
    await db.connect()
    
    # Create agent
    agent = MyAgent()
    
    # Test on known stock
    data = await db.get_fundamentals('AAPL')
    signal = agent.analyze('AAPL', data)
    
    # Check results
    print(f"Testing MyAgent on AAPL...")
    print(f"  Direction: {signal.direction}")
    print(f"  Confidence: {signal.confidence}")
    print(f"  Reasoning: {signal.reasoning}")
    
    # Verify it looks right
    if signal.direction in ['bullish', 'bearish', 'neutral']:
        print("✅ Direction is valid")
    else:
        print("❌ Direction is invalid!")
    
    if 0.0 <= signal.confidence <= 1.0:
        print("✅ Confidence in valid range")
    else:
        print("❌ Confidence out of range!")
    
    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(test_manually())
```

Run it:
```bash
python test_my_agent.py
```

**Pros:** Simple, easy to understand  
**Cons:** You have to check manually, not automated

## Formal Testing (Recommended)

**What is pytest?** A tool that automatically runs your tests and tells you if they pass or fail.

### One-Time Setup

```bash
# Install pytest if you haven't
pip install pytest pytest-asyncio

# Create test database (one time only)
python setup_test_db.py
```

**What this does:** Creates a separate database for testing (so you don't mess up your real data).

### Write a Test

Create `test_my_agent.py`:

```python
import pytest
from agent_framework import Database, Config
from my_agent import MyAgent

@pytest.fixture
async def test_db():
    """
    Set up test database.
    This runs before each test.
    """
    db = Database(Config.get_test_database_url())
    await db.connect()
    yield db  # Test runs here
    await db.disconnect()

@pytest.mark.asyncio
async def test_agent_on_aapl(test_db):
    """
    Test that agent works on Apple stock.
    """
    agent = MyAgent()
    
    # Get Apple's data
    data = await test_db.get_fundamentals('AAPL')
    
    # Analyze it
    signal = agent.analyze('AAPL', data)
    
    # Check results
    assert signal.direction in ['bullish', 'bearish', 'neutral']
    assert 0.0 <= signal.confidence <= 1.0
    assert len(signal.reasoning) > 0

@pytest.mark.asyncio
async def test_low_pe_is_bullish(test_db):
    """
    Test that agent recommends buying low PE stocks.
    """
    agent = MyAgent()
    
    # Create fake data with low PE
    fake_data = {
        'ticker': 'TEST',
        'pe_ratio': 10.0,  # Very low PE
        'revenue_growth': 15.0,
        'profit_margin': 20.0
    }
    
    signal = agent.analyze('TEST', fake_data)
    
    # Should recommend buying
    assert signal.direction == 'bullish'
    assert signal.confidence > 0.5
```

**What this does:**
- `@pytest.fixture` - Sets up test database automatically
- `@pytest.mark.asyncio` - Tells pytest this test is async
- `assert` - Check if something is true (test fails if not)

### Run Tests

```bash
# Run all tests
pytest test_my_agent.py -v

# Run specific test
pytest test_my_agent.py::test_agent_on_aapl -v

# See detailed output
pytest test_my_agent.py -v -s
```

**What you'll see:**
```
test_my_agent.py::test_agent_on_aapl PASSED        [50%]
test_my_agent.py::test_low_pe_is_bullish PASSED    [100%]

✅ 2 passed in 0.54s
```

## Understanding Test Output

**PASSED** ✅ - Test worked! Everything is correct.

**FAILED** ❌ - Test found a problem. Look at the error message.

Example failure:
```
test_my_agent.py::test_agent_on_aapl FAILED

    assert signal.direction in ['bullish', 'bearish', 'neutral']
    AssertionError: assert 'BULLISH' in ['bullish', 'bearish', 'neutral']
```

**What this means:** Your agent returned "BULLISH" (uppercase) but test expected lowercase. Fix your code!

## What to Test

### Test 1: Agent Works on Real Data

```python
@pytest.mark.asyncio
async def test_agent_works(test_db):
    """Basic smoke test - does agent run without crashing?"""
    agent = MyAgent()
    data = await test_db.get_fundamentals('AAPL')
    signal = agent.analyze('AAPL', data)
    
    # Just check it returned something valid
    assert signal is not None
    assert signal.direction in ['bullish', 'bearish', 'neutral']
```

**Tests:** Agent doesn't crash, returns valid signal.

### Test 2: Agent Logic Works

```python
@pytest.mark.asyncio
async def test_low_pe_means_buy(test_db):
    """Test that low PE = buy recommendation."""
    agent = MyAgent()
    
    # Make up data with low PE
    data = {'pe_ratio': 10.0, 'profit_margin': 20.0}
    signal = agent.analyze('TEST', data)
    
    # Should be bullish
    assert signal.direction == 'bullish'
```

**Tests:** Your agent's logic is correct.

### Test 3: Edge Cases

```python
@pytest.mark.asyncio
async def test_handles_missing_data(test_db):
    """Test agent doesn't crash with missing data."""
    agent = MyAgent()
    
    # Empty data
    data = {}
    signal = agent.analyze('TEST', data)
    
    # Should still return something
    assert signal is not None
```

**Tests:** Agent handles errors gracefully.

## Test the Framework Itself

Run the built-in tests:

```bash
# Setup test database (one time)
python setup_test_db.py

# Run all framework tests
pytest tests/ -v

# See test coverage
pytest tests/ --cov=agent_framework
```

**What this tests:** The framework's database, models, utilities.

## Common Test Patterns

### Pattern 1: Test Database Connection

```python
@pytest.mark.asyncio
async def test_database_connection(test_db):
    """Test we can connect to database."""
    # If we get here, connection worked!
    assert test_db is not None
    
    # Check it's healthy
    health = await test_db.health_check()
    assert health == True
```

### Pattern 2: Test Agent on All Stocks

```python
@pytest.mark.asyncio
async def test_agent_on_all_stocks(test_db):
    """Test agent works on every stock."""
    agent = MyAgent()
    tickers = await test_db.list_tickers()
    
    for ticker in tickers:
        data = await test_db.get_fundamentals(ticker)
        signal = agent.analyze(ticker, data)
        
        # Should work for all stocks
        assert signal.direction in ['bullish', 'bearish', 'neutral']
```

### Pattern 3: Test With Fake Data

```python
def test_agent_logic():
    """Test agent without database (faster!)"""
    agent = MyAgent()
    
    # No database needed - use fake data
    fake_data = {
        'pe_ratio': 15.0,
        'profit_margin': 25.0,
        'revenue_growth': 10.0
    }
    
    signal = agent.analyze('FAKE', fake_data)
    assert signal.confidence > 0
```

**Benefit:** Tests run faster (no database queries).

## Mocking (Advanced)

**What is mocking?** Pretending a component exists without actually using it. Good for testing AI agents without spending money on API calls.

```python
from unittest.mock import Mock

def test_ai_agent_without_real_api():
    """Test AI agent without calling actual AI API."""
    from my_ai_agent import MyAIAgent
    
    agent = MyAIAgent()
    
    # Replace real AI with fake one
    agent.llm = Mock()
    agent.llm.chat.return_value = "bullish|80|Strong fundamentals"
    
    # Test works without spending money on API!
    signal = agent.analyze('AAPL', {'pe_ratio': 20})
    assert signal.direction == 'bullish'
```

**Why mock?** 
- Don't spend money on API calls during testing
- Tests run faster
- Tests work without internet

## When Tests Fail

### Read the Error

```
AssertionError: assert 'BULLISH' in ['bullish', 'bearish', 'neutral']
```

**Translation:** Your agent returned "BULLISH" but test expected lowercase "bullish". Fix the capitalization!

### Check What Was Returned

```python
signal = agent.analyze('AAPL', data)
print(f"Got: {signal.direction}")  # Print to see what it actually is
assert signal.direction == 'bullish'
```

### Use Debugger

```python
import pdb; pdb.set_trace()  # Pauses here

signal = agent.analyze('AAPL', data)
# Now you can inspect variables
```

## Best Practices

### 1. Test After Every Change

```bash
# After changing your agent
pytest test_my_agent.py -v
```

### 2. Test Happy Path (Normal Case)

```python
def test_normal_usage():
    """Test typical use case."""
    # Most common scenario
```

### 3. Test Edge Cases

```python
def test_empty_data():
    """Test with no data."""
    
def test_extreme_values():
    """Test with weird values (PE=0, PE=10000, etc.)"""
```

### 4. Keep Tests Simple

```python
# Good - one thing per test
def test_low_pe_is_bullish():
    assert agent.analyze(...).direction == 'bullish'

# Bad - too much in one test
def test_everything():
    assert agent.analyze(...).direction == 'bullish'
    assert agent.analyze(...).confidence > 0.5
    assert agent.analyze(...).reasoning != ''
    # ... 50 more assertions
```

### 5. Name Tests Clearly

```python
# Good names
test_low_pe_recommends_buy()
test_handles_missing_data()
test_works_on_apple_stock()

# Bad names
test_1()
test_stuff()
test_agent()
```

## Troubleshooting Tests

### "Test database not found"

```bash
# Create it
python setup_test_db.py
```

### "Connection refused"

```bash
# Make sure Docker is running
docker-compose up -d postgres
```

### "Import error"

```bash
# Reinstall framework
pip install -e .
```

### Tests are slow

**Solution:** Mock the database or use fake data instead of real queries.

### "pytest: command not found"

```bash
# Install pytest
pip install pytest pytest-asyncio
```

## Quick Commands

```bash
# Run all your tests
pytest -v

# Run specific file
pytest test_my_agent.py -v

# Run specific test
pytest test_my_agent.py::test_low_pe_is_bullish -v

# See print statements
pytest -v -s

# Stop on first failure
pytest -x

# Run tests matching name
pytest -k "agent" -v

# Check test coverage
pytest --cov=agent_framework --cov-report=html
```

## Example Test File

Here's a complete example you can copy:

```python
# test_my_value_agent.py
import pytest
from agent_framework import Database, Config
from my_agent import ValueAgent

@pytest.fixture
async def test_db():
    """Setup test database."""
    db = Database(Config.get_test_database_url())
    await db.connect()
    yield db
    await db.disconnect()

@pytest.mark.asyncio
async def test_value_agent_exists(test_db):
    """Test we can create the agent."""
    agent = ValueAgent()
    assert agent is not None

@pytest.mark.asyncio
async def test_analyzes_apple(test_db):
    """Test agent works on Apple stock."""
    agent = ValueAgent()
    data = await test_db.get_fundamentals('AAPL')
    signal = agent.analyze('AAPL', data)
    
    assert signal.direction in ['bullish', 'bearish', 'neutral']
    assert 0.0 <= signal.confidence <= 1.0
    assert len(signal.reasoning) > 0

def test_low_pe_is_bullish():
    """Test low PE = buy recommendation."""
    agent = ValueAgent()
    data = {'pe_ratio': 10.0}
    signal = agent.analyze('TEST', data)
    
    assert signal.direction == 'bullish'
    assert signal.confidence > 0.7

def test_high_pe_is_bearish():
    """Test high PE = sell recommendation."""
    agent = ValueAgent()
    data = {'pe_ratio': 40.0}
    signal = agent.analyze('TEST', data)
    
    assert signal.direction == 'bearish'
```

Run it:
```bash
pytest test_my_value_agent.py -v
```

## Next Steps

1. ✅ Write simple tests for your agents
2. ✅ Run tests after making changes
3. ✅ Fix any failures
4. ✅ Add more tests as you add features

**Remember:** Testing seems like extra work, but it saves you from bugs later!

---

**Not required for learning, but very helpful as you build more complex agents.** Start simple and add tests as you go!
