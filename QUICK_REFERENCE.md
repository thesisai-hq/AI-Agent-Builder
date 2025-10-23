# Quick Reference Guide

Fast reference for common tasks in the AI Agent Framework v2.0.

## 🚀 Quick Start

```bash
# 1. Install
git clone <repo> && cd AI-Agent-Builder
pip install -e .

# 2. Start database
docker-compose up -d postgres

# 3. Seed data
python seed_data.py

# 4. Verify
python quickstart.py
```

## 📦 Common Imports

```python
# Core
from agent_framework import Agent, Signal, Config

# Database
from agent_framework import Database, DatabaseError

# LLM
from agent_framework import LLMClient, LLMConfig, LLMError

# RAG
from agent_framework import RAGSystem, RAGConfig

# API
from agent_framework import api_app, register_agent_instance

# Utilities
from agent_framework import (
    parse_llm_signal,
    format_fundamentals,
    calculate_sentiment_score
)
```

## 🗄️ Database

### Connect and Use

```python
# Connect
db = Database(Config.get_database_url())
await db.connect()

try:
    # Query
    tickers = await db.list_tickers()
    data = await db.get_fundamentals('AAPL')
    prices = await db.get_prices('AAPL', days=30)
    news = await db.get_news('AAPL')
    filing = await db.get_filing('AAPL')
    
    # Health check
    healthy = await db.health_check()
    
finally:
    await db.disconnect()
```

### Transactions

```python
async with db.transaction() as conn:
    await conn.execute("INSERT INTO ...")
    await conn.execute("UPDATE ...")
    # Commits automatically
```

### Error Handling

```python
from agent_framework.database import QueryError, ConnectionError

try:
    data = await db.get_fundamentals('AAPL')
except QueryError as e:
    logger.error(f"Query failed: {e}")
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")
```

## 🤖 Simple Agent

```python
class MyAgent(Agent):
    def analyze(self, ticker: str, data: dict) -> Signal:
        pe = data.get('pe_ratio', 0)
        
        if pe < 15:
            return Signal('bullish', 0.8, 'Undervalued')
        elif pe > 30:
            return Signal('bearish', 0.7, 'Overvalued')
        else:
            return Signal('neutral', 0.5, 'Fair value')

# Use
agent = MyAgent()
signal = agent.analyze('AAPL', data)
```

## 💬 LLM Agent

```python
class LLMAgent(Agent):
    def __init__(self):
        config = AgentConfig(
            name="My LLM Agent",
            llm=LLMConfig(
                provider='ollama',  # or 'openai', 'anthropic'
                model='llama3.2',
                system_prompt="You are a conservative investor...",
                max_retries=3,
                temperature=0.7
            )
        )
        super().__init__(config)
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        prompt = format_fundamentals(data)
        response = self.llm.chat(f"Analyze {ticker}: {prompt}")
        return parse_llm_signal(response)

# Use
agent = LLMAgent()
signal = agent.analyze('AAPL', data)
```

## 📚 RAG Agent

```python
class RAGAgent(Agent):
    def __init__(self):
        config = AgentConfig(
            name="RAG Agent",
            rag=RAGConfig(
                chunk_size=300,
                chunk_overlap=50,
                top_k=3
            )
        )
        super().__init__(config)
    
    async def analyze_filing(self, ticker: str, filing: str):
        # Add document
        self.rag.add_document(filing)
        
        # Query
        context = self.rag.query("What are the risks?")
        
        # Analyze
        direction, confidence = calculate_sentiment_score(context)
        
        # Clean up
        self.rag.clear()
        
        return {'direction': direction, 'confidence': confidence}
```

## 🌐 API

### Start Server

```bash
# Development
uvicorn agent_framework.api:app --reload

# Production
uvicorn agent_framework.api:app --host 0.0.0.0 --port 8000
```

### Register Agent

```python
from agent_framework import register_agent_instance

agent = MyAgent()
register_agent_instance('my_agent', agent)
```

### Endpoints

```bash
# Health check
curl http://localhost:8000/health

# List tickers
curl http://localhost:8000/tickers

# Get ticker data
curl http://localhost:8000/tickers/AAPL

# Analyze
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "my_agent", "ticker": "AAPL"}'
```

## ⚙️ Configuration

### Environment Variables

```bash
# .env file
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/agent_framework
TEST_DATABASE_URL=postgresql://postgres:postgres@localhost:5433/agent_framework_test
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
OLLAMA_BASE_URL=http://localhost:11434
```

### Use Config Helper

```python
from agent_framework import Config

# Database
db_url = Config.get_database_url()
test_db_url = Config.get_test_database_url()

# LLM
openai_key = Config.get_llm_api_key('openai')
anthropic_key = Config.get_llm_api_key('anthropic')

# Ollama
ollama_url = Config.get_ollama_url()
```

## 🧪 Testing

### Run Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=agent_framework --cov-report=html

# Specific test
pytest tests/test_framework.py::TestDatabase -v

# Async tests
pytest tests/ -v --asyncio-mode=auto
```

### Test Fixture

```python
@pytest.fixture
async def test_db():
    db = Database(Config.get_test_database_url())
    await db.connect()
    yield db
    await db.disconnect()

