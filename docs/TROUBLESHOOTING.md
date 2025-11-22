# Troubleshooting Guide

Common issues and solutions for AI-Agent-Builder.

---

## Quick Diagnosis

**Start here if you're stuck:**

```bash
# Check Python version (need 3.10+)
python3 --version

# Check Docker is running
docker ps

# Check database is running
docker ps | grep postgres

# Check environment is activated
which python  # Should show venv/conda path

# Check installation
pip show ai-agent-framework

# Test framework import
python -c "from agent_framework import Agent, Database; print('✅ Framework works')"
```

---

## Installation Issues

### Module Not Found

**Error:**
```
ModuleNotFoundError: No module named 'agent_framework'
ModuleNotFoundError: No module named 'openai'
ModuleNotFoundError: No module named 'ollama'
```

**Solutions:**

**1. Framework not installed:**
```bash
cd ~/AI-Agent-Builder
pip install -e ".[all]"
```

**2. Wrong environment active:**
```bash
# Conda
conda activate agent-framework

# venv
cd ~/AI-Agent-Builder
source venv/bin/activate

# Verify
which python  # Should show environment path
```

**3. Missing optional dependencies:**
```bash
# Install LLM support (OpenAI, Anthropic, Ollama)
pip install -e ".[llm]"

# Install RAG support (document analysis)
pip install -e ".[rag]"

# Install everything
pip install -e ".[all]"
```

**4. System Python confusion:**
```bash
# Use python3, not python
python3 -m pip install -e ".[all]"

# Or create alias
alias python=python3
```

---

### Permission Denied

**Error:**
```
PermissionError: [Errno 13] Permission denied
```

**Solutions:**

```bash
# Option 1: Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -e ".[all]"

# Option 2: User install (system Python only)
pip install --user -e ".[all]"

# Option 3: Fix permissions (Linux/Mac)
sudo chown -R $USER:$USER ~/AI-Agent-Builder
```

---

### Python Version Too Old

**Error:**
```
ERROR: Package requires Python >=3.10
```

**Solutions:**

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv
python3.11 -m venv venv
source venv/bin/activate
```

**macOS:**
```bash
brew install python@3.11
/usr/local/opt/python@3.11/bin/python3.11 -m venv venv
source venv/bin/activate
```

**Use conda (easiest):**
```bash
conda create -n agent-framework python=3.11 -y
conda activate agent-framework
```

---

## Database Issues

### Can't Connect to Database

**Error:**
```
ConnectionError: Could not connect to database
asyncpg.exceptions.InvalidPasswordError
Connection refused
```

**Solutions:**

**1. Database not running:**
```bash
# Check if running
docker ps | grep postgres

# Start database
docker compose up -d postgres

# Wait for startup
sleep 10

# Check logs
docker compose logs postgres
```

**2. Wrong credentials:**
```bash
# Check .env file
cat .env | grep DB_

# Should match docker-compose.yml
cat docker-compose.yml | grep POSTGRES_

# Fix if needed
nano .env
```

**3. Wrong port:**
```bash
# Check if port is available
lsof -i :5433

# Try different port
# Edit .env:
DB_PORT=5434

# Restart database
docker compose down
docker compose up -d postgres
```

**4. Database not initialized:**
```bash
# Remove and recreate
docker compose down -v
docker compose up -d postgres
sleep 10
python seed_data.py
```

---

### Port Already in Use

**Error:**
```
Error starting container: port is already allocated
Bind for 0.0.0.0:5433 failed: port is already allocated
```

**Solutions:**

**Option 1: Stop conflicting service:**
```bash
# Find what's using the port
lsof -i :5433

# Stop it
sudo systemctl stop postgresql  # If system PostgreSQL
```

**Option 2: Use different port:**
```bash
# Edit .env
nano .env
# Change: DB_PORT=5434

# Edit docker-compose.yml
nano docker-compose.yml
# Change: "5434:5432"

# Restart
docker compose down
docker compose up -d postgres
```

---

### Database Data Missing

**Error:**
```
No data available for AAPL
QueryError: relation "fundamentals" does not exist
```

**Solutions:**

```bash
# Run seed script
python seed_data.py

# Or manually:
docker compose exec postgres psql -U postgres -d agent_framework -f /docker-entrypoint-initdb.d/schema.sql
python seed_data.py

