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

### Setup & Launch

```bash
# Clone repository
git clone https://github.com/thesisai-hq/AI-Agent-Builder.git
cd AI-Agent-Builder

# One-time setup
chmod +x gui/setup.sh gui/launch.sh
./gui/setup.sh

# Launch GUI (every time)
./gui/launch.sh
```

**Opens at:** `http://localhost:8501`

**Time to first agent:** 10 minutes (no coding!)

---

### What Gets Installed

✅ **GUI framework** (Streamlit)  
✅ **PDF processing** (PyPDF2)  
✅ **All LLM providers** (Ollama, OpenAI, Anthropic)  
✅ **RAG support** (sentence-transformers)  
✅ **Framework core** (FastAPI, PostgreSQL client, Pydantic)

**Everything installed - full functionality immediately!**

---

### Optional: Database Setup (For Real Data)

**GUI works with mock data by default.** For testing with database:

```bash
# Copy environment template
cp .env.example .env

# Start PostgreSQL
docker compose up -d postgres
sleep 10

# Add sample data (AAPL, MSFT, TSLA, JPM)
python seed_data.py
```

---

### Optional: LLM Setup (For AI Agents)

**Rule-Based agents work immediately!** For LLM/RAG/Hybrid agents:

**Ollama (Free, Local AI - Recommended):**
```bash
# Install Ollama service
curl https://ollama.ai/install.sh | sh

# Download model (~4GB)
ollama pull llama3.2

# Start service (keep running)
ollama serve
```

**Or use the visual "⚙️ LLM Setup" wizard in the GUI!**

**OpenAI/Anthropic (Cloud APIs):**
```bash
# Add API key to .env
nano .env
# Add: OPENAI_API_KEY=sk-your-key
# or: ANTHROPIC_API_KEY=sk-ant-your-key
```

**[Complete GUI Guide →](GUI_QUICK_START.md)**

---

## 💻 Framework Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/thesisai-hq/AI-Agent-Builder.git
cd AI-Agent-Builder

# Install with pip (standard Python workflow)
pip install -e ".[all]"
```

**That's it!** Framework is installed and ready to use.

**Alternative installations:**
```bash
# Minimal (core only)
pip install -e .

# With LLM support
pip install -e ".[llm]"

# With RAG support
pip install -e ".[rag]"

# Development tools
pip install -e ".[dev]"

# Everything (recommended)
pip install -e ".[all]"
```

**Time to first agent:** 5 minutes

---

### Optional: Virtual Environment (Recommended)

```bash
# Create isolated environment
python3 -m venv venv

# Activate
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Then install
pip install -e ".[all]"
```

---

### Optional: Database Setup

```bash
# Copy environment template
cp .env.example .env

# Start PostgreSQL with Docker
docker compose up -d postgres
sleep 10

# Seed sample data
python seed_data.py
```

**Note:** Many examples work without database (mock data)

---

### Your First Agent (5 Minutes)

Create `my_agent.py`:

```python
from agent_framework import Agent, Signal, Database, Config
import asyncio

class ValueAgent(Agent):
    """Buy undervalued stocks with low PE ratios."""
    
    async def analyze(self, ticker: str, data: dict) -> Signal:
        pe = data.get('pe_ratio', 0)
        
        if pe < 15:
            return Signal(
                direction='bullish',
                confidence=0.8,
                reasoning=f'Undervalued: PE={pe}'
            )
        elif pe > 30:
            return Signal(
                direction='bearish',
                confidence=0.7,
                reasoning=f'Overvalued: PE={pe}'
            )
        return Signal(
            direction='neutral',
            confidence=0.6,
            reasoning='Fair value'
        )

async def main():
    db = Database(Config.get_database_url())
    await db.connect()
    
    agent = ValueAgent()
    
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
AAPL: neutral (60%) - Fair value
MSFT: neutral (60%) - Fair value
TSLA: bearish (70%) - Overvalued: PE=52.3
JPM: bullish (80%) - Undervalued: PE=11.2
```

**[Complete Framework Guide →](docs/FRAMEWORK_QUICKSTART.md)**

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
- **Document processing** with RAG
- **Python basics** (by viewing generated code)
- **Database queries** and data management
- **Async programming** patterns

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
**Setup:** Ollama (free) or OpenAI/Anthropic (paid)

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
- ✅ Import as library (`pip install`)
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
1. Run `./gui/setup.sh` (10 min)
2. Create rule-based agent (30 min)
3. Test with sample data (20 min)
4. Try example strategies (1 hour)

**Week 2:**
5. Setup Ollama (10 min)
6. Create AI-powered agent (30 min)
7. Compare AI vs rules (20 min)

**Week 3+:**
8. Create hybrid agent (30 min)
9. Upload and analyze PDFs (45 min)
10. Build custom strategy (2 hours)

**Total:** 8-12 hours over 3 weeks

---

### For Framework Users (Python)

**Day 1:**
1. `pip install -e ".[all]"` (5 min)
2. Run `examples/01_basic.py` (5 min)
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

## 🎯 Quick Commands Reference

### GUI Users
```bash
./gui/setup.sh            # One-time setup
./gui/launch.sh           # Launch GUI
```

### Framework Users  
```bash
pip install -e ".[all]"         # Install everything
pip install -e ".[dev]"         # Install with dev tools
pip install -e .                # Core only

python examples/01_basic.py     # Run example
python -m agent_framework.api   # Start API server
pytest tests/ -v                # Run tests
```

### Database (Optional)
```bash
docker compose up -d postgres   # Start PostgreSQL
python seed_data.py             # Add sample data
docker compose down             # Stop services
```

---

## 📖 Documentation

### For GUI Users
- [GUI Quick Start](GUI_QUICK_START.md) - Visual interface walkthrough
- Creating agents visually with forms
- Testing agents with mock/real data

### For Framework Users
- [Framework Quick Start](docs/FRAMEWORK_QUICKSTART.md) - Pip install & code
- [API Reference](docs/API_REFERENCE.md) - Complete API documentation
- [Integration Patterns](docs/INTEGRATION_PATTERNS.md) - Real-world usage
- [Example Code](examples/README.md) - Working examples

### For Both
- [Getting Started](docs/GETTING_STARTED.md) - Installation overview
- [Configuration](docs/CONFIGURATION.md) - Environment settings
- [Database Setup](docs/DATABASE_SETUP.md) - PostgreSQL guide
- [LLM Customization](docs/LLM_CUSTOMIZATION.md) - AI configuration
- [Choosing Agent Type](docs/CHOOSING_AGENT_TYPE.md) - Which to use
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues

---

## 🎓 For Universities & Educators

**For GUI-based courses:**
- ✅ Zero coding barrier
- ✅ Setup: Two commands
- ✅ Immediate results

**For programming courses:**
- ✅ Standard pip install
- ✅ Real-world framework design
- ✅ Production patterns (async, typing, testing)

**[University Setup Guide →](docs/UNIVERSITY_SETUP.md)**

---

## 🤝 Contributing

- 🐛 **Report bugs** - [GitHub Issues](https://github.com/thesisai-hq/AI-Agent-Builder/issues)
- 📖 **Improve docs** - Pull requests welcome
- 🎓 **Add examples** - Share your strategies
- 💡 **Suggest features** - [Discussions](https://github.com/thesisai-hq/AI-Agent-Builder/discussions)

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📜 License

MIT License - Free to use, modify, and distribute. See [LICENSE](LICENSE).

**Educational Disclaimer:** Not financial advice. For learning only. See [DISCLAIMER.md](DISCLAIMER.md).

---

*Interested in production trading tools? [thesis-app is coming soon](THESIS_APP.md).*
