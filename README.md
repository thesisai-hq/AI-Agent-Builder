# AI Agent Builder - Learn Investment Analysis with AI

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![For Education](https://img.shields.io/badge/use-education%20only-orange.svg)](DISCLAIMER.md)

**Build AI-powered stock analysis agents** - Choose your approach:

---

## Choose Your Path

### 🎨 Visual GUI (No Coding Required)

**Perfect for:**
- 📚 Finance students learning investment concepts
- 🏫 University courses on quantitative finance
- 💡 Anyone exploring AI in investing
- 🧑‍🎓 Beginners with no programming background

**What you get:**
- Visual agent builder (forms, no code)
- Pre-built strategies (Buffett, Lynch, Graham)
- Test with sample data instantly
- View generated code to learn Python (optional)

**[→ GUI Quick Start](#-gui-quick-start)**

---

### 💻 Python Framework (For Developers)

**Perfect for:**
- 👨‍💻 Developers building investment systems
- 🔬 Researchers creating custom strategies
- 🏢 Teams integrating into larger applications
- 🎓 Students learning Python + finance together

**What you get:**
- Full programmatic control
- Import into your projects
- Build multi-agent orchestrations
- REST API for service deployment

**[→ Framework Quick Start](#-framework-quick-start)**

---

**Both paths use the same powerful framework - choose what works for you!**

---

## ⚠️ Educational Tool Only

This is a **learning tool for finance education**. Not for real trading.

- ❌ **NOT financial advice** - For learning only
- ❌ **NOT for real trading** - Theoretical exercises only
- ✅ **FOR education** - Learn investment concepts with AI

**Ready for production?** [thesis-app](THESIS_APP.md) - professional platform (coming soon)

**Legal:** [DISCLAIMER.md](DISCLAIMER.md) | [LICENSE](LICENSE)

---

## 🎨 GUI Quick Start

### One-Command Installation

**Linux / macOS / WSL2:**
```bash
git clone https://github.com/thesisai-hq/AI-Agent-Builder.git
cd AI-Agent-Builder
chmod +x install.sh
./install.sh
```

**Windows:**
```bash
git clone https://github.com/thesisai-hq/AI-Agent-Builder.git
cd AI-Agent-Builder
install.bat
```

**Opens visual GUI at:** `http://localhost:8501`

### What the Installer Does:
1. Checks prerequisites (Python 3.10+, Docker)
2. Creates virtual environment
3. Installs all dependencies
4. Sets up PostgreSQL database
5. Adds sample data (AAPL, MSFT, TSLA, JPM)
6. Launches visual GUI automatically

**Time to first agent:** 10 minutes (no coding!)

**Complete GUI guide:** [GUI_QUICK_START.md](GUI_QUICK_START.md)

---

## 💻 Framework Quick Start

### Installation (For Developers)

```bash
# Clone repository
git clone https://github.com/thesisai-hq/AI-Agent-Builder.git
cd AI-Agent-Builder

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate.bat  # Windows

# Install framework
pip install -e ".[all]"

# Setup database
cp .env.example .env
docker compose up -d postgres
sleep 10
python seed_data.py
```

### Your First Agent (Pure Python)

```python
# my_agent.py
from agent_framework import Agent, Signal, Database, Config
import asyncio

class ValueAgent(Agent):
    """Buy undervalued stocks with low PE ratios."""
    
    async def analyze(self, ticker: str, data: dict) -> Signal:
        pe = data.get('pe_ratio', 0)
        
        if pe < 15:
            return Signal('bullish', 0.8, f'Undervalued: PE={pe}')
        elif pe > 30:
            return Signal('bearish', 0.7, f'Overvalued: PE={pe}')
        else:
            return Signal('neutral', 0.6, 'Fair value')

async def main():
    # Connect to database
    db = Database(Config.get_database_url())
    await db.connect()
    
    # Create agent
    agent = ValueAgent()
    
    # Analyze stocks
    for ticker in await db.list_tickers():
        data = await db.get_fundamentals(ticker)
        signal = await agent.analyze(ticker, data)
        print(f"{ticker}: {signal.direction} ({signal.confidence:.0%}) - {signal.reasoning}")
    
    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

**Run it:**
```bash
python my_agent.py
```

**Output:**
```
AAPL: neutral (60%) - Fair value: PE=28.5
MSFT: neutral (60%) - Fair value: PE=32.1
TSLA: bearish (70%) - Overvalued: PE=52.3
JPM: bullish (80%) - Undervalued: PE=11.2
```

**Time to first agent:** 15 minutes (if familiar with Python)

**Complete framework guide:** [docs/FRAMEWORK_QUICKSTART.md](docs/FRAMEWORK_QUICKSTART.md)

---

## 🎓 What You'll Learn

### Finance Concepts
- **Value investing** (Warren Buffett, Benjamin Graham)
- **Growth investing** (Peter Lynch, GARP)
- **Risk assessment** and portfolio construction
- **SEC filing analysis** with AI
- **Multi-factor** investment strategies
- **Quantitative screening** techniques

### AI/Tech Skills (Optional)
- Using **AI for analysis** (ChatGPT, Claude, LLaMA)
- **Prompt engineering** for financial analysis
- **Document processing** with RAG (Retrieval-Augmented Generation)
- **Sentiment analysis** with VADER (news and text analysis)
- **Python basics** (by viewing generated code)
- **Database queries** and data management

**GUI users:** Learn concepts without coding  
**Framework users:** Learn Python + finance together

---

## 🤖 Four Agent Types

Create agents either way - visual forms **OR** Python code:

### 📊 Rule-Based (Start Here!)

**Concept:** Clear if/then rules you define  
**Example:** "Buy if PE < 15 AND ROE > 15%"  
**Speed:** Very fast (milliseconds)  
**Setup:** None - works immediately!

**GUI:** Fill form → Generate code  
**Framework:** Write Python class directly

---

### 🧠 LLM-Powered (AI Intelligence)

**Concept:** Uses AI for nuanced analysis  
**Example:** "Apple shows strong competitive moat..."  
**Speed:** Slower (2-5 seconds)  
**Setup:** Install Ollama (free) or use OpenAI/Anthropic (paid)

**GUI:** Configure in forms → AI reasoning  
**Framework:** LLMConfig + system prompts

---

### 🔀 Hybrid (Best of Both)

**Concept:** Rules filter + AI analyzes  
**Example:** Filter 1000 stocks → AI analyzes top 50  
**Speed:** Fast screening, selective analysis  
**Setup:** Same as LLM

**GUI:** Define rules + LLM config  
**Framework:** Two-stage analyze() method

---

### 📄 RAG-Powered (Document Analysis)

**Concept:** Analyzes long documents  
**Example:** Extract insights from 100-page 10-K  
**Speed:** Varies by document size  
**Setup:** Same as LLM

**GUI:** Upload PDF → Get insights  
**Framework:** RAGSystem + document processing

**[Complete Agent Type Guide →](docs/CHOOSING_AGENT_TYPE.md)**

---

## 🎨 GUI Features

**No coding required!** Create agents through visual interface:

- 🎨 **Agent Builder** - Form-based creation
- 📚 **Example Gallery** - Buffett, Lynch, Graham strategies
- 🧪 **Testing** - Try agents on sample or real data
- 👁️ **Code Viewer** - See generated Python code
- 📄 **PDF Upload** - Analyze SEC filings
- ⚙️ **LLM Setup Wizard** - Step-by-step AI configuration
- 💾 **Save & Share** - Export agents as Python files

**Launch GUI:**
```bash
./gui/launch.sh   # After installation
```

**[Complete GUI Guide →](GUI_QUICK_START.md)**

---

## 💻 Framework Features

**Full programmatic control** for developers:

```python
# Import and use in your code
from agent_framework import (
    Agent, Signal, Database, Config,
    LLMConfig, RAGConfig, AgentConfig
)

# Build custom agents
class MyAgent(Agent):
    async def analyze(self, ticker, data):
        # Your logic here
        return Signal(...)

# Use in your projects
agent = MyAgent()
signal = await agent.analyze('AAPL', data)
```

**Framework capabilities:**
- ✅ Import as library
- ✅ REST API server (FastAPI)
- ✅ Multi-agent orchestration
- ✅ Custom database queries
- ✅ Async operations
- ✅ Type safety (Pydantic)

**Run examples:**
```bash
python examples/01_basic.py       # Rule-based agent
python examples/02_llm_agent.py   # AI-powered agent
python examples/03_hybrid.py      # Hybrid agent
```

**[Complete Framework Guide →](docs/FRAMEWORK_QUICKSTART.md)**

---

## 📚 Learning Path

### For GUI Users (No Coding)

**Week 1:**
1. Create rule-based agent in GUI (30 min)
2. Test with sample data (20 min)
3. Try example strategies (1 hour)

**Week 2:**
4. Setup Ollama (10 min)
5. Create AI-powered agent (30 min)
6. Compare AI vs rules (20 min)

**Week 3+:**
7. Create hybrid agent (30 min)
8. Upload and analyze PDFs (45 min)
9. Build custom strategy (2 hours)

**Total:** 8-12 hours over 3 weeks

---

### For Framework Users (Python)

**Day 1:**
1. Install framework (`pip install`) (10 min)
2. Run examples/01_basic.py (5 min)
3. Modify and experiment (30 min)

**Day 2:**
4. Build custom agent class (30 min)
5. Add LLM integration (30 min)
6. Test with database (20 min)

**Day 3+:**
7. Build multi-agent system (2 hours)
8. Deploy REST API (1 hour)
9. Integrate into your project (varies)

**Total:** 5-8 hours to proficiency

---

## 💡 Same Agent, Two Ways

**Goal:** Create a value investing agent

### 🎨 GUI Approach:
1. Open GUI → Create Agent
2. Select "Rule-Based"
3. Add rule: PE < 15 → Bullish
4. Click "Generate Code"
5. Click "Save"

**Result:** `value_agent.py` file created

---

### 💻 Framework Approach:
1. Create `value_agent.py`
2. Write Python code:
```python
from agent_framework import Agent, Signal

class ValueAgent(Agent):
    async def analyze(self, ticker, data):
        pe = data.get('pe_ratio', 0)
        if pe < 15:
            return Signal('bullish', 0.8, f'Undervalued: PE={pe}')
        return Signal('neutral', 0.5, 'Fair value')
```
3. Run: `python value_agent.py`

**Result:** Same functionality, created in code

---

**Both create identical Python code - choose your workflow!**

---

## 📖 Documentation

### For GUI Users
- [GUI Quick Start](GUI_QUICK_START.md) - Visual interface walkthrough
- [Creating Agents Visually](docs/GUI_TUTORIAL.md) - Step-by-step
- [Understanding Signals](docs/SIGNALS_EXPLAINED.md) - What results mean

### For Framework Users
- [Framework Quick Start](docs/FRAMEWORK_QUICKSTART.md) - Code-based setup
- [API Reference](docs/API_REFERENCE.md) - Complete API documentation
- [Integration Patterns](docs/INTEGRATION_PATTERNS.md) - Real-world usage
- [Example Code](examples/README.md) - Working examples

### For Both
- [Getting Started](docs/GETTING_STARTED.md) - Installation all methods
- [Configuration](docs/CONFIGURATION.md) - Environment settings
- [Database Setup](docs/DATABASE_SETUP.md) - PostgreSQL guide
- [LLM Customization](docs/LLM_CUSTOMIZATION.md) - AI configuration
- [Choosing Agent Type](docs/CHOOSING_AGENT_TYPE.md) - Which to use when
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues

---

## 🎓 For Universities & Educators

### Why Use in Your Course?

**For GUI-based courses:**
- ✅ Zero coding barrier - Students use visual interface
- ✅ Fast setup - One command installation
- ✅ Immediate results - Create agents in minutes

**For programming courses:**
- ✅ Learn Python through finance
- ✅ Real-world framework design
- ✅ Production patterns (async, pooling, validation)

**For both:**
- ✅ Code visibility - GUI shows generated code
- ✅ Progression - Start GUI, graduate to code
- ✅ Real strategies - Buffett, Lynch, Graham
- ✅ Complete curriculum - 8-12 hours structured learning

### Course Examples

**Quantitative Finance (GUI-focused):**
- Week 1-2: Create agents visually
- Week 3-4: View and understand code
- Week 5-6: Modify exported code
- Week 7-8: Custom strategies

**Python for Finance (Code-focused):**
- Week 1-2: Run and modify examples
- Week 3-4: Build agents from scratch
- Week 5-6: Multi-agent systems
- Week 7-8: API deployment

**[University Setup Guide →](docs/UNIVERSITY_SETUP.md)**

---

## 🚀 From Learning to Production

### You've Learned the Basics

**With GUI:**
- ✅ Understand investment agent concepts
- ✅ Built and tested strategies
- ✅ Learned from famous investors

**With Framework:**
- ✅ Understand agent architecture
- ✅ Built programmatic systems
- ✅ Integrated into projects

### Interested in Production Trading?

**thesis-app** (coming soon) will offer production-ready features:

| Feature | AI-Agent-Builder<br>**(Available Now - Free)** | thesis-app<br>**(Coming Soon)** |
|---------|-----------------|----------------|
| Purpose | Learning & experimentation | Professional trading |
| Data | Sample (10-20 stocks) | Real-time (10,000+ stocks) |
| Historical | Snapshot only | 10+ years of data |
| Execution | Manual testing | Automated execution |
| Portfolio | Single stock | Full portfolio management |
| Risk Controls | Basic confidence | Professional risk controls |
| Support | Community | Professional support |
| Cost | **Free forever** | Details TBA |

*thesis-app is currently in development. [Learn more →](THESIS_APP.md)*

---

## 🤝 Contributing

Help make this better for students and developers worldwide!

- 🐛 **Report bugs** - [GitHub Issues](https://github.com/thesisai-hq/AI-Agent-Builder/issues)
- 📖 **Improve docs** - GUI or framework documentation
- 🎓 **Add examples** - Visual strategies or code examples
- 💡 **Suggest features** - For GUI or framework
- 🔧 **Submit PRs** - Code contributions welcome

**Both GUI and framework contributions valued equally!**

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📜 License & Legal

### Open Source (MIT License)

**Free to use, modify, and distribute**

```
Copyright (c) 2025 ThesisAI LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

[Full License](LICENSE)

### What You Can Do

- ✅ Use for personal projects (GUI or code)
- ✅ Use for educational purposes
- ✅ Modify however you want
- ✅ Use in university courses
- ✅ Build upon for research
- ✅ Include in your own projects
- ✅ Deploy as service (with proper disclaimers)

Just include the license and copyright notice.

### Educational Disclaimer

**This software:**
- ❌ Does NOT provide financial advice
- ❌ Is NOT for real trading (use thesis-app when ready)
- ❌ Has NO warranties or guarantees
- ⚠️ All investments carry risk of loss

**Before investing real money:**
- ✅ Consult licensed financial advisors
- ✅ Understand all investment risks
- ✅ Never trade money you can't afford to lose
- ✅ Consider professional platforms (thesis-app coming soon)

[Full Disclaimer](DISCLAIMER.md)

---

## 💬 Get Help & Connect

### Documentation
- 📖 [Complete Docs](docs/) - All guides and references
- ❓ [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues

### Report Issues
- 🐛 [GitHub Issues](https://github.com/thesisai-hq/AI-Agent-Builder/issues) - Bug reports (GUI or framework)
- 💡 [Feature Requests](https://github.com/thesisai-hq/AI-Agent-Builder/discussions) - Suggestions

---

## 🎯 Quick Commands

```bash
# Installation
./install.sh              # GUI: One-command setup (Linux/Mac)
install.bat               # GUI: One-command setup (Windows)
pip install -e ".[all]"  # Framework: Developer install

# GUI Usage
./gui/launch.sh           # Start visual interface

# Framework Usage
python examples/01_basic.py    # Run example agent
python my_agent.py             # Run your agent

# Database
docker compose up -d postgres   # Start database
docker compose down             # Stop everything
python seed_data.py            # Re-seed data

# Development
pytest tests/                   # Run tests
pip install -e ".[dev]"        # Install dev tools
```

---

## 🗺️ Project Overview

```
AI-Agent-Builder/
├── agent_framework/     # Core framework (~1,200 lines)
│   ├── agent.py        # Base Agent class - inherit this
│   ├── models.py       # Signal, LLMConfig, etc.
│   ├── database.py     # PostgreSQL client
│   ├── llm.py          # LLM integration
│   ├── rag.py          # Document analysis
│   └── api.py          # REST API server
│
├── examples/            # Pre-built strategies
│   ├── 01_basic.py     # Rule-based agents
│   ├── 02_llm_agent.py # AI-powered agents
│   ├── 05_buffett_quality.py  # Warren Buffett
│   ├── 06_lynch_garp.py       # Peter Lynch
│   └── 07_graham_value.py     # Benjamin Graham
│
├── gui/                 # Visual interface (Streamlit)
│   ├── app.py          # Main GUI application
│   ├── agent_creator.py # Visual agent builder
│   └── agent_tester.py  # Testing interface
│
├── docs/                # Complete documentation
│   ├── FRAMEWORK_QUICKSTART.md  # For developers
│   ├── API_REFERENCE.md         # Complete API
│   └── ...
│
├── install.sh           # GUI one-command installer
└── README.md            # This file
```

---

## ⭐ Show Your Support

If this helped you learn (via GUI or framework):
- ⭐ Star this repo on GitHub
- 🐦 Share on Twitter with #AIAgentBuilder
- 📧 Recommend to your professor or team
- 💬 Share your success story

---

*Remember: This is for education only. For real trading, consult financial professionals. Interested in production tools? [thesis-app is coming soon](THESIS_APP.md).*
