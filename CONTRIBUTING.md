# Contributing to AI Agent Builder

First off, thank you for considering contributing to AI Agent Builder! 🎉

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Environment details** (OS, Python version, etc.)
- **Code samples** if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear use case**
- **Why this would be useful**
- **Possible implementation** (if you have ideas)

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code, add tests
3. Ensure the test suite passes
4. Make sure your code follows the style guidelines
5. Write a clear commit message

## Development Setup
```bash
# Fork and clone
git clone https://github.com/your-username/ai-agent-builder.git
cd ai-agent-builder

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install

# Start PostgreSQL
docker-compose up -d

# Generate mock data
python generate_mock_data.py --tickers 10

# Run tests
pytest

# Start API
uvicorn agent_builder.api.main:app --reload
```

## Code Style

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://github.com/psf/black) for formatting
- Use [Ruff](https://github.com/charliermarsh/ruff) for linting
- Add type hints
- Write docstrings (Google style)

## Testing

- Write tests for new features
- Maintain test coverage > 80%
- Run `pytest` before submitting PR
- Add integration tests for API endpoints

## Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Reference issues and PRs liberally

Example:
```
Add batch query optimization for AgentContext

- Implement prefetch_common_metrics() method
- Reduces DB queries from 6 to 1
- Improves performance by 30%

Closes #123
```
## Questions?

Feel free to open an issue or discussion!