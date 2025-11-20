# Project Structure

## Directory Layout

```
AI-Agent-Builder/
├── agent_framework/          # Core package
│   ├── __init__.py          # Public API exports
│   ├── models.py            # Pydantic models
│   ├── agent.py             # Agent base class
│   ├── database.py          # PostgreSQL client
│   ├── llm.py               # LLM client (OpenAI, Anthropic, Ollama)
│   ├── rag.py               # RAG system
│   ├── confidence.py        # Enhanced confidence calculations
│   ├── api.py               # FastAPI server
│   ├── config.py            # Configuration management
│   └── utils.py             # Shared utilities
│
├── examples/                 # Working examples
│   ├── README.md            # Examples guide
│   ├── 01_basic.py          # Rule-based agents
│   ├── 02_llm_agent.py      # LLM-powered agents
│   ├── 03_hybrid.py         # Hybrid agents (rules + LLM)
│   ├── 04_rag_agent.py      # RAG document analysis
│   ├── 05_buffett_quality.py # Warren Buffett strategy
│   ├── 06_lynch_garp.py      # Peter Lynch GARP
│   ├── 07_graham_value.py    # Benjamin Graham value
│   └── myagent.py           # Template/playground file
│
├── tests/                    # Test suite
│   ├── README.md            # Testing guide
│   ├── test_framework.py    # Framework tests
│   └── conftest.py          # Shared fixtures (optional)
│
├── gui/                      # Visual interface (Streamlit)
│   ├── app.py               # Main GUI application
│   ├── agent_creator.py     # Visual agent builder
│   ├── agent_tester.py      # Testing interface
│   ├── agent_loader.py      # Agent file management
│   ├── code_viewer.py       # Educational code viewer
│   ├── llm_setup_wizard.py  # LLM setup wizard
│   ├── metrics.py           # Metric definitions
│   ├── requirements.txt     # GUI dependencies
│   ├── setup.sh             # GUI setup script (Linux/Mac)
│   └── launch.sh            # GUI launcher (Linux/Mac)
│
├── docs/                     # Documentation
│   ├── FRAMEWORK_QUICKSTART.md  # Framework quick start (developers)
│   ├── API_REFERENCE.md         # Complete API documentation
│   ├── GETTING_STARTED.md       # Installation & setup (all methods)
│   ├── CONFIGURATION.md         # Environment configuration
│   ├── DATABASE_SETUP.md        # Database setup guide
│   ├── LLM_CUSTOMIZATION.md     # LLM configuration
│   ├── CHOOSING_AGENT_TYPE.md   # Agent type comparison
│   ├── AGENT_FILE_GUIDELINES.md # File organization best practices
│   ├── HYBRID_AGENTS.md         # Hybrid agent guide
│   ├── UNIVERSITY_SETUP.md      # Classroom deployment
│   ├── TROUBLESHOOTING.md       # Common issues
│   ├── OLLAMA_SETUP.md          # Ollama installation
│   └── PROJECT_STRUCTURE.md     # This file
│
├── install.sh                # One-command installer (Linux/macOS/WSL2)
├── install.bat               # One-command installer (Windows)
├── docker-compose.yml        # PostgreSQL setup
├── schema.sql                # Database schema
├── seed_data.py              # Sample data seeding
├── setup_test_db.py          # Test database setup
├── quickstart.py             # Installation verification script
├── pyproject.toml            # Package configuration (PEP 621)
├── .env.example              # Configuration template
├── .gitignore                # Git ignore patterns
├── README.md                 # Main documentation (dual-audience)
├── GUI_QUICK_START.md        # GUI user quick start
├── THESIS_APP.md             # Production platform info (coming soon)
├── DISCLAIMER.md             # Legal disclaimer
├── CONTRIBUTING.md           # Contribution guidelines
├── CHANGELOG.md              # Version history
└── LICENSE                   # MIT License
```

---

## Core Modules

### models.py
Pydantic models with validation:
- `Signal` - Trading signal (immutable)
- `LLMConfig` - LLM configuration with smart defaults
- `RAGConfig` - RAG configuration with validation
- `AgentConfig` - Complete agent configuration
- `DatabaseConfig` - Database configuration with pool settings

### agent.py
Base agent class with lazy initialization:
- Abstract `analyze()` method (must implement)
- Lazy LLM client (`self.llm` property)
- Lazy RAG system (`self.rag` property)
- Simple, extensible design

### database.py
PostgreSQL client with connection pooling:
- Connection pooling (2-10 connections, 9x faster)
- Transaction support
- Comprehensive error handling
- Health checks
- Methods: get_fundamentals, get_prices, get_news, get_filing, list_tickers

