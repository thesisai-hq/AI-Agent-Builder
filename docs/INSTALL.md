# Installation Guide

## Prerequisites

- Python 3.10, 3.11, or 3.12
- pip (Python package manager)
- Docker and Docker Compose (recommended)
- Git (for cloning repository)

## Quick Install (Recommended)

```bash
# Clone repository
git clone git@github.com:thesisai-hq/AI-Agent-Builder.git
cd AI-Agent-Builder

# Install framework
pip install -e .

# Start PostgreSQL with Docker
docker-compose up -d postgres

# Seed database
python seed_data.py

# Verify installation
python quickstart.py
```

That's it! The framework is ready to use.

## Detailed Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/ai-agent-framework.git
cd AI-Agent-Builder
```

### 2. Install Framework

#### Basic Installation (Core Only)

```bash
pip install -e .
```

This installs:
- FastAPI and Uvicorn
- Pydantic for validation
- asyncpg for PostgreSQL
- NumPy for data processing

#### With Optional Dependencies

```bash
# Install with LLM support (OpenAI, Anthropic, Ollama)
pip install -e .[llm]

# Install with RAG support (sentence-transformers)
pip install -e .[rag]

# Install with development tools (pytest, black)
pip install -e .[dev]

# Install everything
pip install -e .[all]
```

### 3. Set Up PostgreSQL

#### Option A: Docker (Recommended)

```bash
# Start PostgreSQL
docker-compose up -d postgres

# Check it's running
docker-compose ps

# View logs if needed
docker-compose logs postgres
```

Docker automatically:
- Creates the database
- Runs the schema
- Sets up health checks
- Persists data in a volume

#### Option B: Local PostgreSQL

See [DATABASE_SETUP.md](DATABASE_SETUP.md) for detailed instructions.

### 4. Seed Database

```bash
python seed_data.py
```

This adds sample data:
- 4 tickers (AAPL, MSFT, TSLA, JPM)
- 90 days of price history per ticker
- 3 news items per ticker
- 1 SEC 10-K filing per ticker

### 5. Configure Environment (Optional)

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
# DATABASE_URL=postgresql://postgres:postgres@localhost:5433/agent_framework
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
```

### 6. Verify Installation

```bash
python quickstart.py
```

Expected output:
```
============================================================
AI Agent Framework - Quick Start
Version 2.0.0
============================================================

🔍 Checking imports...
✅ Core imports successful

⚙️  Testing configuration...
✅ Config helpers working

🗄️  Testing database...
✅ Connected to database with 4 tickers
   Available: AAPL, MSFT, TSLA, JPM
✅ Retrieved data for AAPL: PE=28.5

🤖 Testing simple agent...
✅ Agent analysis: BULLISH (70%)
   Reasoning: PE ratio: 28.5

📚 Testing RAG system...
✅ RAG query successful

🌐 Testing API...
✅ FastAPI app loaded

============================================================
Summary
============================================================
✅ Imports
✅ Configuration
✅ Database
✅ Simple Agent
⚠️  RAG System (optional)
✅ API

Passed: 5/6

🎉 Framework is ready to use!

Next steps:
  1. Run examples: python examples/01_basic.py
  2. Start API: uvicorn agent_framework.api:app --reload
  3. Run tests: pytest tests/
```

## Running Examples

All examples work immediately after installation:

```bash
# Simple agents (no LLM required)
python examples/01_basic.py

# LLM agents (requires Ollama/OpenAI/Anthropic)
python examples/02_llm_agent.py

# RAG analysis (requires sentence-transformers)
python examples/03_rag_agent.py
```

## Starting the API Server

```bash
# Development mode with auto-reload
uvicorn agent_framework.api:app --reload

# Production mode
uvicorn agent_framework.api:app --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000/docs for interactive API documentation.

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=agent_framework --cov-report=html

# Run specific test file
pytest tests/test_framework.py -v

# Run specific test
pytest tests/test_framework.py::TestDatabase::test_database_connection -v
```

## Optional: LLM Setup

### Ollama (Local, Free)

```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Start service (if not auto-started)
ollama serve

# Pull a model
ollama pull llama3.2

# Verify
ollama list
```

No configuration needed - examples will detect Ollama automatically.

### OpenAI

```bash
# Install OpenAI client
pip install openai

# Add to .env
echo "OPENAI_API_KEY=sk-your-key-here" >> .env
```

Update examples to use OpenAI:
```python
llm=LLMConfig(
    provider='openai',
    model='gpt-4',
    api_key=Config.get_llm_api_key('openai')
)
```

### Anthropic

```bash
# Install Anthropic client
pip install anthropic

# Add to .env
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" >> .env
```

Update examples to use Anthropic:
```python
llm=LLMConfig(
    provider='anthropic',
    model='claude-3-sonnet-20240229',
    api_key=Config.get_llm_api_key('anthropic')
)
```

## Optional: RAG Setup

```bash
# Install sentence-transformers
pip install sentence-transformers
```

First use will download ~100MB of models. Subsequent uses are fast.

