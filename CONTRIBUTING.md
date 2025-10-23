# Contributing to AI Agent Framework

Thank you for considering contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/ai-agent-framework.git
   cd ai-agent-framework
   ```
3. **Install in development mode**:
   ```bash
   pip install -e .[dev]
   ```
4. **Set up the database**:
   ```bash
   docker-compose up -d postgres
   python seed_data.py
   python setup_test_db.py
   ```

## Development Workflow

1. **Create a branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**

3. **Run tests**:
   ```bash
   pytest tests/ -v
   ```

4. **Format code**:
   ```bash
   black agent_framework/ examples/ tests/
   ```

5. **Commit your changes**:
   ```bash
   git commit -m "Add feature: description"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**

## Code Standards

### Python Style

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://black.readthedocs.io/) for formatting (line length: 88)
- Use type hints for all functions
- Write docstrings for public APIs

### Code Quality

- **Type hints**: All functions must have type hints
- **Docstrings**: Use Google-style docstrings
- **Testing**: New features must include tests
- **Coverage**: Maintain >80% test coverage

### Example

```python
from typing import Optional

def my_function(ticker: str, data: dict) -> Optional[Signal]:
    """Brief description of function.
    
    Args:
        ticker: Stock ticker symbol
        data: Fundamental data dictionary
        
    Returns:
        Signal object or None if analysis fails
        
    Raises:
        ValueError: If ticker is invalid
    """
    # Implementation
    pass
```

## Testing

### Writing Tests

- Place tests in `tests/` directory
- Use pytest fixtures for database access
- Test both success and error cases
- Use descriptive test names

### Running Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=agent_framework

# Specific test
pytest tests/test_framework.py::TestDatabase::test_connection -v
```

### Test Structure

```python
import pytest
import pytest_asyncio

@pytest_asyncio.fixture
async def test_db():
    """Database fixture."""
    db = Database(Config.get_test_database_url())
    await db.connect()
    yield db
    await db.disconnect()

@pytest.mark.asyncio
async def test_my_feature(test_db):
    """Test description."""
    result = await test_db.my_method()
    assert result is not None
```

## Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Update CHANGELOG.md** with your changes
4. **Ensure all tests pass**
5. **Keep PRs focused** on a single feature/fix

### PR Title Format

- `feat: Add new feature`
- `fix: Fix bug description`
- `docs: Update documentation`
- `test: Add tests for X`
- `refactor: Refactor component`

### PR Description

Include:
- **What**: Description of changes
- **Why**: Reason for changes
- **How**: Implementation approach
- **Testing**: How you tested the changes

## Bug Reports

### Before Submitting

1. Check existing issues
2. Try the latest version
3. Verify it's not a configuration issue

### Bug Report Template

```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Run command X
2. See error

**Expected behavior**
What should happen

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.11]
- Framework version: [e.g., 1.0.0]

**Additional context**
Any other relevant information
```

## Feature Requests

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
Description of the problem

**Describe the solution you'd like**
Clear description of desired solution

**Describe alternatives**
Alternative solutions considered

**Additional context**
Any other context or examples
```

## Code Review Process

### What We Look For

- ✅ Code quality and readability
- ✅ Test coverage
- ✅ Documentation updates
- ✅ Performance implications
- ✅ Backward compatibility

### Review Timeline

- Initial review: Within 3 days
- Follow-up: Within 2 days
- Merge: After approval and CI passes

## Development Guidelines

### Adding a New Agent Type

1. Create the agent class inheriting from `Agent`
2. Implement the `analyze()` method
3. Add example in `examples/`
4. Add tests in `tests/`
5. Update documentation

### Adding a New Database Method

1. Add method to `Database` class
2. Add error handling
3. Add docstring
4. Add tests
5. Update documentation

### Adding Dependencies

- Minimize new dependencies
- Use optional dependencies when possible
- Update `requirements.txt` or `setup.py`
- Document in README if user-facing

## Questions?

- Open an issue for discussion
- Check documentation in `docs/`
- Review existing code and tests

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🙏
