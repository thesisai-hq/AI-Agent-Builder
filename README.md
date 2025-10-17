# AI Agent Builder

> Multi-agent stock analysis system with LLM and RAG capabilities

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A flexible, production-ready framework for building AI-powered stock analysis agents with support for multiple LLM providers and RAG configurations.**

---

## 🎯 Features

### **Multi-Agent System**
- ✅ Flexible agent framework with decorator-based creation
- ✅ Agent registry for dynamic management
- ✅ Consensus calculation from multiple signals
- ✅ Built-in caching and performance optimization

### **LLM Integration**
- ✅ **Ollama** - Local inference (recommended for testing)
- ✅ **OpenAI** - GPT models (production-ready)
- ✅ **Anthropic** - Claude models (high quality)
- ✅ Unified interface across all providers

### **RAG (Retrieval-Augmented Generation)**
- ✅ **3 Embedding Options**: Simple hash, Sentence Transformers, Ollama
- ✅ **3 Vector Stores**: In-memory, ChromaDB, FAISS
- ✅ Semantic search through SEC filings
- ✅ Context-aware analysis with database integration

### **Infrastructure**
- ✅ PostgreSQL with connection pooling (50x faster)
- ✅ Docker containerization
- ✅ FastAPI with automatic OpenAPI docs
- ✅ Comprehensive mock database for testing
- ✅ Input validation and SQL injection prevention

---

## 🚀 Quick Start

See [QUICK_START.md](docs/QUICK_START.md) for detailed instructions.

```bash
# 1. Clone and setup
git clone <your-repo>
cd ai-agent-builder

# 2. Install core dependencies
pip install -r requirements.txt

# 3. Start PostgreSQL (Docker)
make start

# 4. Load mock data
make seed

# 5. Run API
python main.py
```

Visit: **http://localhost:8000/docs**

---

## 📁 Project Structure

```
ai-agent-builder/
├── agent_builder/           # Main package
│   ├── core/               # Config, database, security
│   │   ├── config.py       # Configuration management
│   │   ├── database.py     # Connection pooling
│   │   └── security.py     # Input validation
│   ├── agents/             # Agent system
│   │   ├── base.py         # Base classes
│   │   ├── context.py      # Data access
│   │   └── registry.py     # Agent management
│   ├── llm/                # LLM providers
│   │   ├── base.py         # Base interface
│   │   ├── providers.py    # Ollama, OpenAI, Anthropic
│   │   └── prompts.py      # Prompt templates
│   ├── rag/                # RAG system
│   │   ├── embeddings.py   # Embedding models
│   │   ├── vectorstores.py # Vector databases
│   │   ├── retriever.py    # Data retrieval
│   │   └── rag_engine.py   # RAG orchestration
│   └── api/                # FastAPI application
│       ├── app.py          # Application setup
│       └── routes.py       # API endpoints
├── examples/               # Example agents
│   ├── register_agents.py  # Simple test agents
│   ├── llm_agent_example.py # LLM-powered agents
│   └── rag_agents.py       # RAG-powered agents
├── database/               # Database setup
│   ├── mock_data.sql       # Mock data schema
│   └── setup_mock_db.py    # Database initialization
├── docker-compose.yml      # Docker configuration
├── Makefile               # Convenient commands
└── main.py                # Entry point
```

---

## 🤖 Creating Agents

### **Simple Agent**
```python
from agent_builder import agent

@agent("PE Ratio Analyzer", "Analyzes P/E ratios")
def pe_agent(ticker, context):
    pe = context.get_fundamental("pe_ratio")
    
    if pe < 15:
        return "bullish", 0.8, "Low P/E indicates value"
    elif pe > 30:
        return "bearish", 0.7, "High P/E suggests overvaluation"
    
    return "neutral", 0.5, f"Average P/E: {pe}"

# Register
from agent_builder import get_registry
registry = get_registry()
registry.register(pe_agent.agent, weight=1.2, tags=["fundamental"])
```

### **LLM-Powered Agent**
```python
from agent_builder.llm import get_llm_provider, PromptTemplates

@agent("LLM Analyzer", "Uses AI for analysis")
def llm_agent(ticker, context):
    llm = get_llm_provider("ollama")
    
    fundamentals = context.get_fundamentals()
    prompt = PromptTemplates.fundamental_analysis(ticker, fundamentals)
    
    response = llm.generate(prompt, temperature=0.3)
    parsed = PromptTemplates.parse_llm_response(response.content)
    
    return parsed["signal"], parsed["confidence"], parsed["reasoning"]
```

### **RAG-Powered Agent**
```python
from agent_builder.rag import RAGEngine

@agent("RAG Analyzer", "Uses RAG for context-aware analysis")
def rag_agent(ticker, context):
    # Create RAG engine
    rag = RAGEngine(
        db=context.db,
        embedding="sentence-transformers",
        vectorstore="chroma"
    )
    
    # Index and search SEC filings
    rag.index_sec_filings(ticker)
    rag_context = rag.get_relevant_context(ticker, "growth strategy")
    
    # Use context in LLM
    llm = get_llm_provider("ollama")
    response = llm.generate(f"{rag_context}\n\nAnalyze {ticker}.")
    
    # Parse and return
    parsed = PromptTemplates.parse_llm_response(response.content)
    return parsed["signal"], parsed["confidence"], parsed["reasoning"]
```