# Verify
python -c "
import asyncio
from agent_framework import Database, Config
async def check():
    db = Database(Config.get_database_url())
    await db.connect()
    tickers = await db.list_tickers()
    print(f'Found {len(tickers)} tickers: {tickers}')
    await db.disconnect()
asyncio.run(check())
"
```

---

## LLM Issues

### Ollama Connection Failed

**Error:**
```
LLMError: Could not initialize ollama
Connection refused [Errno 111]
```

**Solutions:**

**1. Ollama not running:**
```bash
# Start Ollama service (in separate terminal)
ollama serve

# Or run as background service (Linux)
nohup ollama serve &

# macOS (usually auto-starts)
# Check: ps aux | grep ollama
```

**2. Ollama not installed:**
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Verify
ollama --version
```

**3. Wrong URL:**
```bash
# Check .env
cat .env | grep OLLAMA_BASE_URL

# Should be:
OLLAMA_BASE_URL=http://localhost:11434

# Test connection
curl http://localhost:11434/api/tags
```

---

### Model Not Found

**Error:**
```
LLMError: Model llama3.2 not found
```

**Solutions:**

```bash
# List available models
ollama list

# Pull missing model
ollama pull llama3.2

# Verify
ollama list | grep llama3.2

# Test model
ollama run llama3.2 "Hello"
```

**Popular models:**
```bash
ollama pull llama3.2      # Latest (4GB)
ollama pull mistral       # Fast (4GB)
ollama pull phi           # Small (2GB)
```

---

### OpenAI/Anthropic API Key Error

**Error:**
```
APIError: Invalid API key
AuthenticationError
```

**Solutions:**

**1. API key not set:**
```bash
# Add to .env
nano .env

# OpenAI
OPENAI_API_KEY=sk-your-key-here

# Anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Restart Python script
```

**2. Invalid key format:**
```bash
# Check for spaces
cat .env | grep API_KEY

# Should be:
OPENAI_API_KEY=sk-abc123  # No spaces

# NOT:
OPENAI_API_KEY= sk-abc123  # ❌ Space after =
OPENAI_API_KEY=sk-abc123   # ❌ Space after key
```

**3. Key expired or invalid:**
- Get new key from https://platform.openai.com/api-keys
- Or https://console.anthropic.com/

---

### LLM Package Not Installed

**Error:**
```
LLMError: Ollama package not installed
ImportError: No module named 'openai'
```

**Solutions:**

```bash
# Install all LLM providers
pip install -e ".[llm]"

# Or specific provider
pip install ollama       # Free, local
pip install openai       # Paid API
pip install anthropic    # Paid API

# Verify
pip list | grep -E "(ollama|openai|anthropic)"
```

---

## GUI Issues

### GUI Won't Start

**Error:**
```
streamlit: command not found
```

**Solutions:**

```bash
# Run GUI setup (installs all dependencies)
cd ~/AI-Agent-Builder
./gui/setup.sh

# Or manual install
pip install -r gui/requirements.txt

# Verify
streamlit --version
```

**Note:** `./gui/setup.sh` installs ALL dependencies including LLM and RAG packages.

---

### GUI Port Already in Use

**Error:**
```
Port 8501 is already in use
```

**Solutions:**

```bash
# Use different port
streamlit run gui/app.py --server.port 8502

# Or kill existing Streamlit
pkill -f streamlit

# Then run
./gui/launch.sh
```

---

### RAG Agent Errors

**Error:**
```
No module named 'sentence_transformers'
RAGError: Could not load embedding model
```

**Cause:** RAG support not installed (needed for document analysis)

**Solutions:**

```bash
# Option 1: Run GUI setup (recommended)
cd ~/AI-Agent-Builder
./gui/setup.sh  # Installs everything including sentence-transformers

# Option 2: Manual install
pip install sentence-transformers

# Option 3: Install all optional dependencies
pip install -e ".[all]"

# Verify
python3 -c "import sentence_transformers; print('✅ RAG support installed')"
```

**Note:** If you used `./gui/setup.sh`, sentence-transformers should already be installed.

---

### Agent File Not Found in GUI

**Error:**
```
Agent file not found in examples/
```

**Solutions:**

```bash
# Check file exists
ls -la examples/

# Agent files should be in examples/
# Not in gui/ or agent_framework/

# If saved in wrong location, move it:
mv gui/myagent.py examples/myagent.py
```

---

## Example Script Issues

### Import Errors in Examples

**Error:**
```
ImportError: cannot import name 'Agent' from 'agent_framework'
```

