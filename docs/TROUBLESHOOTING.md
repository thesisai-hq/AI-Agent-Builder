# Troubleshooting Guide

Quick solutions to common issues.

---

## 🐛 Common Errors

### **1. "ModuleNotFoundError: No module named 'agent_builder'"**

**Cause:** Python can't find the package

**Solutions:**
```bash
# A. Install in development mode (recommended)
pip install -e .

# B. Add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# C. Run as module
python -m examples.register_agents
```

**Verify:**
```bash
python -c "import agent_builder; print('✅ OK')"
```

---

### **2. "KeyError: 'ContainerConfig'" (Docker)**

**Cause:** Old Docker Compose version with corrupted container

**Solution:**
```bash
# Clean everything
docker-compose down --remove-orphans
docker rm -f $(docker ps -aq --filter name=agent) 2>/dev/null || true

# Start fresh
make start

# Or use simple Docker (no compose)
./docker_simple.sh
```

---

### **3. "Database connection failed"**

**Cause:** PostgreSQL not running or wrong connection string

**Check:**
```bash
# Is database running?
docker ps | grep agentbuilder_db

# Test connection
make test

# View logs
make logs
```

**Fix:**
```bash
# Restart database
make restart

# Check .env file
cat .env | grep DATABASE_URL
# Should be: postgresql://agent_user:agent_password@localhost:5432/agentbuilder

# Test from command line
docker exec agentbuilder_db psql -U agent_user -d agentbuilder -c "SELECT 1"
```

---

### **4. "Port 5432 already in use"**

**Cause:** Another PostgreSQL instance running

**Solution A: Stop local PostgreSQL**
```bash
# Linux
sudo systemctl stop postgresql

# macOS
brew services stop postgresql

# Windows
net stop postgresql-x64-15
```

**Solution B: Change port**

In `docker-compose.yml`:
```yaml
ports:
  - "5433:5432"  # Use 5433 instead
```

Then update `.env`:
```bash
DATABASE_URL=postgresql://agent_user:agent_password@localhost:5433/agentbuilder
```

---

### **5. "Ollama connection refused"**

**Cause:** Ollama server not running

**Fix:**
```bash
# Start Ollama
ollama serve

# In another terminal
ollama pull llama3.2

# Test
ollama run llama3.2 "Hello"

# Verify from Python
python -c "import requests; r=requests.get('http://localhost:11434/api/tags'); print('✅ OK' if r.status_code==200 else '❌ Error')"
```

---

### **6. "No data returned from database"**

**Cause:** Mock data not loaded

**Fix:**
```bash
# Check if tables exist
make shell
\dt
\q

# Load data
make seed

# Verify data
make shell
SELECT COUNT(*) FROM mock_fundamentals;
SELECT ticker FROM mock_fundamentals;
\q
```

---

### **7. "Analysis stays in 'pending' status"**

**Cause:** Background task failed, check logs

**Debug:**
```bash
# Check API logs (terminal where python main.py is running)
# Look for errors like:
# ERROR: Agent xyz failed: ...

# Test agents manually
python examples/register_agents.py

# Check database
make shell
SELECT * FROM analyses ORDER BY created_at DESC LIMIT 1;
\q
```

---

### **8. "sentence-transformers import error"**

**Cause:** Missing dependencies or incompatible versions

**Fix:**
```bash
# Uninstall and reinstall
pip uninstall sentence-transformers -y
pip install sentence-transformers==2.2.2

# Or install with dependencies
pip install sentence-transformers[training]

# Check
python -c "from sentence_transformers import SentenceTransformer; print('✅ OK')"
```

---

### **9. "ChromaDB SQLite error"**

**Cause:** ChromaDB using old SQLite version

**Fix:**
```bash
# Upgrade pysqlite3
pip install pysqlite3-binary

# Or use in-memory mode
# In your code:
import chromadb
client = chromadb.Client()  # Uses in-memory instead of persistent
```

---

### **10. "FAISS import error"**

**Cause:** Wrong FAISS package or missing numpy

**Fix:**
```bash
# Install both together
pip install faiss-cpu numpy

# Verify
python -c "import faiss; import numpy; print('✅ OK')"

# If still fails, try:
pip install --upgrade faiss-cpu numpy
```

---

## 🔧 Diagnostic Commands

### **Check System Status**
```bash
# Database
make status
make test

# Python packages
pip list | grep -E "fastapi|pydantic|psycopg2|sentence|chroma|faiss"

# Ollama
curl http://localhost:11434/api/tags

# API
curl http://localhost:8000/health
```

### **View Logs**
```bash
# Database logs
make logs

# API logs
# (View terminal where python main.py is running)

# Docker logs
docker logs agentbuilder_db
```

### **Database Inspection**
```bash
# Open shell
make shell

# List tables
\dt

# Check table contents
SELECT COUNT(*) FROM mock_fundamentals;
SELECT * FROM mock_fundamentals WHERE ticker = 'AAPL';

# Check analyses
SELECT id, ticker, status FROM analyses ORDER BY created_at DESC LIMIT 5;

# Exit
\q
```

---

## 🔄 Reset Procedures

### **Soft Reset (Keep data)**
```bash
# Restart services
make restart
python main.py
```

### **Hard Reset (Fresh start)**
```bash
# Stop everything
make stop

# Remove containers
make clean

# Start fresh
make start
make seed
python main.py
```

