# Project Structure

## Directory Layout

```
AI-Agent-Builder/
├── agent_framework/          # Core package
│   ├── __init__.py          # Public API
│   ├── models.py            # Pydantic models
│   ├── agent.py             # Agent base class
│   ├── database.py          # PostgreSQL client
│   ├── llm.py               # LLM client
│   ├── rag.py               # RAG system
│   ├── api.py               # FastAPI server
│   ├── config.py            # Configuration
│   └── utils.py             # Utilities
│
├── examples/                 # Working examples
│   ├── 01_basic.py          # Simple agents
│   ├── 02_llm_agent.py      # LLM agents
│   ├── 03_hybrid.py         # Hybrid agents
│   └── 04_rag_agent.py      # RAG agents
│
├── tests/                    # Test suite
│   └── test_framework.py    # Tests
│
├── docs/                     # Documentation
│   ├── GETTING_STARTED.md   # Installation & setup
│   ├── CONFIGURATION.md     # Environment config
│   ├── LLM_CUSTOMIZATION.md # LLM per-agent config
│   ├── DATABASE_SETUP.md    # Database details
│   └── PROJECT_STRUCTURE.md # This file
│
├── docker-compose.yml        # PostgreSQL setup
├── schema.sql                # Database schema
├── seed_data.py              # Sample data
├── pyproject.toml            # Package config (PEP 621)
├── .env.example              # Config template
└── README.md                 # Main docs
```

## Core Modules

### models.py
Pydantic models with validation:
- `Signal` - Trading signal
- `LLMConfig` - LLM configuration
- `RAGConfig` - RAG configuration
- `AgentConfig` - Agent configuration
- `DatabaseConfig` - Database configuration

### agent.py
Base agent class with lazy initialization:
- Abstract `analyze()` method
- Optional LLM and RAG support
- Simple, extensible design

### database.py
PostgreSQL client with:
- Connection pooling
- Transaction support
- Error handling
- Health checks

### llm.py
Unified LLM interface for:
- OpenAI
- Anthropic
- Ollama

Features: retries, system prompts, error handling

### rag.py
Document retrieval and analysis:
- Text chunking
- Semantic search
- Query interface

### api.py
FastAPI REST server:
- Health endpoints
- Data endpoints
- Analysis endpoints
- Agent registration

### config.py
Centralized configuration:
- Environment variable helpers
- Database URLs
- LLM settings

### utils.py
Shared utilities:
- `parse_llm_signal()` - Parse LLM responses
- `format_fundamentals()` - Format data for LLMs
- `calculate_sentiment_score()` - Sentiment analysis

## Code Size

```
Core package:      ~1,200 lines
Examples:          ~400 lines
Tests:             ~300 lines
Total:             ~2,000 lines
```

Compact, maintainable codebase.

## Design Principles

1. **Pydantic validation** - Runtime type checking
2. **Dependency injection** - No singletons, testable
3. **Lazy initialization** - Load only what's needed
4. **Error handling** - Comprehensive exceptions
5. **Connection pooling** - Performance
6. **Async operations** - Non-blocking I/O

## Adding Components

### New Agent

```python
# examples/my_agent.py
from agent_framework import Agent, Signal

class MyAgent(Agent):
    def analyze(self, ticker, data):
        return Signal('bullish', 0.8, 'Custom logic')
```

### New Database Method

```python
# agent_framework/database.py
async def get_custom_data(self, ticker):
    async with self.acquire() as conn:
        return await conn.fetch("SELECT...")
```

### New API Endpoint

```python
# agent_framework/api.py
@app.get("/custom")
async def custom_endpoint(db: Database = Depends(get_db)):
    return await db.get_custom_data()
```

### New Utility

```python
# agent_framework/utils.py
def custom_utility(data):
    return processed_data
```

## Import Patterns

```python
# Core
from agent_framework import Agent, Signal, Config

# Database
from agent_framework import Database

# LLM
from agent_framework import LLMConfig, LLMClient

# RAG
from agent_framework import RAGConfig, RAGSystem

# API
from agent_framework import api_app, register_agent_instance

# Utils
from agent_framework import parse_llm_signal, format_fundamentals
```

## File Conventions

- **Classes**: PascalCase
- **Functions**: snake_case
- **Constants**: UPPER_SNAKE_CASE
- **Private**: _leading_underscore
- **Line limit**: 88 characters (Black)
- **Type hints**: Required for public APIs
- **Docstrings**: Required for public functions

## Testing Structure

```
tests/
├── test_framework.py     # All tests
└── conftest.py           # Fixtures (if needed)
```

Keep tests simple and focused.

## Documentation Structure

```
docs/
├── GETTING_STARTED.md    # Installation & first steps
├── CONFIGURATION.md      # Environment variables
├── LLM_CUSTOMIZATION.md  # Per-agent LLM config
├── DATABASE_SETUP.md     # Database details
├── TESTING.md            # Testing guide
└── PROJECT_STRUCTURE.md  # This file
```

Minimal, focused documentation.