**Solutions:**

```bash
# 1. Make sure you're in project directory
cd ~/AI-Agent-Builder

# 2. Framework must be installed
pip install -e ".[all]"

# 3. Environment must be activated
conda activate agent-framework  # If conda
source venv/bin/activate        # If venv

# 4. Run from project root
python examples/01_basic.py  # ✅ Correct
cd examples && python 01_basic.py  # ❌ Wrong
```

---

### LLM Examples Fail with Fallback

**Behavior:**
```
⚠️ LLM unavailable, using fallback logic
```

**Not an error, but LLM isn't working. Causes:**

**1. Ollama not running:**
```bash
# Start Ollama
ollama serve  # In separate terminal

# Then run example again
python examples/02_llm_agent.py
```

**2. Model not downloaded:**
```bash
ollama pull llama3.2
python examples/02_llm_agent.py
```

**3. Package not installed:**
```bash
pip install -e ".[llm]"
python examples/02_llm_agent.py
```

---

## Docker Issues

### Docker Not Installed

**Error:**
```
docker: command not found
```

**Solutions:**

See [DATABASE_SETUP.md](DATABASE_SETUP.md) for Docker installation instructions.

**Quick install (Linux):**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
```

---

### Docker Daemon Not Running

**Error:**
```
Cannot connect to the Docker daemon
```

**Solutions:**

**Linux:**
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

**macOS/Windows:**
- Start Docker Desktop application
- Wait for whale icon to appear

---

### Docker Permission Denied

**Error:**
```
permission denied while trying to connect to the Docker daemon socket
```

**Solutions:**

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply changes
newgrp docker

# Or restart terminal

# Verify
docker ps
```

---

## Performance Issues

### Slow Database Queries

**Symptoms:**
- Queries take > 5 seconds
- Database timeouts

**Solutions:**

**1. Increase pool size (if many concurrent users):**
```bash
# Edit .env
DB_MAX_POOL_SIZE=20  # Default is 10
```

**2. Increase timeout:**
```bash
DB_COMMAND_TIMEOUT=120  # Default is 60 seconds
```

**3. Check Docker resources:**
```bash
# Give Docker more RAM/CPU in Docker Desktop settings
```

**4. Restart database:**
```bash
docker compose restart postgres
```

---

### Slow LLM Responses

**Symptoms:**
- LLM calls take > 10 seconds
- Timeouts

**Solutions:**

**Ollama (local):**
```bash
# Use smaller model
ollama pull phi  # 2GB instead of llama3.2 4GB

# Update agent to use phi
```

**OpenAI/Anthropic:**
```bash
# Use faster model
OPENAI_MODEL=gpt-3.5-turbo  # Instead of gpt-4

# Reduce max_tokens
OPENAI_MAX_TOKENS=500  # Instead of 1000
```

**Hybrid approach:**
```bash
# Use hybrid agents (filter with rules, then LLM)
python examples/03_hybrid.py
```

---

## Testing Issues

### pytest Not Found

**Error:**
```
pytest: command not found
```

**Solutions:**

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Or just pytest
pip install pytest pytest-asyncio

# Verify
pytest --version
```

---

### Tests Failing

**Error:**
```
FAILED tests/test_framework.py::test_agent
```

**Solutions:**

**1. Database must be running:**
```bash
docker compose up -d postgres
sleep 10
pytest tests/
```

**2. Use test database:**
```bash
# Tests use TEST_DATABASE_URL from .env
# Make sure it's different from production
cat .env | grep TEST_DATABASE_URL

# Should be:
TEST_DATABASE_URL=postgresql://postgres:postgres@localhost:5433/agent_framework_test
```

**3. Clean test database:**
```bash
# Drop and recreate test database
docker compose exec postgres psql -U postgres -c "DROP DATABASE IF EXISTS agent_framework_test;"
docker compose exec postgres psql -U postgres -c "CREATE DATABASE agent_framework_test;"
pytest tests/
```

---

## Platform-Specific Issues

### WSL2 (Windows)

**Issue: Docker not working in WSL2**

**Solutions:**
```bash
# Enable WSL2 integration in Docker Desktop
# Settings → Resources → WSL Integration → Enable for Ubuntu

# Verify
docker ps
```

**Issue: Port not accessible from Windows**

**Solutions:**
```bash
# Use WSL2 IP, not localhost
ip addr show eth0 | grep inet