### llm.py
Unified LLM interface:
- Supports: OpenAI, Anthropic, Ollama
- Automatic retries with exponential backoff
- System prompts for agent personas
- Error handling (LLMError, APIError, RateLimitError)
- Temperature and max_tokens configuration

### rag.py
Document retrieval and analysis:
- Text chunking with overlap
- Semantic search using sentence-transformers
- Query interface for retrieval
- In-memory storage (educational use)

### confidence.py
Enhanced confidence calculations:
- `ConfidenceCalculator` - Distance-based scoring
- `EnhancedConfidenceCalculator` - Multi-factor analysis
- Data quality adjustments
- LLM response validation

### api.py
FastAPI REST server:
- Health endpoints
- Data endpoints (tickers, fundamentals, prices)
- Analysis endpoints
- Agent registration
- Dependency injection
- CORS configuration

### config.py
Centralized configuration:
- Environment variable helpers
- Database URL construction
- LLM provider settings
- RAG configuration
- All settings from .env file

### utils.py
Shared utilities:
- `parse_llm_signal()` - Parse LLM formatted responses
- `format_fundamentals()` - Format data for LLM prompts
- `calculate_sentiment_score()` - VADER sentiment analysis with fallback

---

## Code Size

```
Core package:      ~1,500 lines (added confidence.py)
Examples:          ~800 lines (7 strategies + README)
Tests:             ~300 lines
GUI:               ~2,000 lines
Total:             ~4,600 lines
```

Compact, maintainable codebase.

---

## Design Principles

1. **Pydantic validation** - Runtime type checking, immutable models
2. **Dependency injection** - No singletons, fully testable
3. **Lazy initialization** - Load LLM/RAG only when needed
4. **Error handling** - Comprehensive exception hierarchy
5. **Connection pooling** - 9x database performance
6. **Async operations** - Non-blocking I/O for scalability
7. **Type hints** - 100% type coverage for IDE support
8. **One agent per file** - Clear organization

---

## Adding Components

### New Agent

```python
# examples/my_agent.py
from agent_framework import Agent, Signal

class MyAgent(Agent):
    async def analyze(self, ticker, data):
        # Your logic
        return Signal('bullish', 0.8, 'Custom logic')
```

---

### New Database Method

```python
# agent_framework/database.py
async def get_custom_data(self, ticker):
    async with self.acquire() as conn:
        return await conn.fetch("SELECT ... WHERE ticker = $1", ticker)
```

---

### New API Endpoint

```python
# agent_framework/api.py
@app.get("/custom")
async def custom_endpoint(db: Database = Depends(get_db)):
    return await db.get_custom_data()
```

---

### New Utility Function

```python
# agent_framework/utils.py
def custom_utility(data: dict) -> dict:
    """Process data in custom way."""
    return processed_data
```

---

## Import Patterns

```python
# Core
from agent_framework import Agent, Signal, Config

# Database
from agent_framework import Database, DatabaseConfig

# LLM
from agent_framework import LLMConfig, LLMClient

# RAG
from agent_framework import RAGConfig, RAGSystem

# API
from agent_framework import api_app, register_agent_instance

# Utils
from agent_framework import (
    parse_llm_signal,
    format_fundamentals,
    calculate_sentiment_score
)

# Confidence
from agent_framework import (
    ConfidenceCalculator,
    EnhancedConfidenceCalculator
)

# Exceptions
from agent_framework import (
    DatabaseError,
    LLMError,
    RAGError
)
```

---

## File Conventions

