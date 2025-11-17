# AI Agent Builder - Learn Investment Analysis with AI

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![For Education](https://img.shields.io/badge/use-education%20only-orange.svg)](DISCLAIMER.md)

**Build AI-powered stock analysis agents** - No coding experience required!

Perfect for:
- 📚 Finance students learning investment analysis
- 🎓 University courses on quantitative finance
- 🤖 Anyone curious about AI in investing

---

## ⚠️ Educational Tool Only

This is a **learning tool for finance education**. Not for real trading.

- ❌ **NOT financial advice** - For learning only
- ❌ **NOT for real trading** - Theoretical exercises only
- ✅ **FOR education** - Learn investment concepts with AI

**See [DISCLAIMER.md](DISCLAIMER.md) for complete legal terms**

---

## 🚀 Quick Start (5 Minutes)

### 1. Install

```bash
git clone https://github.com/yourusername/AI-Agent-Builder.git
cd AI-Agent-Builder
pip install -e ".[all]"
```

### 2. Setup Database

```bash
cp .env.example .env
docker compose up -d postgres
python seed_data.py
```

### 3. Launch Visual GUI

```bash
./gui/launch.sh
```

Opens at: **http://localhost:8501**

**Done!** Start creating agents visually - no coding needed!

---

## 🎓 What You'll Learn

### Finance Concepts
- Value investing (Warren Buffett, Benjamin Graham)
- Growth investing (Peter Lynch, GARP)
- Risk assessment and portfolio construction
- SEC filing analysis
- Multi-factor investment strategies

### AI/Tech Skills (Optional)
- Using AI for analysis (ChatGPT, Claude, LLaMA)
- Prompt engineering
- Document processing with RAG
- Python basics (by viewing generated code)
- Database queries

**You can use the visual GUI without any coding knowledge!**

---

## 🤖 Agent Types

Create four types of agents visually:

### 📊 Rule-Based (Start Here!)

**What:** Follows clear rules you define
**Example:** "Buy if PE < 15 AND ROE > 15%"
**Setup:** None - works immediately!
**Best for:** Learning basics, fast screening

### 🧠 LLM-Powered (AI Intelligence)

**What:** Uses AI (ChatGPT, Claude, LLaMA) for analysis
**Example:** "Apple shows strong competitive moat with 28% ROE..."
**Setup:** Install Ollama (free) or use OpenAI/Anthropic (paid)
**Best for:** Deep analysis, complex reasoning

### 📄 RAG-Powered (Document Analysis)

**What:** Analyzes long documents (SEC filings, reports)
**Example:** Extract insights from 100-page 10-K filing
**Setup:** Same as LLM (Ollama recommended)
**Best for:** Research, due diligence, document review

### 🔀 Hybrid (Best of Both)

**What:** Rules for screening + AI for deep analysis
**Example:** Filter 1000 stocks → AI analyzes top 50
**Setup:** Same as LLM (Ollama recommended)
**Best for:** Large-scale analysis, cost efficiency (95% cheaper)

[Complete Comparison](docs/CHOOSING_AGENT_TYPE.md)

---

## 🎨 Visual GUI Features

**No coding required!** Create agents through forms:

- 📋 **Browse** - Example strategies (Buffett, Lynch, Graham)
- ➕ **Create** - Build agents with visual forms
- 🧪 **Test** - Try with mock data or real data (YFinance)
- 👁️ **View Code** - See and learn from generated Python code
- 📄 **Upload PDFs** - Analyze SEC filings with RAG agents
- ⚙️ **LLM Setup** - Step-by-step wizard for AI setup
- 💾 **Save** - Agents saved to `examples/` folder

**See code, learn Python, but use GUI for everything!**

---

## 📚 Learning Path

### Week 1: Basics (No AI Setup)
```
1. Launch GUI → Create rule-based agent (30 min)
2. Test with mock data → Understand signals (20 min)
3. View generated code → See Python basics (30 min)
4. Try example strategies → Buffett, Lynch (1 hour)
```

**No AI setup needed yet!**

### Week 2: AI Intelligence
```
5. Install Ollama using wizard (10 min)
6. Create LLM-powered agent (30 min)
7. Compare LLM vs Rules on same stock (20 min)
8. Try different AI "personalities" (1 hour)
```

**Uses free Ollama - no costs!**

### Week 3+: Advanced
```
9. Create Hybrid agent (efficiency) (30 min)
10. Upload PDF → Analyze with RAG (45 min)
11. Build custom investment strategy (2 hours)
12. Compare multiple agents (ongoing)
```

---

## 💡 Simple Example

Even without coding, here's what the GUI generates:

```python
# You create this in GUI by clicking forms
# GUI generates this Python code automatically

class ValueAgent(Agent):
    """Buy undervalued stocks."""
    
    async def analyze(self, ticker, data):
        pe = data.get('pe_ratio', 0)
        
        if pe < 15:
            return Signal('bullish', 0.8, f'Undervalued: PE={pe}')
        return Signal('neutral', 0.5, 'Fair value')
```

**You can:**
- ✅ Create this in GUI without coding
- ✅ View the code to learn Python
- ✅ Download and modify if you want
- ✅ Or just use it without ever seeing code!

---

## 🔧 Setup Options

### Option A: Automatic (Recommended)

```bash
./gui/setup.sh    # Installs everything
./gui/launch.sh   # Start GUI
```

**Installs:**
- GUI (Streamlit)
- All LLM providers (Ollama, OpenAI, Anthropic)
- RAG support (document analysis)
- PDF processing
- YFinance (real market data)

**Everything works after setup!**

### Option B: Manual

```bash
# Core framework
pip install -e ".[all]"

# Database
docker compose up -d postgres
python seed_data.py

# For LLM agents (optional - do later)
# Follow wizard in GUI: ⚙️ LLM Setup
```

[Complete Installation Guide](docs/GETTING_STARTED.md)

---

## 📖 Documentation

### For Students
- [Quick Start](QUICK_START.md) - 5-minute setup
- [GUI Quick Start](GUI_QUICK_START.md) - Visual interface guide
- [How to Use Agents](gui/how_to_page.py) - Complete tutorial (in GUI)
- [Choosing Agent Type](docs/CHOOSING_AGENT_TYPE.md) - Which to use when

### For Learning Python
- [View Agent Code](gui/code_viewer.py) - Educational code viewer
- [Examples](examples/) - Buffett, Lynch, Graham strategies
- [Agent Guidelines](docs/AGENT_FILE_GUIDELINES.md) - Code patterns

### Technical Reference
- [LLM Customization](docs/LLM_CUSTOMIZATION.md) - AI configuration
- [API Reference](docs/API_REFERENCE.md) - REST API docs
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues

---

## 🎓 For Universities

### Why Use in Your Course?

- ✅ **No coding required** - Students use visual GUI
- ✅ **Code visibility** - Can view/learn Python optionally
- ✅ **Real strategies** - Buffett, Lynch, Graham examples
- ✅ **Modern AI** - Learn LLMs, RAG, hybrid systems
- ✅ **Free tools** - Ollama for AI, PostgreSQL for data
- ✅ **Safe learning** - Mock data, clear disclaimers

### Course Integration

**Quantitative Finance Course:**
- Week 1-2: Rule-based agents (quantitative screening)
- Week 3-4: LLM agents (AI in finance)
- Week 5-6: RAG agents (document analysis, research)
- Week 7-8: Student projects (build custom strategies)

**Python for Finance Course:**
- Students create agents in GUI (no code)
- View generated code to learn Python
- Modify code to learn programming
- Build increasingly complex agents

**Investment Analysis Course:**
- Learn by implementing famous strategies
- Test strategies on sample data
- Compare different approaches
- Understand limitations of systematic investing

### Classroom Setup

```bash
# One-time server setup
git clone https://github.com/yourusername/AI-Agent-Builder.git
cd AI-Agent-Builder
./gui/setup.sh

# Students access at:
http://your-server:8501
```

**Each student can:**
- Create and save their own agents
- Test with mock or real data
- View and learn from code
- Download their work

---

## 🤝 Contributing

Help make this better for students worldwide!

- 🐛 Report bugs
- 📖 Improve documentation
- 🎓 Add example strategies
- 💡 Suggest features
- 🔧 Submit pull requests

See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📜 License

**MIT License** - Free to use, modify, and distribute

Copyright (c) 2025 ThesisAI LLC

See [LICENSE](LICENSE) for details.

### What This Means

You can:
- ✅ Use for personal or educational projects
- ✅ Modify the code however you want
- ✅ Use in university courses
- ✅ Build upon it for research

Just include the license and copyright notice.

---

## ⚠️ Disclaimer

### Educational Use Only

This software:
- ❌ Does NOT provide financial advice
- ❌ Is NOT for real trading
- ❌ Has NO warranties

Before real investing:
- ✅ Consult licensed financial advisors
- ✅ Understand all risks
- ✅ Never invest money you can't afford to lose

[Full Disclaimer](DISCLAIMER.md)

---

## 💬 Get Help

- 📖 [Documentation](docs/)
- ⚙️ [LLM Setup Wizard](gui/llm_setup_wizard.py) - In GUI
- ❓ [Troubleshooting](docs/TROUBLESHOOTING.md)
- 🐛 [Report Issues](https://github.com/yourusername/AI-Agent-Builder/issues)

---

## 🚀 Production Ready?

**This tool is for learning.** For real trading, you need:
- Professional risk management
- Real-time data feeds
- Regulatory compliance
- Production support

**Check out [thesis-app](https://thesisai.app)** for production-ready investment tools.

---

## 🙏 Acknowledgments

Inspired by legendary investors:
- **Warren Buffett** - Quality and value investing
- **Peter Lynch** - Growth at reasonable price
- **Benjamin Graham** - Value investing principles

Built for education. Maintained by [ThesisAI](https://thesisai.app).

---

## 🎯 Quick Reference

**Three steps to start:**
```bash
./gui/setup.sh    # Setup (one-time)
./gui/launch.sh   # Launch GUI
```

**In GUI:**
- Create Rule-Based agent → Works immediately ✅
- Create LLM agent → Use wizard: ⚙️ LLM Setup
- View any code → Click 👁️ View button
- Test with data → Mock or real (YFinance)

**Get help:**
- In GUI: Click "📚 How to Use Agents"
- In GUI: Click "⚙️ LLM Setup" for AI setup
- Docs: [Documentation](docs/)

---

**Learn investing. Learn AI. Learn coding (optional).** 🚀

[Get Started](QUICK_START.md) | [GUI Guide](GUI_QUICK_START.md) | [Documentation](docs/)
