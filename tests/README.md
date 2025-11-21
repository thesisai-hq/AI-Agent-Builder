# Testing Guide - AI Agent Framework

**Complete guide to testing agents and the framework.**

**Last Updated:** November 20, 2025 (Documentation Review Complete)

---

## 🚀 Quick Start - Run Tests Now!

### For Everyone (Most Common)

```bash
cd ~/AI-Agent-Builder

# Run all tests with one command
pytest tests/gui/ -v

# Expected output:
# ✅ 54 tests passed in ~3 seconds
```

### For Framework Developers

```bash
cd ~/AI-Agent-Builder

# Run framework + GUI tests
pytest tests/ -v

# Expected output:
# ✅ ~100 tests passed in ~6 seconds
```

### For Quick Verification (No pytest needed)

```bash
cd ~/AI-Agent-Builder

# Standalone verification scripts
python3 tests/gui/test_verify_setup.py        # Verify GUI setup
python3 tests/gui/test_verify_phase1.py       # Verify Phase 1 refactoring
python3 tests/gui/test_verify_signals.py      # Verify Signal usage
```

---

## 📁 Test Organization

```
tests/
├── test_framework.py            # Core framework tests (~40 tests)
│
└── gui/                         # GUI tests (54 tests)
    ├── conftest.py              # Pytest configuration & fixtures
    ├── run_tests.sh             # Convenient test runner
    │
    ├── Core Tests (40 tests)
    ├── test_security.py         # Security & sanitization (17 tests) 🔒
    ├── test_integration.py      # End-to-end workflows (7 tests)
    ├── test_test_config.py      # Data configuration (16 tests)
    │
    └── Verification (14 tests)
        ├── test_verify_async_utils.py   # Async utils (3 tests)
        ├── test_verify_setup.py         # Setup (1 test)
        ├── test_verify_signal.py        # Signal (1 test)
        ├── test_verify_phase1.py        # Phase 1 (3 tests)
        ├── test_verify_refactoring.py   # Refactoring (7 tests)
        └── test_verify_signals.py       # Signal style (2 tests)
```

**Total:** 94+ tests across framework and GUI

---

## 🎯 Running Tests - All Methods

### Method 1: Run All Tests

```bash
cd ~/AI-Agent-Builder

# Everything (framework + GUI)
pytest tests/ -v

# Just GUI tests
pytest tests/gui/ -v

# Just framework tests
pytest tests/test_framework.py -v
```

---

### Method 2: Run Specific Test Files

```bash
cd ~/AI-Agent-Builder

# Security tests (critical)
pytest tests/gui/test_security.py -v

# Integration tests
pytest tests/gui/test_integration.py -v

# Config tests
pytest tests/gui/test_test_config.py -v

# All verification tests
pytest tests/gui/test_verify_*.py -v
```

---

### Method 3: Run Specific Test Functions

```bash
cd ~/AI-Agent-Builder

# Run one specific test
pytest tests/gui/test_security.py::TestInputSanitization::test_sanitize_identifier_removes_special_chars -v

# Run all tests in a class
pytest tests/gui/test_security.py::TestInputSanitization -v

# Run tests matching pattern
pytest tests/gui/ -k "security" -v
pytest tests/gui/ -k "integration" -v
```

---

### Method 4: Run with Coverage

```bash
cd ~/AI-Agent-Builder

# Terminal coverage report
pytest tests/gui/ --cov=gui --cov-report=term-missing

# HTML coverage report (opens in browser)
pytest tests/gui/ --cov=gui --cov-report=html
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
```

**Coverage Targets:**
- Security: 100% ✅
- Integration: 80%+ ✅
- Config: 90%+ ✅
- Overall: >75% ✅

---

### Method 5: Using Test Runner Script

```bash
cd ~/AI-Agent-Builder

# Make executable (first time only)
chmod +x tests/gui/run_tests.sh

# Run complete test suite with coverage
./tests/gui/run_tests.sh
```

**Output includes:**
- All test results
- Coverage report
- Link to HTML report

---

### Method 6: Standalone Verification Scripts

