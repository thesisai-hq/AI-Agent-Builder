# AI Agent Framework

Build AI-powered investment analysis agents in Python.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## ⚠️ IMPORTANT DISCLAIMER

**THIS IS AN EDUCATIONAL TOOL FOR LEARNING PURPOSES ONLY**

This software does NOT provide financial advice. All outputs are for educational demonstration only. DO NOT use for real trading without consulting qualified financial professionals. See [DISCLAIMER.md](DISCLAIMER.md) for complete legal terms.

**For production-ready investment tools:** See [thesis-app](https://thesisai.app)

---

## 🚀 Quick Start

**Get running in 5 minutes:**

```bash
# Install
git clone https://github.com/thesisai-hq/AI-Agent-Builder.git
cd AI-Agent-Builder
pip install -e ".[all]"

# Setup database
cp .env.example .env
docker compose up -d postgres
sleep 10
python seed_data.py

# Run first example
python examples/01_basic.py
```

**Detailed guides:**
- **[5-minute setup](QUICK_START.md)** - Copy-paste commands
- **[Complete installation](docs/GETTING_STARTED.md)** - Conda/venv/system Python options
- **[Visual GUI](GUI_QUICK_START.md)** - No-code agent builder
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

---

## 📚 What Is This?

A lightweight Python framework for creating AI agents that analyze stocks and make investment recommendations. Think of it as LEGO blocks for building custom stock analysts.

### Key Features

- 🤖 **Rule-based or AI-powered agents** - Start simple, add AI when needed
- 🎨 **Visual GUI** - Build agents without coding (Streamlit)
- 📊 **PostgreSQL database** - Sample stock data included
- 🔌 **Flexible LLM support** - OpenAI, Anthropic, or local Ollama
- 🚀 **Production-ready API** - FastAPI REST server
- 📦 **Conda/venv/system Python** - Use your preferred environment

### Agent Types

| Type | Speed | Cost | Best For | Example |
|------|-------|------|----------|---------|
| **Rule-Based** | ⚡⚡⚡⚡⚡ | Free | Clear criteria, fast screening | Screen 1000s for PE < 15 |
| **LLM-Powered** | ⚡⚡☆☆☆ | $$ | Deep analysis, small datasets | Analyze top 10 candidates |
| **Hybrid** | ⚡⚡⚡⚡☆ | $ | Large-scale + depth | Screen 500 → Analyze top 25 |
| **RAG-Powered** | ⚡☆☆☆☆ | $$ | Document analysis | Extract insights from SEC filings |

**Learn more:** [Choosing Agent Type Guide](docs/CHOOSING_AGENT_TYPE.md)

---

## 💡 Simple Example

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

**Try it:** `python examples/01_basic.py`

---

## 📖 Documentation

### Getting Started
- **[Quick Start](QUICK_START.md)** - 5-minute setup with copy-paste commands
- **[Getting Started](docs/GETTING_STARTED.md)** - Complete installation guide
- **[GUI Quick Start](GUI_QUICK_START.md)** - Visual agent builder
- **[Configuration](docs/CONFIGURATION.md)** - Environment variables explained
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

### Core Concepts
- **[Choosing Agent Type](docs/CHOOSING_AGENT_TYPE.md)** - Rule-Based vs LLM vs Hybrid vs RAG
- **[Hybrid Agents](docs/HYBRID_AGENTS.md)** - Combining rules and AI efficiently
- **[LLM Customization](docs/LLM_CUSTOMIZATION.md)** - AI model configuration
- **[Database Setup](docs/DATABASE_SETUP.md)** - PostgreSQL details

### Reference
- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - Code organization
- **[Examples Guide](examples/README.md)** - Learning path and strategy examples
- **[Agent File Guidelines](docs/AGENT_FILE_GUIDELINES.md)** - Best practices
- **[API Reference](docs/API_REFERENCE.md)** - REST API documentation

### Legal
- **[Disclaimer](DISCLAIMER.md)** - Educational use and legal terms
- **[License](LICENSE)** - MIT License
- **[Contributing](CONTRIBUTING.md)** - How to contribute

---

## 🎓 Learning Path

Follow these examples in order:

```bash
# 1. Rule-based (no AI, fast)
python examples/01_basic.py          # ⭐ Start here

# 2. LLM-powered (AI analysis)
python examples/02_llm_agent.py      # ⭐⭐ Requires Ollama

# 3. Hybrid (rules + AI)
python examples/03_hybrid.py         # ⭐⭐⭐ Best of both

# 4. RAG document analysis
python examples/04_rag_agent.py      # ⭐⭐⭐⭐ Analyze PDFs

# 5. Famous investor strategies
python examples/05_buffett_quality.py  # Warren Buffett
python examples/06_lynch_garp.py       # Peter Lynch
python examples/07_graham_value.py     # Benjamin Graham
```

**Or use the visual GUI:**
```bash
./gui/launch.sh
```

---

## 🛠️ Installation Options

### Core Dependencies (Always Installed)
```bash
pip install -e .
```
Includes: FastAPI, Pydantic, AsyncPG, basic framework

### Optional Dependencies

```bash
# LLM support (OpenAI, Anthropic, Ollama)
pip install -e ".[llm]"

# RAG support (Document analysis)
pip install -e ".[rag]"

# Development tools (pytest, black, ruff)
pip install -e ".[dev]"

# Everything (recommended)
pip install -e ".[all]"
```

**See [Getting Started](docs/GETTING_STARTED.md) for environment setup (conda/venv/system Python)**

---

## 🔧 Configuration

All settings are managed via `.env` file:

```bash
# Copy template
cp .env.example .env

# Edit settings
nano .env
```

**Key settings:**
- **Database:** Host, port, credentials
- **LLM providers:** OpenAI, Anthropic, Ollama
- **API:** Host, port, CORS

**See [Configuration Guide](docs/CONFIGURATION.md) for details**

---

## 🤖 AI Integration (Optional)

### Free Local AI (Ollama)
```bash
# Install
curl https://ollama.ai/install.sh | sh

# Download model
ollama pull llama3.2

# Run examples
python examples/02_llm_agent.py
```

### OpenAI (ChatGPT)
```bash
# Add to .env
OPENAI_API_KEY=sk-your-key-here

# Run examples
python examples/02_llm_agent.py
```

### Anthropic (Claude)
```bash
# Add to .env
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Run examples
python examples/02_llm_agent.py
```

**See [LLM Customization Guide](docs/LLM_CUSTOMIZATION.md) for advanced configuration**

---

## 🎨 Visual GUI

Build agents without coding:

```bash
# Setup (one time - installs ALL dependencies)
./gui/setup.sh

# Launch
./gui/launch.sh
```

**Setup installs everything:**
- ✅ GUI (Streamlit)
- ✅ All LLM providers (Ollama, OpenAI, Anthropic)
- ✅ RAG support (document analysis)
- ✅ PDF processing

**No optional dependencies!** Everything works after setup.

**Features:**
- 📋 Browse and manage agents
- ➕ Create agents visually (Rule-Based, LLM, Hybrid, RAG)
- 🧪 Test agents with mock data or PDFs
- 📈 Backtest agents on scenarios
- 💾 Save directly to `examples/`
- 🎓 Educational tooltips for financial metrics

**See [GUI Quick Start](GUI_QUICK_START.md) for details**

---

## 🏗️ Project Structure

```
AI-Agent-Builder/
├── agent_framework/        # Core package
│   ├── agent.py           # Base Agent class
│   ├── models.py          # Pydantic data models
│   ├── database.py        # PostgreSQL client
│   ├── llm.py             # LLM integrations
│   ├── rag.py             # Document analysis
│   ├── api.py             # FastAPI server
│   └── config.py          # Configuration
│
├── gui/                   # Visual agent builder
│   └── app.py            # Streamlit application
│
├── examples/              # Learning examples
│   ├── 01_basic.py        # Rule-based
│   ├── 02_llm_agent.py    # LLM-powered
│   ├── 03_hybrid.py       # Hybrid
│   └── 04_rag_agent.py    # RAG-powered
│
├── docs/                  # Documentation
├── tests/                 # Test suite
└── docker-compose.yml     # Database setup
```

**See [Project Structure](docs/PROJECT_STRUCTURE.md) for details**

---

## 📝 Common Commands

```bash
# Environment management
conda activate agent-framework          # Conda
source venv/bin/activate                # venv

# Database
docker compose up -d postgres           # Start
docker compose down                     # Stop
docker compose logs postgres            # View logs

# Development
python examples/01_basic.py             # Run agent
pytest tests/                           # Run tests
pip install -e ".[dev]"                # Install dev tools

# GUI
./gui/launch.sh                        # Start GUI
```

---

## 🐛 Troubleshooting

**Common issues:**

| Problem | Quick Fix |
|---------|-----------|
| Module not found | `pip install -e ".[all]"` |
| Can't connect to DB | `docker compose up -d postgres` |
| Port in use | Change `DB_PORT` in `.env` |
| LLM not working | `ollama serve` + `ollama pull llama3.2` |

**See [Complete Troubleshooting Guide](docs/TROUBLESHOOTING.md) for all issues**

---

## ⚡ Performance Tips

**For large-scale screening:**
- Use **Rule-Based** for initial filtering (1000s of stocks)
- Use **Hybrid** for smart filtering + deep analysis (95% cost reduction)
- Use **LLM-Powered** only on final candidates (< 20 stocks)

**For production:**
- Connection pooling enabled by default (2-10 connections)
- Async operations for non-blocking I/O
- Horizontal scaling via FastAPI

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Ways to contribute:**
- 🐛 Report bugs
- 💡 Suggest features
- 📖 Improve documentation
- 🔧 Submit pull requests
- 🎓 Share example strategies

---

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

Copyright (c) 2025 ThesisAI LLC

**Summary:** You can use, modify, and distribute this software freely, with attribution.

---

## ⚖️ Legal

### Educational Use Only

This software is for **learning and education only**. It is NOT:
- ❌ Financial advice
- ❌ Investment recommendations
- ❌ Trading signals
- ❌ Professional advice

### Investment Risks

ALL INVESTMENTS CARRY RISK. You can lose money. Past performance does not guarantee future results.

### Requirements

Before any real trading:
- ✅ Consult licensed financial advisors
- ✅ Understand all risks
- ✅ Comply with regulations
- ✅ Use professional data sources
- ✅ Implement proper risk management

**See [DISCLAIMER.md](DISCLAIMER.md) for complete legal terms**

---

## 🚀 Production Ready?

For production trading systems with:
- ✅ Professional risk management
- ✅ Regulatory compliance
- ✅ Real-time data integrations
- ✅ Production support and SLAs
- ✅ Proper legal protection

**Visit [thesis-app](https://thesisai.app)**

---

## 📞 Support

- **Documentation:** [docs/](docs/)
- **Examples:** [examples/](examples/)
- **Issues:** [GitHub Issues](https://github.com/thesisai-hq/AI-Agent-Builder/issues)
- **Troubleshooting:** [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

**Do not request financial advice in issues**

---

## 🙏 Acknowledgments

Built for learning. Inspired by legendary investors:
- Warren Buffett - Quality investing
- Peter Lynch - Growth at reasonable price
- Benjamin Graham - Value investing

---

**Educational tool · Not financial advice · MIT License · [Full Disclaimer](DISCLAIMER.md)**
