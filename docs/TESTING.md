# Testing Guide

## Quick Setup

### 1. Set Up Test Database

```bash
# Run the setup script
python setup_test_db.py
```

Or manually:

```bash
# Create test database
docker exec agent_framework_db createdb -U postgres agent_framework_test

# Run schema
docker exec -i agent_framework_db psql -U postgres agent_framework_test < schema.sql

# Seed test database
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/agent_framework_test python seed_data.py
```

### 2. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=agent_framework --cov-report=html

# Run specific test file
pytest tests/test_framework.py -v

# Run specific test class
pytest tests/test_framework.py::TestDatabase -v

# Run specific test
pytest tests/test_framework.py::TestDatabase::test_database_connection -v
```

## Test Database

The framework uses a **separate test database** (`agent_framework_test`) to ensure:
- ✅ Test isolation
- ✅ No interference with development data
- ✅ Parallel test execution (future)
- ✅ Safe cleanup

### Configuration

Test database URL is configured via:
1. Environment variable: `TEST_DATABASE_URL`
2. Default: `postgresql://postgres:postgres@localhost:5433/agent_framework_test`

## Test Structure

```
tests/
└── test_framework.py          # All tests
    ├── TestModels             # Pydantic model tests
    ├── TestDatabase           # Database operation tests
    ├── TestAgent              # Agent functionality tests
    ├── TestRAGSystem          # RAG system tests
    ├── TestUtilities          # Utility function tests
    └── TestIntegration        # Integration tests
```

## Writing Tests

### Test Fixtures

Use the `test_db` fixture for database tests:

```python
@pytest.mark.asyncio
async def test_my_feature(test_db):
    """Test with database access."""
    data = await test_db.get_fundamentals('AAPL')
    assert data is not None
```

### Async Tests

All async tests must use `@pytest.mark.asyncio`:

```python
@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    result = await my_async_function()
    assert result == expected
```

### Model Validation Tests

Test Pydantic models with ValidationError:

```python
from pydantic import ValidationError

def test_model_validation():
    """Test model rejects invalid data."""
    with pytest.raises(ValidationError):
        Signal(direction='invalid', confidence=0.5, reasoning='test')
```

## Common Test Patterns

### 1. Test Database Query

```python
@pytest.mark.asyncio
async def test_query(test_db):
    tickers = await test_db.list_tickers()
    assert isinstance(tickers, list)
    assert len(tickers) > 0
```

### 2. Test Agent

```python
@pytest.mark.asyncio
async def test_agent(test_db):
    agent = MyAgent()
    data = await test_db.get_fundamentals('AAPL')
    signal = agent.analyze('AAPL', data)
    
    assert isinstance(signal, Signal)
    assert signal.direction in ('bullish', 'bearish', 'neutral')
    assert 0 <= signal.confidence <= 1
```

### 3. Test Error Handling

```python
from agent_framework.database import QueryError

@pytest.mark.asyncio
async def test_error_handling(test_db):
    with pytest.raises(QueryError):
        await test_db.get_fundamentals('INVALID' * 100)
```

## Test Coverage

Current coverage: **~85%**

View coverage report:
```bash
pytest tests/ --cov=agent_framework --cov-report=html
open htmlcov/index.html  # or browse to file
```

## Troubleshooting

### Test Database Doesn't Exist

**Error:** `database "agent_framework_test" does not exist`

**Solution:**
```bash
python setup_test_db.py
```

### Connection Refused

**Error:** `connection refused`

**Solution:**
```bash
docker-compose ps  # Check PostgreSQL is running
docker-compose up -d postgres  # Start if needed
```

### Fixture Not Working

**Error:** `AttributeError: 'async_generator' object has no attribute`

**Solution:** Make sure you're using `@pytest_asyncio.fixture`:
```python
import pytest_asyncio

@pytest_asyncio.fixture
async def my_fixture():
    # Setup
    yield something
    # Teardown
```

### Tests Pass Locally But Fail in CI

**Common causes:**
1. Test database not set up in CI
2. Different PostgreSQL version
3. Missing environment variables
4. Race conditions (use proper fixtures)

### Slow Tests

RAG tests can be slow on first run (downloads models). Subsequent runs are fast.

To skip slow tests:
```bash
pytest tests/ -v -m "not slow"
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: agent_framework_test
        ports:
          - 5432:5432
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      
      - name: Install dependencies
        run: |
          pip install -e .[dev]
      
      - name: Run schema
        run: psql postgresql://postgres:postgres@localhost:5432/agent_framework_test < schema.sql
      
      - name: Seed test database
        run: DATABASE_URL=postgresql://postgres:postgres@localhost:5432/agent_framework_test python seed_data.py
      
      - name: Run tests
        run: pytest tests/ -v --cov=agent_framework
```

## Best Practices

### 1. Test Isolation

- ✅ Use separate test database
- ✅ Use fixtures for setup/teardown
- ✅ Don't depend on test execution order
- ✅ Clean up after tests

### 2. Meaningful Tests

- ✅ Test one thing per test
- ✅ Use descriptive test names
- ✅ Include docstrings
- ✅ Assert specific conditions

### 3. Fast Tests

- ✅ Use fixtures to share setup
- ✅ Mock external services when possible
- ✅ Run database tests in parallel (future)
- ✅ Skip slow tests in development

### 4. Maintainable Tests

- ✅ Keep tests simple
- ✅ Avoid test duplication
- ✅ Use helper functions
- ✅ Update tests with code changes

## Test Commands Cheat Sheet

```bash
# Basic
pytest tests/                              # Run all tests
pytest tests/ -v                           # Verbose output
pytest tests/ -x                           # Stop on first failure
pytest tests/ -k test_database            # Run matching tests

# Coverage
pytest tests/ --cov=agent_framework       # Show coverage
pytest tests/ --cov-report=html           # HTML report
pytest tests/ --cov-report=term-missing   # Show missing lines

# Specific tests
pytest tests/test_framework.py            # One file
pytest tests/test_framework.py::TestDatabase  # One class
pytest tests/test_framework.py::TestDatabase::test_connection  # One test

# Output
pytest tests/ -v                          # Verbose
pytest tests/ -s                          # Show print statements
pytest tests/ --tb=short                  # Short traceback
pytest tests/ -vv                         # Very verbose

# Performance
pytest tests/ --durations=10              # Show 10 slowest tests
pytest tests/ -n auto                     # Parallel (requires pytest-xdist)

# Debugging
pytest tests/ --pdb                       # Drop into debugger on failure
pytest tests/ -l                          # Show local variables
```

## Resources

- pytest documentation: https://docs.pytest.org/
- pytest-asyncio: https://pytest-asyncio.readthedocs.io/
- Coverage.py: https://coverage.readthedocs.io/

## Next Steps

1. ✅ Set up test database: `python setup_test_db.py`
2. ✅ Run tests: `pytest tests/ -v`
3. ✅ Check coverage: `pytest tests/ --cov=agent_framework`
4. 📝 Write tests for your custom agents
5. 🔄 Set up CI/CD pipeline
