# Setup Guide

Complete setup instructions for the AI Agent Framework with PostgreSQL.

## Prerequisites

- Python 3.10, 3.11, or 3.12
- Docker Desktop (recommended) OR PostgreSQL 12+
- Git

## Quick Setup (Docker - Recommended)

### Step 1: Clone and Install

```bash
git clone https://github.com/yourusername/ai-agent-builder.git
cd AI-Agent-Builder
pip install -e .
```

### Step 2: Start PostgreSQL

```bash
docker-compose up -d postgres
```

This will:
- Pull PostgreSQL 16 Alpine image
- Create database named `agent_framework`
- Initialize schema automatically
- Run on port 5432

Verify it's running:
```bash
docker ps
# Should show: agent_framework_db
```

### Step 3: Seed Sample Data

```bash
python seed_data.py
```

This loads 4 sample stocks (AAPL, MSFT, TSLA, JPM) with:
- Fundamental metrics
- 90 days of price history
- Recent news items
- SEC 10-K filing excerpts

### Step 4: Verify Setup

```bash
python quickstart.py
```

Expected output:
```
✅ Core imports successful
✅ Connected to database with 4 tickers
✅ Agent analysis: BULLISH (70%)
✅ RAG query successful (if sentence-transformers installed)
✅ FastAPI app loaded

🎉 Framework is ready to use!
```

### Step 5: Run Examples

```bash
# Simple agents (no LLM required)
python examples/01_basic.py

# LLM agents (requires Ollama or API keys)
python examples/02_llm_agent.py

# RAG analysis (requires sentence-transformers)
python examples/03_rag_agent.py
```

---

## Alternative: Local PostgreSQL Setup

If you prefer not to use Docker:

### Install PostgreSQL

**macOS:**
```bash
brew install postgresql@16
brew services start postgresql@16
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Windows:**
Download installer from https://www.postgresql.org/download/windows/

### Create Database

```bash
# Create database
createdb agent_framework

# Or with sudo if needed
sudo -u postgres createdb agent_framework
```

### Initialize Schema

```bash
psql agent_framework < schema.sql
```

### Seed Data

```bash
python seed_data.py
```

---

## Configuration

### Environment Variables

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env`:

```bash
# PostgreSQL Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/agent_framework

# LLM API Keys (optional)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

### Connection String Format

```
postgresql://[user]:[password]@[host]:[port]/[database]
```

Examples:
- Docker: `postgresql://postgres:postgres@localhost:5432/agent_framework`
- Local: `postgresql://postgres:postgres@localhost:5432/agent_framework`
- Remote: `postgresql://user:pass@db.example.com:5432/agent_framework`

---

## Optional Dependencies

### For LLM Agents

**Option 1: Ollama (Local, Free, Recommended)**

```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull model
ollama pull llama3.2

# Python client (already in setup.py[llm])
pip install -e .[llm]
```

**Option 2: OpenAI**

```bash
pip install -e .[llm]
echo "OPENAI_API_KEY=sk-..." >> .env
```

**Option 3: Anthropic Claude**

```bash
pip install -e .[llm]
echo "ANTHROPIC_API_KEY=sk-ant-..." >> .env
```

### For RAG (Document Analysis)

```bash
pip install -e .[rag]
```

This installs sentence-transformers (~100MB download on first use).

### All Features

```bash
pip install -e .[all]
```

Installs LLM providers, RAG, and development tools.

---

## Database Management

### Check Database Status

```bash
# List tables
docker exec agent_framework_db psql -U postgres agent_framework -c "\dt"

# Count records
docker exec agent_framework_db psql -U postgres agent_framework -c "SELECT COUNT(*) FROM fundamentals;"

# View tickers
docker exec agent_framework_db psql -U postgres agent_framework -c "SELECT ticker, name FROM fundamentals;"
```

### Reset Database

```bash
# Drop and recreate (Docker)
docker-compose down -v
docker-compose up -d postgres
python seed_data.py

# Or manually
docker exec agent_framework_db psql -U postgres agent_framework -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
docker exec -i agent_framework_db psql -U postgres agent_framework < schema.sql
python seed_data.py
```

### Backup Database

```bash
docker exec agent_framework_db pg_dump -U postgres agent_framework > backup.sql
```

### Restore Database

```bash
docker exec -i agent_framework_db psql -U postgres agent_framework < backup.sql
```

---

## Starting the API Server

```bash
uvicorn agent_framework.api:app --reload
```

Visit http://localhost:8000/docs for interactive API documentation.

---

## Running Tests

```bash
# Install test dependencies
pip install -e .[dev]

# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_framework.py::TestDatabase -v

# With coverage
pytest tests/ --cov=agent_framework --cov-report=html
```

---

## Troubleshooting

### "Connection refused" Error

**Problem:** Can't connect to PostgreSQL

**Solution:**
```bash
# Check if PostgreSQL is running
docker ps
# or
pg_isready

# Restart PostgreSQL
docker-compose restart postgres
# or
brew services restart postgresql@16
```

### "Database does not exist"

**Problem:** Database not created

**Solution:**
```bash
# Docker
docker-compose down -v
docker-compose up -d postgres

# Local
createdb agent_framework
psql agent_framework < schema.sql
```

### "No tickers in database"

**Problem:** Database is empty

**Solution:**
```bash
python seed_data.py
```

### Port 5432 Already in Use

**Problem:** Another PostgreSQL instance running

**Solution:**
```bash
# Find what's using the port
lsof -i :5432

# Stop other PostgreSQL
brew services stop postgresql

# Or use different port in docker-compose.yml:
ports:
  - "5433:5432"
# Then update DATABASE_URL to use port 5433
```

### "Import Error: No module named 'openai'"

**Problem:** Missing LLM dependencies

**Solution:**
```bash
pip install -e .[llm]
```

### "Import Error: No module named 'sentence_transformers'"

**Problem:** Missing RAG dependencies

**Solution:**
```bash
pip install -e .[rag]
```

---

## Production Setup

For production deployment:

1. **Use managed PostgreSQL** (AWS RDS, Google Cloud SQL, etc.)
2. **Enable SSL connections**
3. **Use environment variables** for secrets
4. **Set up connection pooling** (already implemented)
5. **Enable monitoring** (pg_stat_statements)
6. **Set up backups**

Example production connection:
```bash
DATABASE_URL=postgresql://user:pass@prod-db.us-east-1.rds.amazonaws.com:5432/agent_framework?sslmode=require
```

---

## Next Steps

1. ✅ Verify setup: `python quickstart.py`
2. 📚 Read [README.md](README.md)
3. 🎯 Run examples: `python examples/01_basic.py`
4. 🧪 Run tests: `pytest tests/`
5. 🚀 Build your first agent!

---

## Support

- Check [DATABASE_SETUP.md](DATABASE_SETUP.md) for detailed database docs
- Check [INSTALL.md](INSTALL.md) for installation options
- Review examples in `examples/` directory
- Run `python quickstart.py` for diagnostics