# Or use localhost with port forwarding
# (Usually works automatically in WSL2)
```

---

### macOS

**Issue: ARM (M1/M2/M3) compatibility**

**Solutions:**
```bash
# Use ARM-compatible Miniconda
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
bash Miniconda3-latest-MacOSX-arm64.sh

# Or use native Python
brew install python@3.11
```

**Issue: Permission denied on scripts**

**Solutions:**
```bash
# Make scripts executable
chmod +x gui/setup.sh gui/launch.sh clean_all.sh
```

---

### Linux

**Issue: sudo required for Docker**

**Solutions:**
```bash
# Add user to docker group (one time)
sudo usermod -aG docker $USER
newgrp docker

# Verify (should work without sudo)
docker ps
```

---

## Environment Issues

### Wrong Python Version Active

**Problem:**
```bash
python --version  # Shows 3.8
# But need 3.10+
```

**Solutions:**

**Conda (best solution):**
```bash
conda create -n agent-framework python=3.11 -y
conda activate agent-framework
python --version  # Should show 3.11
```

**System Python:**
```bash
# Use python3.11 explicitly
python3.11 --version
python3.11 -m venv venv
source venv/bin/activate
```

---

### Virtual Environment Not Activating

**Problem:**
```bash
source venv/bin/activate
# Prompt doesn't change
```

**Solutions:**

**1. Check venv exists:**
```bash
ls -la venv/bin/activate  # Should exist

# If not, create it:
python3 -m venv venv
```

**2. Use full path:**
```bash
source ~/AI-Agent-Builder/venv/bin/activate
```

**3. Wrong shell:**
```bash
# For fish shell
source venv/bin/activate.fish

# For csh
source venv/bin/activate.csh
```

**4. Recreate venv:**
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -e ".[all]"
```

---

## Configuration Issues

### .env File Not Found

**Error:**
```
WARNING: .env file not found, using defaults
```

**Solutions:**

```bash
# Copy example
cp .env.example .env

# Verify
ls -la .env

# Edit if needed
nano .env
```

---

### Environment Variables Not Loaded

**Problem:**
Changes to .env don't take effect

**Solutions:**

**1. Restart Python script:**
```bash
# Ctrl+C to stop
# Run again
python examples/01_basic.py
```

**2. Check python-dotenv installed:**
```bash
pip install python-dotenv

# Or reinstall framework
pip install -e ".[all]"
```

**3. Manual load (for testing):**
```python
from dotenv import load_dotenv
load_dotenv()

import os
print(os.getenv('DB_PORT'))  # Should show your value
```

---

## Still Stuck?

### Get More Information

```bash
# Show full error traceback
python -v examples/01_basic.py

# Check all environment variables
env | grep -E "(DB_|OPENAI|ANTHROPIC|OLLAMA)"

# Check Docker logs
docker compose logs postgres

# Check system info
python3 --version
docker --version
pip list | grep agent-framework
```

---

### Where to Get Help

1. **Check documentation:**
   - [GETTING_STARTED.md](GETTING_STARTED.md) - Setup guide
   - [CONFIGURATION.md](CONFIGURATION.md) - Settings
   - [DATABASE_SETUP.md](DATABASE_SETUP.md) - Database help

2. **Search existing issues:**
   - [GitHub Issues](https://github.com/thesisai-hq/AI-Agent-Builder/issues)

3. **Open a new issue:**
   - Include error message (full traceback)
   - Include system info (OS, Python version)
   - Include steps to reproduce
   - **DO NOT** request financial advice

---

## Common Error Messages Quick Reference

| Error | Quick Fix |
|-------|-----------|
| `ModuleNotFoundError: agent_framework` | `pip install -e ".[all]"` |
| `ModuleNotFoundError: openai` | `pip install -e ".[llm]"` |
| `ConnectionError: database` | `docker compose up -d postgres` |
| `Port already in use` | Change `DB_PORT` in `.env` |
| `Model not found` | `ollama pull llama3.2` |
| `Invalid API key` | Add key to `.env` |
| `Permission denied` | Use venv or `--user` flag |
| `python: command not found` | Use `python3` |
| `Docker daemon not running` | Start Docker Desktop |
| `.env file not found` | `cp .env.example .env` |

---

**Remember:** Most issues are due to:
1. Environment not activated
2. Dependencies not installed
3. Database not running
4. LLM service not running

**Always check these first!** ✅