- **Classes**: PascalCase (`ValueAgent`, `LLMConfig`)
- **Functions**: snake_case (`get_fundamentals`, `parse_llm_signal`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_RETRIES`)
- **Private**: _leading_underscore (`_llm`, `_rag`)
- **Line limit**: 88-100 characters (Black formatter)
- **Type hints**: Required for all public APIs
- **Docstrings**: Required for all public functions
- **One agent per file**: examples/ organization rule

---

## Testing Structure

```
tests/
├── README.md             # Testing guide (pytest usage)
├── test_framework.py     # Core framework tests
└── conftest.py           # Shared fixtures (optional)
```

**Test coverage:** ~85%  
**Test framework:** pytest + pytest-asyncio

**Run tests:**
```bash
pytest tests/ -v --cov=agent_framework
```

---

## Documentation Structure

```
docs/
├── FRAMEWORK_QUICKSTART.md  # For developers (code-first)
├── API_REFERENCE.md         # Complete API reference
├── GETTING_STARTED.md       # Comprehensive installation
├── CONFIGURATION.md         # Environment variables
├── DATABASE_SETUP.md        # Database guide
├── LLM_CUSTOMIZATION.md     # AI configuration
├── CHOOSING_AGENT_TYPE.md   # Agent type comparison
├── AGENT_FILE_GUIDELINES.md # Organization best practices
├── HYBRID_AGENTS.md         # Hybrid strategies
├── UNIVERSITY_SETUP.md      # Educational deployment
├── TROUBLESHOOTING.md       # Common issues
├── OLLAMA_SETUP.md          # Ollama setup
└── PROJECT_STRUCTURE.md     # This file
```

**Root documentation:**
- `README.md` - Dual-audience overview
- `GUI_QUICK_START.md` - Visual interface guide
- `THESIS_APP.md` - Production platform info

Minimal, focused, well-organized documentation.

---

## Dependencies

### Core (Required)
```
fastapi>=0.104.0          # REST API
uvicorn[standard]>=0.24.0 # ASGI server
pydantic>=2.5.0           # Data validation
asyncpg>=0.29.0           # PostgreSQL driver
numpy>=1.24.0             # Numerical operations
python-dotenv>=1.0.0      # Environment loading
vaderSentiment>=3.3.2     # Sentiment analysis
```

### Optional - LLM
```
openai>=1.3.0             # OpenAI API
anthropic>=0.7.0          # Anthropic API
ollama>=0.1.0             # Ollama client
```

### Optional - RAG
```
sentence-transformers>=2.2.0  # Embeddings
```

### Optional - Development
```
pytest>=7.4.0             # Testing
pytest-asyncio>=0.21.0    # Async tests
pytest-cov>=4.1.0         # Coverage
black>=23.11.0            # Formatting
ruff>=0.1.0               # Linting
```

**Install all:**
```bash
pip install -e ".[all]"
```

---

## Architecture Overview

### Layer 1: Models (Pydantic)
- Type-safe data structures
- Runtime validation
- Immutability (frozen models)

### Layer 2: Core Components
- Agent (base class)
- Database (connection pool)
- LLMClient (multi-provider)
- RAGSystem (document analysis)

### Layer 3: Utilities
- Config (environment management)
- Utils (parsing, formatting, sentiment)
- Confidence (sophisticated scoring)

### Layer 4: API
- FastAPI server
- Agent registry
- REST endpoints

### Layer 5: Applications
- Examples (learning agents)
- GUI (Streamlit interface)
- Tests (pytest suite)

---

## Design Patterns Used

1. **Abstract Base Class** - Agent is ABC with abstract analyze()
2. **Lazy Initialization** - LLM/RAG created on first access
3. **Dependency Injection** - Database passed to functions
4. **Context Managers** - Resource cleanup (database connections)
5. **Factory Pattern** - Config creates default instances
6. **Strategy Pattern** - Different agent types, same interface
7. **Repository Pattern** - Database abstracts SQL
8. **Singleton** - Config class (static methods)

---

## For Developers

### Two Ways to Use:

**1. Visual GUI (No coding):**
```bash
./install.sh
# Creates agents through forms
```

**2. Python Framework (Programmatic):**
```bash
pip install -e ".[all]"
# Import and use in your code
```

**Both use the same core framework!**

### Getting Started:

**GUI users:** See [GUI_QUICK_START.md](../GUI_QUICK_START.md)  
**Framework users:** See [FRAMEWORK_QUICKSTART.md](FRAMEWORK_QUICKSTART.md)

---

## Extending the Framework

### Add New Agent Type

1. Create agent class inheriting from `Agent`
2. Implement `analyze()` method
3. Add example in `examples/`
4. Add tests in `tests/`
5. Update documentation

### Add New Database Table

1. Update `schema.sql`
2. Add methods to `database.py`
3. Update `seed_data.py` if needed
4. Add tests
5. Document in API reference

### Add New LLM Provider

1. Add to `LLMConfig` provider Literal
2. Add initialization in `llm.py._get_client()`
3. Add `_chat_provider()` method
4. Update tests
5. Document in configuration guide

---

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for:
- Code standards
- Testing requirements
- Pull request process
- Documentation guidelines

---

## File Organization Best Practices

### One Agent Per File ✅

```python
# GOOD
examples/
├── value_agent.py      # ValueAgent
├── growth_agent.py     # GrowthAgent
└── quality_agent.py    # QualityAgent

# BAD
examples/
└── strategies.py       # ValueAgent, GrowthAgent, QualityAgent
```

**See:** [AGENT_FILE_GUIDELINES.md](AGENT_FILE_GUIDELINES.md)

---

## Resources

- **Getting Started:** [GETTING_STARTED.md](GETTING_STARTED.md)
- **API Reference:** [API_REFERENCE.md](API_REFERENCE.md)
- **Examples:** [../examples/README.md](../examples/README.md)
- **Testing:** [../tests/README.md](../tests/README.md)

---

**Clean, maintainable, educational code structure.** 🚀