```bash
cd ~/AI-Agent-Builder

# These don't need pytest - run directly
python3 tests/gui/test_verify_setup.py
python3 tests/gui/test_verify_phase1.py
python3 tests/gui/test_verify_signals.py
python3 tests/gui/test_verify_refactoring.py
```

**Best for:**
- Quick sanity checks
- User documentation
- CI/CD verification steps

---

## 📊 Test Categories Explained

### 🔒 Security Tests (CRITICAL)

**File:** `tests/gui/test_security.py` (17 tests)

**What we test:**
- Input sanitization (prevent code injection)
- String escaping (prevent breakout attacks)
- Numeric validation (prevent overflows)
- Filename validation (prevent path traversal)

**Why critical:** Generates executable Python code from user input

**Run:**
```bash
pytest tests/gui/test_security.py -v
```

**Coverage requirement:** 100%

---

### 🔄 Integration Tests (VALUABLE)

**File:** `tests/gui/test_integration.py` (7 tests)

**What we test:**
- Complete test execution workflow
- Agent loading and initialization
- Async execution patterns
- Error handling end-to-end
- RAG agent workflows

**Why valuable:** Ensures components work together

**Run:**
```bash
pytest tests/gui/test_integration.py -v
```

**Coverage target:** 80%+

---

### 📦 Config Tests (USEFUL)

**File:** `tests/gui/test_test_config.py` (16 tests)

**What we test:**
- Mock data configuration
- Database configuration
- PDF upload configuration
- YFinance integration
- Data validation

**Why useful:** TestDataConfig is core to all testing

**Run:**
```bash
pytest tests/gui/test_test_config.py -v
```

**Coverage target:** 90%+

---

### ✅ Verification Tests (CONVENIENT)

**Files:** `test_verify_*.py` (14 tests total)

**What we test:**
- Async utils refactoring
- GUI setup correctness
- Signal creation
- Phase 1 refactoring
- Code style checks

**Why useful:** Quick checks, user-friendly output

**Run with pytest:**
```bash
pytest tests/gui/test_verify_*.py -v
```

**Run standalone:**
```bash
python3 tests/gui/test_verify_setup.py
```

---

## 🛠️ Prerequisites

### Install Test Dependencies

```bash
# Option 1: Install all (recommended)
pip install -e ".[all]"

# Option 2: Install dev only
pip install -e ".[dev]"

# Option 3: Manual install
pip install pytest pytest-asyncio pytest-cov
```

**Includes:**
- pytest (test framework)
- pytest-asyncio (async support)
- pytest-cov (coverage reports)
- black (code formatter)
- ruff (linter)

---

### Setup Test Database (Optional)

**Only needed for framework tests, not GUI tests.**

```bash
# Start PostgreSQL
docker compose up -d postgres

# Create test database
python setup_test_db.py

# Verify
docker exec -it agent_framework_db psql -U postgres -l | grep test
```

**Note:** GUI tests don't require database (use mock data)

---

## 📝 Writing Your Own Tests

### Test Template for Your Agent

```python
"""Test your custom agent."""

import pytest
from agent_framework import Agent, Signal


class TestMyAgent:
    """Tests for MyAgent."""
    
    @pytest.mark.asyncio
    async def test_bullish_signal(self):
        """Test agent generates bullish signal."""
        from my_agent import MyAgent
        
        agent = MyAgent()
        data = {'pe_ratio': 12.0, 'roe': 25.0}  # Strong fundamentals
        
        signal = await agent.analyze('TEST', data)
        
        assert signal.direction == 'bullish'
        assert signal.confidence > 0.7
        assert 'undervalued' in signal.reasoning.lower()
    
    @pytest.mark.asyncio
    async def test_bearish_signal(self):
        """Test agent generates bearish signal."""
        from my_agent import MyAgent
        
        agent = MyAgent()
        data = {'pe_ratio': 45.0, 'debt_to_equity': 3.0}  # Risky
        
        signal = await agent.analyze('TEST', data)
        
        assert signal.direction == 'bearish'
        assert signal.confidence > 0.6
```

