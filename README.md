# AI Agent Framework

Build AI-powered investment analysis agents in Python.

## What Is This?

A lightweight framework for creating AI agents that analyze stocks and make investment recommendations. Think of it as LEGO blocks for building custom stock analysts.

**Key Features:**
- 🤖 Rule-based or AI-powered agents
- 🎨 Visual GUI for building agents (Streamlit)
- 📊 PostgreSQL database with sample stock data
- 🔌 Supports OpenAI, Anthropic, or local Ollama
- 🚀 Production-ready FastAPI server
- 📦 Works with conda, venv, or system Python

## Quick Start

```bash
# 1. Install (choose one environment: conda, venv, or system Python)
git clone https://github.com/thesisai-hq/AI-Agent-Builder.git
cd AI-Agent-Builder
pip install -e .

# 2. Setup database
cp .env.example .env
docker compose up -d postgres
python seed_data.py

# 3. Run example
python examples/01_basic.py
```

See [Quick Start Guide](QUICK_START.md) for detailed setup with conda/venv options.

## Simple Example

```python
from agent_framework import Agent, Signal, Database, Config
import asyncio

class ValueAgent(Agent):
    """Buy undervalued stocks (PE < 15)"""
    
    def analyze(self, ticker, data):
        pe = data.get('pe_ratio', 0)
        
        if pe < 15:
            return Signal('bullish', 0.8, f'Undervalued at PE={pe:.1f}')
        elif pe > 30:
            return Signal('bearish', 0.7, f'Overvalued at PE={pe:.1f}')
        else:
            return Signal('neutral', 0.5, 'Fair value')

async def main():
    db = Database(Config.get_database_url())
    await db.connect()
    
    agent = ValueAgent()
    data = await db.get_fundamentals('AAPL')
    signal = agent.analyze('AAPL', data)
    
    print(f"{signal.direction.upper()}: {signal.reasoning}")
    await db.disconnect()

asyncio.run(main())
```

## Installation Options

### Core Dependencies Only
```bash
pip install -e .
```

### With LLM Support (OpenAI, Anthropic, Ollama)
```bash
pip install -e ".[llm]"
```

### With RAG (Document Analysis)
```bash
pip install -e ".[rag]"
```

### With Development Tools
```bash
pip install -e ".[dev]"
```

### Everything
```bash
pip install -e ".[all]"
```

## GUI - Visual Agent Builder

Build agents visually with no coding required!

```bash
# Setup
./gui/setup.sh

# Launch
./gui/launch.sh
```

**Features:**
- 📋 Browse existing agents
- ➕ Create agents (Rule-Based, LLM-Powered, Hybrid)
- 🧪 Test agents with mock or real data
- 💾 Save directly to `examples/`

See **[GUI Quick Start](GUI_QUICK_START.md)** for details.

## Documentation

### Quick Start Guides
- **[GUI Quick Start](GUI_QUICK_START.md)** - Visual agent builder (5 min)
- **[Quick Start](QUICK_START.md)** - Framework setup (5 min)

### Framework Documentation
- **[Getting Started](docs/GETTING_STARTED.md)** - Detailed installation
- **[Configuration](docs/CONFIGURATION.md)** - Environment settings
- **[Database Guide](docs/DATABASE_SETUP.md)** - Database setup
- **[LLM Customization](docs/LLM_CUSTOMIZATION.md)** - AI configuration
- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - Architecture

### GUI Documentation
- **[GUI README](gui/README.md)** - Complete GUI guide

## Project Structure

```
AI-Agent-Builder/
├── agent_framework/        # Core framework
│   ├── __init__.py        # Public API exports
│   ├── agent.py           # Base Agent class
│   ├── models.py          # Pydantic data models
│   ├── database.py        # PostgreSQL client
│   ├── llm.py             # LLM integrations
│   ├── rag.py             # Document analysis
│   ├── api.py             # FastAPI server
│   ├── config.py          # Configuration management
│   └── utils.py           # Utility functions
│
├── gui/                   # Visual agent builder (NEW)
│   ├── app.py            # Streamlit GUI application
│   ├── agent_loader.py   # Load/save agents
│   ├── agent_creator.py  # Generate agent code
│   ├── agent_tester.py   # Test agents
│   └── README.md         # GUI documentation
│
├── examples/              # Working examples
│   ├── 01_basic.py        # Simple rule-based agents
│   ├── 02_llm_agent.py    # AI-powered agents
│   ├── 03_rag_agent.py    # Document analysis
│   └── 04_custom_llm_config.py  # LLM customization
│
├── docs/                  # Documentation
├── tests/                 # Test suite
├── pyproject.toml         # Package configuration (PEP 621)
└── docker-compose.yml     # Database setup
```

## Common Commands

```bash
# Activate environment (choose your setup)
conda activate agent-framework          # If using conda
source venv/bin/activate                # If using venv
# (no activation needed for system Python)

# Start database
docker compose up -d postgres

# Run examples
python examples/01_basic.py
python examples/02_llm_agent.py

# Run tests
pytest tests/

# Stop database
docker compose down
```

## Using AI (Optional)

### Free Local AI (Ollama)
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Download model
ollama pull llama3.2

# Install framework with LLM support
pip install -e ".[llm]"
```

### OpenAI ChatGPT
```bash
# Add to .env
OPENAI_API_KEY=sk-your-key-here

# Install with LLM support
pip install -e ".[llm]"
```

### Anthropic Claude
```bash
# Add to .env
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Install with LLM support
pip install -e ".[llm]"
```

## Requirements

- Python 3.10+
- Docker (for PostgreSQL)
- Terminal: WSL2, macOS, or Linux

## Optional: Ultra-Fast Installation with uv

Want 10-100x faster installs? Use [uv](https://github.com/astral-sh/uv):

```bash
# Install uv (one-time setup)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Use uv instead of pip (same commands)
uv pip install -e ".[all]"

# uv is a drop-in replacement - works with existing pyproject.toml
```

## License

MIT License - See [LICENSE](LICENSE) file.

## Support

- **Issues:** [GitHub Issues](https://github.com/thesisai-hq/AI-Agent-Builder/issues)
- **Documentation:** [docs/](docs/)
- **Examples:** [examples/](examples/)

---

Built for learning and experimentation. Not financial advice.