---

## 🌐 API Usage

### **Run Analysis**
```bash
POST /analyze
{
  "ticker": "AAPL",
  "agent_ids": ["pe_ratio_agent", "llm_analyzer"]  # optional
}

Response:
{
  "analysis_id": "abc-123",
  "status": "pending"
}
```

### **Get Results**
```bash
GET /analyze/{analysis_id}

Response:
{
  "ticker": "AAPL",
  "status": "completed",
  "signals": [
    {
      "agent_name": "PE Ratio Analyzer",
      "signal_type": "bullish",
      "confidence": 0.8,
      "reasoning": "Low P/E indicates value"
    }
  ],
  "consensus": {
    "signal": "bullish",
    "confidence": 0.75,
    "agreement": 0.88
  }
}
```

### **Manage Agents**
```bash
GET /agents                    # List all agents
POST /agents/{id}/enable       # Enable agent
POST /agents/{id}/disable      # Disable agent
```

---

## 🐳 Docker Commands

```bash
make start      # Start PostgreSQL
make stop       # Stop database
make shell      # Open database shell
make logs       # View logs
make seed       # Load mock data
make test       # Test connection
make backup     # Backup database
make clean      # Remove containers
```

---

## 🎓 Configuration

### **Environment Variables** (`.env`)
```bash
# Database
DATABASE_URL=postgresql://agent_user:agent_password@localhost:5432/agentbuilder

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# LLM Provider (choose one)
LLM_PROVIDER=ollama              # or "openai" or "anthropic"
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# OpenAI (if using)
# OPENAI_API_KEY=sk-...
# OPENAI_MODEL=gpt-4

# Anthropic (if using)
# ANTHROPIC_API_KEY=sk-ant-...
# ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

### **RAG Configuration**
```python
# In your agent code - choose embedding and vector store
rag = RAGEngine(
    db=context.db,
    embedding="sentence-transformers",  # or "simple" or "ollama"
    vectorstore="chroma"                # or "memory" or "faiss"
)
```

---

## 📊 Mock Database

Includes test data for **5 stocks**: AAPL, TSLA, MSFT, GOOGL, NVDA

**Tables:**
- `mock_fundamentals` - Financial metrics (P/E, ROE, margins, etc.)
- `mock_prices` - Historical OHLCV + technical indicators
- `mock_news` - News articles with sentiment scores
- `mock_analyst_ratings` - Buy/sell ratings from major firms
- `mock_insider_trades` - Insider buying/selling activity
- `mock_sec_filings` - 10-K/10-Q filings with full text
- `mock_options` - Options data for volatility analysis
- `mock_macro_indicators` - Economic indicators (Fed rate, GDP, VIX)

---

## 🧪 Testing

```bash
# Test database
make test

# Test agents directly
python examples/register_agents.py

# Test LLM agents
python examples/llm_agent_example.py

# Test RAG agents
python examples/rag_agents.py

# Test API
python main.py
curl http://localhost:8000/health
```

---

## 🎯 RAG Options Comparison

| Configuration | Quality | Speed | Setup | Persistent |
|---------------|---------|-------|-------|------------|
| simple + memory | ⭐ | ⚡⚡⚡ | 0 min | ❌ |
| ST + chroma | ⭐⭐⭐⭐⭐ | ⚡⚡ | 5 min | ✅ |
| ST + faiss | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ | 5 min | Manual |
| ollama + chroma | ⭐⭐⭐⭐ | ⚡ | 10 min | ✅ |

*ST = sentence-transformers*

**Recommended:** sentence-transformers + ChromaDB

---

## 🔧 Troubleshooting

### **Database won't start**
```bash
make clean
make start
```

### **Port 5432 in use**
```bash
# Stop local PostgreSQL
sudo systemctl stop postgresql
# or change port in docker-compose.yml
```

### **Ollama not connecting**
```bash
# Start Ollama
ollama serve

# Pull model
ollama pull llama3.2

# Test
ollama run llama3.2 "Hello"
```

### **Module not found errors**
```bash
# Install in development mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### **RAG dependencies missing**
```bash
# Check what's installed
pip list | grep -E "sentence|chroma|faiss"

# Install recommended setup
pip install sentence-transformers chromadb
```

See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for more.

---

## 📚 Documentation

- **API Docs**: http://localhost:8000/docs (when running)
- **ReDoc**: http://localhost:8000/redoc
- **Quick Start**: [QUICK_START.md](docs/QUICK_START.md)
- **RAG Guide**: [RAG_USAGE.md](docs/RAG_USAGE.md)
- **Docker Guide**: [DOCKER_README.md](docs/DOCKER_README.md)

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    FastAPI Application                    │
│  ┌────────────────────────────────────────────────────┐  │
│  │  POST /analyze  →  Background Task  →  Consensus  │  │
│  └────────────────────────────────────────────────────┘  │
└───────────────────────┬──────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│    Agent     │ │    Agent     │ │    Agent     │
│   Registry   │ │   Context    │ │   Signals    │
└──────┬───────┘ └──────┬───────┘ └──────────────┘
       │                │
       ▼                ▼
