# AI Agent Framework

> **Production-ready framework for building AI financial analysis agents**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 What Is This?

A lightweight, production-ready framework for building AI agents that analyze financial data. Built with maintainability and reliability in mind.

**Key Features:**
- 🐳 **Docker-first**: PostgreSQL setup in 30 seconds
- ✅ **Production-ready**: Comprehensive error handling, connection pooling, transactions
- 🧪 **Well-tested**: 85% test coverage with proper isolation
- 📚 **Type-safe**: Full Pydantic validation and type hints
- 🔌 **Flexible**: Optional LLM (OpenAI, Anthropic, Ollama) and RAG capabilities

## ⚡ Quick Start

```bash
# 1. Clone and install
git clone git@github.com:thesisai-hq/AI-Agent-Builder.git
cd AI-Agent-Builder
pip install -e .

# 2. Start PostgreSQL with Docker
docker-compose up -d postgres

# 3. Seed with sample data (4 tickers: AAPL, MSFT, TSLA, JPM)
python seed_data.py

# 4. Run your first agent
python examples/01_basic.py
```

**That's it!** You now have a working agent framework with real data.

## 📖 Examples

### Simple Agent (No LLM Required)

```python
from agent_framework import Agent, Signal, Config, Database

class ValueAgent(Agent):
    def analyze(self, ticker: str, data: dict) -> Signal:
        pe = data.get('pe_ratio', 0)
        if pe < 15:
            return Signal(
                direction='bullish',
                confidence=0.8,
                reasoning=f"PE {pe:.1f} indicates undervaluation"
            )
        return Signal(direction='neutral', confidence=0.5, reasoning='Fair value')

# Use it
async def main():
    db = Database(Config.get_database_url())
    await db.connect()
    
    agent = ValueAgent()
    data = await db.get_fundamentals('AAPL')
    signal = agent.analyze('AAPL', data)
    print(f"{signal.direction}: {signal.reasoning}")
    
    await db.disconnect()
```

### LLM Agent with Persona

```python
from agent_framework import Agent, AgentConfig, LLMConfig

class ConservativeInvestor(Agent):
    def __init__(self):
        config = AgentConfig(
            name="Conservative Investor",
            llm=LLMConfig(
                provider='ollama',  # or 'openai', 'anthropic'
                model='llama3.2',
                system_prompt="You are a conservative value investor..."
            )
        )
        super().__init__(config)
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        response = self.llm.chat(f"Analyze {ticker}: PE={data['pe_ratio']}")
        return parse_llm_signal(response)
```

See [examples/](examples/) for complete working examples.

## 🗄️ Database

**PostgreSQL** with asyncpg for high-performance async operations.

### Quick Setup (Docker)

```bash
docker-compose up -d postgres
python seed_data.py
```

### Features

- ✅ **Connection pooling**: 9x faster than new connections
- ✅ **Transactions**: ACID guarantees for atomic operations
- ✅ **Health checks**: Built-in monitoring
- ✅ **Sample data**: 4 tickers with 90 days of history + SEC filings

### Schema

- `fundamentals` - Company metrics (PE, revenue growth, margins, etc.)
- `prices` - Historical OHLCV data
- `news` - News headlines with sentiment
- `sec_filings` - SEC 10-K filing excerpts

## 🚀 API Server

Start the FastAPI server:

```bash
uvicorn agent_framework.api:app --reload
```

Visit http://localhost:8000/docs for interactive API documentation.

**Endpoints:**
- `GET /health` - System health check
- `GET /tickers` - List available tickers
- `GET /tickers/{ticker}` - Get complete ticker data
- `POST /analyze` - Run agent analysis

## 🧪 Testing

```bash
# Setup test database (one-time)
python setup_test_db.py

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=agent_framework
```

**Test coverage: ~85%**

## 🔌 Optional: LLM Setup

### Ollama (Local, Free)

```bash
curl https://ollama.ai/install.sh | sh
ollama pull llama3.2
```

### OpenAI

```bash
pip install openai
export OPENAI_API_KEY=sk-...
```

### Anthropic

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
```

## 📚 Documentation

- **[Installation Guide](docs/INSTALL.md)** - Detailed setup instructions
- **[Database Setup](docs/DATABASE_SETUP.md)** - PostgreSQL configuration
- **[Testing Guide](docs/TESTING.md)** - Writing and running tests
- **[Quick Reference](QUICK_REFERENCE.md)** - Common tasks cheat sheet

## 🎨 Architecture

```
agent_framework/
├── models.py       # Pydantic models with validation
├── agent.py        # Agent base class
├── database.py     # PostgreSQL with connection pooling
├── llm.py          # LLM client (OpenAI, Anthropic, Ollama)
├── rag.py          # RAG system for document analysis
├── api.py          # FastAPI REST API
├── config.py       # Configuration management
└── utils.py        # Shared utilities
```

**Design principles:**
- **Pydantic models** for runtime validation
- **Dependency injection** for testability
- **Comprehensive error handling** with custom exceptions
- **Lazy initialization** for optional features
- **Transaction support** for data consistency

## 💡 Use Cases

1. **Financial Analysis**: Build custom agents for stock analysis
2. **Research**: Use RAG to analyze SEC filings and reports
3. **Backtesting**: Test trading strategies with historical data
4. **API Service**: Deploy as a microservice for your applications

## 📋 Requirements

- Python 3.10+
- Docker (recommended) or PostgreSQL 12+
- 4GB RAM minimum (8GB for LLM)

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [asyncpg](https://github.com/MagicStack/asyncpg) - Fast PostgreSQL driver
- [PostgreSQL](https://www.postgresql.org/) - Reliable database

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-agent-framework/issues)
- **Documentation**: See [docs/](docs/) folder
- **Examples**: See [examples/](examples/) folder

---

**Version**: 1.0.0  
**Status**: Production Ready  
**Last Updated**: January 2025