**Save as:** `tests/test_my_agent.py`

**Run:**
```bash
pytest tests/test_my_agent.py -v
```

---

## 📈 Coverage Reports

### Generate Coverage Report

```bash
cd ~/AI-Agent-Builder

# Terminal report with missing lines
pytest tests/gui/ --cov=gui --cov-report=term-missing

# Example output:
# Name                              Stmts   Miss  Cover   Missing
# ---------------------------------------------------------------
# gui/agent_creator.py                180     10    94%   45-48
# gui/business_logic/test_executor.py 120      8    93%   
# gui/components/results_display.py   85      5    94%
# ---------------------------------------------------------------
# TOTAL                               385     23    94%
```

### HTML Coverage Report

```bash
pytest tests/gui/ --cov=gui --cov-report=html

# Open in browser
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

**Shows:**
- Line-by-line coverage
- Missing coverage highlighted
- Interactive navigation

---

## 🔧 Troubleshooting

### Import Errors

```bash
# Error: ModuleNotFoundError: No module named 'agent_framework'

# Fix 1: Install in editable mode
pip install -e .

# Fix 2: Run from project root
cd ~/AI-Agent-Builder
pytest tests/gui/ -v

# Fix 3: Check Python path
python3 -c "import agent_framework; print('OK')"
```

---

### No Tests Collected

```bash
# Error: collected 0 items

# Fix: Use correct path
cd ~/AI-Agent-Builder
pytest tests/gui/ -v  # Correct
# NOT: cd tests/gui && pytest -v  # Wrong directory
```

---

### Async Test Failures

```python
# Error: RuntimeError: no running event loop

# Fix: Add @pytest.mark.asyncio decorator
@pytest.mark.asyncio
async def test_async_function():
    result = await async_operation()
    assert result is not None
```

---

### Fixture Not Found

```bash
# Error: fixture 'examples_dir' not found

# Check: Ensure conftest.py exists
ls tests/gui/conftest.py

# Fixtures must be in conftest.py or imported
```

---

## 🎓 Best Practices

### ✅ DO:

1. **Run tests before committing**
   ```bash
   pytest tests/gui/ -v
   ```

2. **Check coverage**
   ```bash
   pytest tests/gui/ --cov=gui
   ```

3. **Test security code**
   - 100% coverage for input handling

4. **Use clear test names**
   - `test_sanitize_removes_sql_injection` ✅
   - Not: `test_1` ❌

5. **Keep tests focused**
   - One concept per test
   - Clear arrange-act-assert

---

### ❌ DON'T:

1. **Don't skip failing tests**
   - Fix or delete, don't ignore

2. **Don't test UI rendering**
   - Streamlit testing is complex
   - Use manual testing

3. **Don't test third-party code**
   - They have their own tests

4. **Don't commit broken tests**
   - All tests must pass

---

## 📋 Before Committing Checklist

```bash
cd ~/AI-Agent-Builder

# 1. Run all tests
pytest tests/gui/ -v
# ✅ All tests pass

# 2. Check coverage
pytest tests/gui/ --cov=gui --cov-report=term-missing
# ✅ Coverage >75%

# 3. Run verification scripts
python3 tests/gui/test_verify_phase1.py
python3 tests/gui/test_verify_signals.py
# ✅ All verifications pass

# 4. Format code (optional)
black gui/ tests/
# ✅ Code formatted

# 5. Lint code (optional)
ruff check gui/ tests/
# ✅ No lint errors