## Troubleshooting

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'agent_framework'`

**Solution:**
```bash
# Make sure you're in the project directory
cd AI-Agent-Builder

# Install in editable mode
pip install -e .
```

### Database Connection Failed

**Problem:** `ConnectionError: Could not connect to database`

**Solution:**
```bash
# Check Docker is running
docker ps

# Check PostgreSQL container is up
docker-compose ps

# If not running, start it
docker-compose up -d postgres

# Check logs
docker-compose logs postgres

# Verify database exists
docker exec agent_framework_db psql -U postgres -l
```

### Database Empty

**Problem:** `⚠️  Database is empty. Run: python seed_data.py`

**Solution:**
```bash
python seed_data.py
```

### LLM Not Working

**Problem:** LLM agents fail with authentication errors

**Solution:**

For Ollama:
```bash
# Check Ollama is running
ollama list

# If not running
ollama serve

# Pull model if needed
ollama pull llama3.2
```

For OpenAI/Anthropic:
```bash
# Add API key to .env
echo "OPENAI_API_KEY=sk-your-key" >> .env
echo "ANTHROPIC_API_KEY=sk-ant-your-key" >> .env
```

### RAG Slow on First Use

**Problem:** First RAG query takes 30+ seconds

**Solution:** This is normal! sentence-transformers downloads models on first use (~100MB). Subsequent queries are fast (< 1 second).

### Tests Failing

**Problem:** Some tests fail with import or connection errors

**Solution:**
```bash
# Install test dependencies
pip install -e .[dev]

# Make sure database is running
docker-compose up -d postgres

# Make sure data is seeded
python seed_data.py

# Run tests
pytest tests/ -v
```

### Port Already in Use

**Problem:** Port 5433 already in use

**Solution:**
```bash
# Edit docker-compose.yml
# Change ports:
#   - "5434:5432"  # Use different port

# Update .env
DATABASE_URL=postgresql://postgres:postgres@localhost:5434/agent_framework

# Restart
docker-compose down
docker-compose up -d postgres
```

## Uninstall

```bash
# Stop Docker containers
docker-compose down

# Remove Docker volumes (WARNING: deletes all data)
docker-compose down -v

# Uninstall Python package
pip uninstall ai-agent-framework

# Remove repository
cd ..
rm -rf AI-Agent-Builder
```

## Development Setup

For contributing to the framework:

```bash
# Clone repository
git clone https://github.com/yourusername/ai-agent-framework.git
cd AI-Agent-Builder

# Install with dev dependencies
pip install -e .[dev]

# Start PostgreSQL
docker-compose up -d postgres

# Seed database
python seed_data.py

# Run tests
pytest tests/ -v

# Format code
black agent_framework/ examples/ tests/

# Run examples
python examples/01_basic.py
```

## Docker Development Environment

```bash
# Build custom Docker image (if needed)
docker build -t ai-agent-framework .

# Run container with environment variables
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://postgres:postgres@host.docker.internal:5433/agent_framework" \
  -e OPENAI_API_KEY="sk-..." \
  ai-agent-framework

# Or use docker-compose (when configured)
docker-compose up
```

## Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install framework
pip install -e .[all]

# Deactivate when done
deactivate
```

## System Requirements

### Minimum
- Python 3.10+
- 2GB RAM
- 1GB disk space
- Docker (for PostgreSQL)

### Recommended
- Python 3.11 or 3.12
- 4GB+ RAM
- 5GB disk space (for models)
- Docker with 2GB+ memory allocation

### For LLM (Ollama)
- 8GB+ RAM
- 10GB+ disk space (for models)
- Modern CPU (Apple Silicon recommended for Mac)

### For Production
- 8GB+ RAM
- Multi-core CPU
- Managed PostgreSQL database
- Load balancer for API

## Upgrading

### From v1.x to v2.0

v2.0 has breaking changes. See migration guide in README.md.

Key changes:
- Pydantic models instead of dataclasses
- No singleton database pattern
- Dependency injection in API
- Explicit connection management

```bash
# Upgrade
git pull origin main
pip install -e . --upgrade

# Update code
# - Replace get_database() singleton with Database() instances
# - Update model imports (Signal is now Pydantic)
# - Add explicit db.connect() / db.disconnect()
```

### Patch Updates

```bash
git pull origin main
pip install -e . --upgrade
```

## Next Steps

1. ✅ Verify installation: `python quickstart.py`
2. 📖 Read the [README.md](../README.md)
3. 🎯 Run examples: `python examples/01_basic.py`
4. 🧪 Run tests: `pytest tests/`
5. 🚀 Build your first agent!

## Getting Help

- **Documentation**: See docs/ folder
- **Examples**: See examples/ folder
- **Issues**: GitHub issues
- **Database**: See [DATABASE_SETUP.md](DATABASE_SETUP.md)
- **Structure**: See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

## Additional Resources

- PostgreSQL: https://www.postgresql.org/docs/
- FastAPI: https://fastapi.tiangolo.com/
- Pydantic: https://docs.pydantic.dev/
- asyncpg: https://magicstack.github.io/asyncpg/
- Ollama: https://ollama.ai/