### **Nuclear Reset (Everything)**
```bash
# Delete all data and containers
make clean-all

# Remove Python cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null

# Reinstall
pip install -e .

# Rebuild
make start
make seed
python main.py
```

---

## 🧪 Testing Checklist

Run through this checklist if something's not working:

```bash
# 1. Python version
python --version  # Should be 3.8+

# 2. Virtual environment active
which python  # Should point to venv

# 3. Package installed
python -c "import agent_builder"  # Should not error

# 4. Database running
docker ps | grep agentbuilder_db  # Should show running

# 5. Database accessible
make test  # Should show "OK"

# 6. Data loaded
make shell
SELECT COUNT(*) FROM mock_fundamentals;  # Should show 5
\q

# 7. Ollama running (if using LLM)
curl http://localhost:11434/api/tags  # Should return JSON

# 8. API starts
python main.py  # Should show "Starting API..."

# 9. API accessible
curl http://localhost:8000/health  # Should return JSON

# 10. Analysis works
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL"}'
```

---

## 💡 Performance Issues

### **Slow Database Queries**
```bash
# Check connection pool
# In logs, look for: "Database pool initialized (2-10 connections)"

# Increase pool size in .env
DB_MIN_CONN=5
DB_MAX_CONN=20
```

### **Slow LLM Responses**
```python
# First Ollama request is slow (model loading)
# Subsequent requests are fast

# Preload model at startup
llm = get_llm_provider("ollama")
llm.generate("warmup", max_tokens=5)  # Loads model
```

### **Slow RAG Indexing**
```bash
# Use FAISS instead of ChromaDB for speed
pip install faiss-cpu

# In agent:
rag = RAGEngine(db, embedding="sentence-transformers", vectorstore="faiss")
```

---

## 🆘 Still Stuck?

### **Get Detailed Error Info**
```bash
# Run with debug mode
DEBUG=true python main.py

# Check full traceback
python -c "
from agent_builder.core.config import Config
from agent_builder.core.database import DatabasePool
config = Config.from_env()
pool = DatabasePool(config.database)
"
```

### **Clean Environment Test**
```bash
# Create fresh environment
python -m venv test_env
source test_env/bin/activate

# Install only core
pip install fastapi uvicorn pydantic psycopg2-binary python-dotenv requests

# Test import
python -c "import fastapi; print('✅ OK')"
```

### **Common Gotchas**

1. **Wrong directory**: Run commands from project root
2. **Virtual env not activated**: `source venv/bin/activate`
3. **Old .pyc files**: `find . -name "*.pyc" -delete`
4. **Port conflicts**: Check with `lsof -i :8000` and `lsof -i :5432`
5. **Environment variables**: `printenv | grep -E "DATABASE|OLLAMA"`

---

## 📞 Getting Help

1. **Check logs first**: Most errors show in terminal/logs
2. **Test components individually**: Database → Agents → API
3. **Use diagnostic commands**: `make test`, `make status`
4. **Review documentation**: README.md, QUICK_START.md
5. **Create minimal reproduction**: Isolate the failing component

---

## ✅ Verification Script

Save as `verify_setup.py`:
```python
#!/usr/bin/env python
"""Verify system setup"""

import sys

print("=" * 70)
print("SYSTEM VERIFICATION")
print("=" * 70)

checks = []

# Python version
if sys.version_info >= (3, 8):
    print("✅ Python 3.8+")
    checks.append(True)
else:
    print(f"❌ Python {sys.version_info.major}.{sys.version_info.minor} (need 3.8+)")
    checks.append(False)

# Core packages
try:
    import fastapi
    print("✅ FastAPI")
    checks.append(True)
except ImportError:
    print("❌ FastAPI (pip install fastapi)")
    checks.append(False)

try:
    import psycopg2
    print("✅ PostgreSQL driver")
    checks.append(True)
except ImportError:
    print("❌ psycopg2 (pip install psycopg2-binary)")
    checks.append(False)

# Optional packages
try:
    import sentence_transformers
    print("✅ Sentence Transformers (RAG available)")
except ImportError:
    print("⚠️  Sentence Transformers not installed (RAG will use simple embeddings)")

try:
    import chromadb
    print("✅ ChromaDB (Persistent vector store)")
except ImportError:
    print("⚠️  ChromaDB not installed (Will use in-memory store)")

# Package import
try:
    import agent_builder
    print("✅ agent_builder package")
    checks.append(True)
except ImportError:
    print("❌ agent_builder (run: pip install -e .)")
    checks.append(False)

# Database connection
try:
    import requests
    r = requests.get("http://localhost:11434/api/tags", timeout=2)
    if r.status_code == 200:
        print("✅ Ollama running")
except:
    print("⚠️  Ollama not running (optional for LLM features)")

print("\n" + "=" * 70)
if all(checks):
    print("✅ ALL REQUIRED COMPONENTS READY!")
    print("=" * 70)
    print("\n📝 Next: python main.py")
else:
    print("❌ SOME COMPONENTS MISSING")
    print("=" * 70)
    print("\n📝 Fix issues above, then retry")

print()
```

Run it:
```bash
python verify_setup.py
```

---

**You now have:**
- ✅ Complete README.md
- ✅ QUICK_START.md
- ✅ TROUBLESHOOTING.md
- ✅ requirements.txt
- ✅ Verification script

Everything you need to get started and debug issues! 🎉