┌──────────────────────────────────┐
│      Database (PostgreSQL)        │
│    Connection Pool (2-10 conns)   │
│  ┌────────────────────────────┐  │
│  │  Mock Data for 5 Stocks    │  │
│  │  - Fundamentals            │  │
│  │  - Prices + Indicators     │  │
│  │  - News + Sentiment        │  │
│  │  - SEC Filings             │  │
│  │  - Options + Macro         │  │
│  └────────────────────────────┘  │
└──────────────────────────────────┘

Optional Extensions:
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│     LLM      │  │     RAG      │  │  Sentiment   │
│  - Ollama    │  │ - Embeddings │  │   - VADER    │
│  - OpenAI    │  │ - VectorDB   │  │   - FinBERT  │
│  - Claude    │  │ - Retrieval  │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
```

---

## 💻 Development

### **Running Locally**
```bash
# Start database
make start

# Install dependencies
pip install -e .

# Run API (hot reload)
uvicorn agent_builder.api.app:app --reload

# Or
python main.py
```

### **Running in Docker**
```bash
# Full stack (API + DB)
docker-compose -f docker-compose.full.yml up

# Database only
docker-compose up -d postgres
```

### **Code Quality**
```bash
# Format code
black .

# Lint
flake8 agent_builder/

# Type check
mypy agent_builder/
```

---

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/

# With coverage
pytest --cov=agent_builder tests/
```

---

## 📈 Performance

- **Connection Pooling**: 50x faster than creating new connections
- **Agent Caching**: Caches fundamental data per analysis
- **Background Processing**: Non-blocking analysis execution
- **Optimized Queries**: Indexed tables for fast retrieval

**Benchmarks** (5 agents analyzing AAPL):
- Cold start: ~2 seconds
- Warm (cached): ~500ms
- Database query: ~5ms (with pooling)

---

## 🔐 Security

- ✅ Input validation (ticker, agent IDs)
- ✅ SQL injection prevention (table whitelist)
- ✅ Parameterized queries
- ✅ CORS configuration
- ✅ Environment-based secrets

---

## 📦 Dependencies

### **Core** (Required)
```
fastapi, uvicorn, pydantic, psycopg2-binary, python-dotenv, requests
```

### **RAG** (Optional - Recommended)
```
sentence-transformers, chromadb
```

### **Performance** (Optional)
```
faiss-cpu, numpy
```

See [requirements.txt](requirements.txt) for complete list.

---

## 🛠️ Extending the System

### **Add a Custom Agent**
```python
from agent_builder import agent, get_registry

@agent("My Custom Agent", "Description")
def my_agent(ticker, context):
    # Your analysis logic
    data = context.get_fundamental("pe_ratio")
    return "bullish", 0.8, "Your reasoning"

registry = get_registry()
registry.register(my_agent.agent, weight=1.0)
```

### **Add a Custom Data Source**
```python
# In agent_builder/agents/context.py
class AgentContext:
    def get_custom_data(self, ticker):
        return self.db.execute(
            "SELECT * FROM my_custom_table WHERE ticker = %s",
            (ticker,)
        )
```

### **Add a Custom LLM Provider**
```python
# In agent_builder/llm/providers.py
class MyLLMProvider(BaseLLMProvider):
    def generate(self, prompt, **kwargs):
        # Your implementation
        pass
```

---

## 🌍 Production Deployment

### **Environment Setup**
1. Set production DATABASE_URL
2. Configure CORS origins
3. Set DEBUG=false
4. Use production-grade secrets management

### **Scaling**
- Increase database connection pool size
- Use Redis for caching (future enhancement)
- Deploy multiple API instances behind load balancer
- Use managed vector database (Pinecone, Weaviate)

### **Monitoring**
- Enable logging to file
- Add metrics endpoint
- Monitor database connection pool
- Track LLM token usage

---

## 📄 License

MIT License - See [LICENSE](docs/LICENSE) file

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-agent`)
3. Commit changes (`git commit -m 'Add amazing agent'`)
4. Push to branch (`git push origin feature/amazing-agent`)
5. Open Pull Request

---

## 🆘 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Documentation**: [docs/](docs/)

---

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Sentence Transformers for semantic embeddings
- ChromaDB for easy vector storage
- Ollama for local LLM inference
- PostgreSQL for reliable data storage

---

## 📊 Roadmap

- [x] Multi-agent framework
- [x] LLM integration (Ollama, OpenAI, Claude)
- [x] RAG system with multiple backends
- [x] Docker containerization
- [x] Mock database for testing
- [ ] Real-time data integration
- [ ] Backtesting framework
- [ ] Portfolio optimization
- [ ] Web dashboard
- [ ] Agent performance metrics
- [ ] A/B testing for agents

---

**Built with ❤️ for intelligent stock analysis**

---