# All green? Commit! ✅
```

---

## 🎯 Test Strategy

### What We Test

**Security (100% coverage):**
- All user input handling
- Code generation
- File operations

**Integration (80% coverage):**
- Complete workflows
- Component interaction
- Error recovery

**Core Logic (90% coverage):**
- Data configuration
- Agent loading
- Test execution

### What We Don't Test

- ❌ Streamlit UI rendering (manual testing)
- ❌ Simple getters/setters (no logic)
- ❌ Third-party libraries (they test themselves)
- ❌ Removed features (cleanup old tests)

**Philosophy:** Test what adds value, skip what doesn't.

---

## 📚 Additional Resources

### Documentation
- **GUI Testing:** [tests/gui/README.md](gui/README.md)
- **pytest:** https://docs.pytest.org/
- **pytest-asyncio:** https://pytest-asyncio.readthedocs.io/
- **API Reference:** [docs/API_REFERENCE.md](../docs/API_REFERENCE.md)

### Support
- **Issues:** [GitHub Issues](https://github.com/thesisai-hq/AI-Agent-Builder/issues)
- **Discussions:** [GitHub Discussions](https://github.com/thesisai-hq/AI-Agent-Builder/discussions)

---

## 📊 Current Test Status

### Test Suite Metrics

```
Framework Tests:    40 tests    85% coverage ✅
GUI Tests:          54 tests    78% coverage ✅
Total:             ~94 tests

Execution Time:     ~6 seconds
Pass Rate:          100%
Last Cleanup:       Nov 20, 2025
Status:            Production Ready ✅
```

### Coverage by Component

```
agent_framework/     85% ✅
gui/core/            95% ✅
gui/components/      78% ✅
gui/business_logic/  82% ✅
Overall:            >75% ✅
```

---

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -e ".[dev]"
      
      - name: Run tests
        run: |
          pytest tests/ -v \
            --cov=agent_framework \
            --cov=gui \
            --cov-report=xml \
            --cov-report=term
      
      - name: Check coverage threshold
        run: coverage report --fail-under=75
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## 🎓 For Students & Learners

### Understanding Test Output

```bash
$ pytest tests/gui/test_security.py -v

tests/gui/test_security.py::TestInputSanitization::test_sanitize_identifier_removes_special_chars PASSED [14%]
tests/gui/test_security.py::TestInputSanitization::test_sanitize_identifier_ensures_valid_start PASSED [28%]
...

========== 17 passed in 1.2s ==========
```

**What this means:**
- ✅ Each line = one test
- ✅ `PASSED` = test succeeded
- ✅ `[14%]` = progress through suite
- ✅ `17 passed` = all tests worked!

---

### What if Tests Fail?

```bash
$ pytest tests/gui/test_security.py -v

tests/gui/test_security.py::test_something FAILED [50%]

FAILURES
_________________________ test_something _________________________

    def test_something():
        result = do_something()
>       assert result == "expected"
E       AssertionError: assert 'actual' == 'expected'
```

**What to do:**
1. Read the error message
2. Look at the line with `>` (where it failed)
3. Fix the code being tested
4. Run test again
5. Repeat until it passes

---

## 📖 Learning Resources

### Example Tests to Study

**Start here (simplest):**
```bash
# Look at test structure
cat tests/gui/test_verify_signal.py
# Simple, clear, easy to understand
```

**Then study:**
```bash
# More complex tests
cat tests/gui/test_security.py
cat tests/gui/test_integration.py
```

### How to Learn Testing

1. **Read existing tests** - See patterns
2. **Run tests** - Watch them work
3. **Modify tests** - Break them, fix them
4. **Write tests** - Start with simple ones
5. **Review coverage** - See what's tested

---

## 🚀 Summary

### Quick Commands Reference

```bash
# Most common
pytest tests/gui/ -v                              # Run all GUI tests

# By category
pytest tests/gui/test_security.py -v              # Security only
pytest tests/gui/test_integration.py -v           # Integration only
pytest tests/gui/test_verify_*.py -v              # Verification only

# With coverage
pytest tests/gui/ --cov=gui --cov-report=html     # HTML report

# Standalone
python3 tests/gui/test_verify_setup.py            # No pytest needed

# Everything
pytest tests/ -v                                  # Framework + GUI
```

### Expected Results

```
54 tests in tests/gui/ ✅
All pass in ~3 seconds ✅
Coverage >75% ✅
```

### Next Steps

1. **Run:** `pytest tests/gui/ -v`
2. **Verify:** All tests pass
3. **Check coverage:** `pytest tests/gui/ --cov=gui`
4. **Read:** [tests/gui/README.md](gui/README.md) for details

---

**Testing made simple. Run with confidence!** ✅