@pytest.mark.asyncio
async def test_query(test_db):
    data = await test_db.get_fundamentals('AAPL')
    assert data is not None
```

## 🔧 Utilities

### Parse LLM Response

```python
from agent_framework import parse_llm_signal

response = "bullish|80|Strong growth"
signal = parse_llm_signal(response)
# Signal(direction='bullish', confidence=0.8, reasoning='Strong growth')
```

### Format Data for LLM

```python
from agent_framework import format_fundamentals

data = {'pe_ratio': 28.5, 'market_cap': 2800000000000}
formatted = format_fundamentals(data)
# "PE Ratio: 28.5\nMarket Cap: $2800.0B\n..."
```

### Calculate Sentiment

```python
from agent_framework import calculate_sentiment_score

text = "Strong growth and improved profits"
direction, confidence = calculate_sentiment_score(text)
# ('bullish', 0.65)
```

## 🐳 Docker

### PostgreSQL

```bash
# Start
docker-compose up -d postgres

# Stop
docker-compose down

# Logs
docker-compose logs postgres

# Access psql
docker exec -it agent_framework_db psql -U postgres -d agent_framework

# Backup
docker exec agent_framework_db pg_dump -U postgres agent_framework > backup.sql

# Restore
docker exec -i agent_framework_db psql -U postgres agent_framework < backup.sql
```

## 🔍 Debugging

### Enable Debug Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('agent_framework')
logger.setLevel(logging.DEBUG)
```

### Database Logs

```python
# Log all queries
import logging
logging.getLogger('asyncpg').setLevel(logging.DEBUG)
```

### API Logs

```bash
# Run with debug
uvicorn agent_framework.api:app --reload --log-level debug
```

## 📊 Monitoring

### Database Health

```python
# Check connection
healthy = await db.health_check()

# Pool stats (if needed)
if db._pool:
    print(f"Pool size: {db._pool.get_size()}")
    print(f"Idle: {db._pool.get_idle_size()}")
```

### API Health

```bash
curl http://localhost:8000/health
```

## 🚨 Common Errors

### Connection Refused

```bash
# Check Docker
docker ps

# Start database
docker-compose up -d postgres
```

### Import Error

```bash
# Reinstall
pip install -e .
```

### Database Empty

```bash
# Seed data
python seed_data.py
```

### Port in Use

```bash
# Change port in docker-compose.yml
ports:
  - "5434:5432"

# Update DATABASE_URL
DATABASE_URL=postgresql://postgres:postgres@localhost:5434/agent_framework
```

## 📝 Pydantic Models

### Signal

```python
Signal(
    direction='bullish',  # 'bullish', 'bearish', 'neutral'
    confidence=0.8,  # 0.0 to 1.0
    reasoning='Strong growth'  # Non-empty string
)
```

### LLMConfig

```python
LLMConfig(
    provider='ollama',  # 'openai', 'anthropic', 'ollama'
    model='llama3.2',
    api_key=None,  # Optional
    system_prompt="...",  # Optional
    max_retries=3,  # Default 3
    temperature=0.7  # Default 0.7
)
```

### RAGConfig

```python
RAGConfig(
    chunk_size=300,  # Default 500
    chunk_overlap=50,  # Default 50
    top_k=3  # Default 3
)
```

### DatabaseConfig

```python
DatabaseConfig(
    connection_string='postgresql://...',
    min_pool_size=2,  # Default 2
    max_pool_size=10,  # Default 10
    command_timeout=60  # Default 60
)
```

## 🎓 Best Practices

### 1. Always Use Config

```python
# Good
db_url = Config.get_database_url()

# Avoid
db_url = os.getenv('DATABASE_URL', '...')
```

### 2. Use Context Managers

```python
# Good
async with db.transaction() as conn:
    await conn.execute(...)

# Avoid
conn = await db._pool.acquire()
await conn.execute(...)
await db._pool.release(conn)
```

### 3. Handle Exceptions

```python
# Good
try:
    data = await db.get_fundamentals(ticker)
except QueryError as e:
    logger.error(f"Failed: {e}")
    # Handle error

# Avoid
data = await db.get_fundamentals(ticker)  # No error handling
```

### 4. Use Lazy Initialization

```python
# Good - LLM only created if needed
class Agent:
    @property
    def llm(self):
        if self._llm is None and self.config.llm:
            self._llm = LLMClient(self.config.llm)
        return self._llm
```

### 5. Clean Up Resources

```python
# Good
db = Database(Config.get_database_url())
await db.connect()
try:
    # Use database
finally:
    await db.disconnect()
```

## 🔗 Links

- **GitHub**: https://github.com/yourusername/ai-agent-framework
- **Documentation**: See docs/ folder
- **Examples**: See examples/ folder
- **Tests**: See tests/ folder

## 📚 Further Reading

- [README.md](README.md) - Overview and features
- [INSTALL.md](docs/INSTALL.md) - Installation guide
- [DATABASE_SETUP.md](docs/DATABASE_SETUP.md) - Database setup
- [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) - Architecture
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [IMPROVEMENTS_SUMMARY.md](IMPROVEMENTS_SUMMARY.md) - What's new in v2.0

---

**Version**: 2.0.0  
**Last Updated**: 2025-01-XX
