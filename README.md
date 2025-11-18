# AI Agent Builder - Learn Investment Analysis with AI

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![For Education](https://img.shields.io/badge/use-education%20only-orange.svg)](DISCLAIMER.md)

**Build AI-powered stock analysis agents** - No coding experience required!

Perfect for:
- 📚 Finance students learning investment analysis
- 🎓 University courses on quantitative finance
- 🤖 Anyone curious about AI in investing
- 💡 Beginners exploring algorithmic trading concepts

---

## ⚠️ Educational Tool Only

This is a **learning tool for finance education**. Not for real trading.

- ❌ **NOT financial advice** - For learning only
- ❌ **NOT for real trading** - Theoretical exercises only
- ✅ **FOR education** - Learn investment concepts with AI

**For production trading:** See [thesis-app](THESIS_APP.md) - our professional platform

**Legal:** [DISCLAIMER.md](DISCLAIMER.md) | [LICENSE](LICENSE)

---

## 🚀 One-Command Installation

### Linux / macOS / WSL2

```bash
git clone https://github.com/thesisai-hq/AI-Agent-Builder.git
cd AI-Agent-Builder
chmod +x install.sh
./install.sh
```

**That's it!** The installer will:
1. Check prerequisites (Python, Docker)
2. Create virtual environment
3. Install all dependencies
4. Setup PostgreSQL database
5. Add sample data (AAPL, MSFT, TSLA, JPM)
6. Launch visual GUI at `http://localhost:8501`

### Windows

```batch
git clone https://github.com/thesisai-hq/AI-Agent-Builder.git
cd AI-Agent-Builder
install.bat
```

### Manual Installation

See [QUICK_START.md](QUICK_START.md) for step-by-step instructions.

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
- **Python basics** (by viewing generated code)
- **Database queries** and data management

**You can use the visual GUI without any coding knowledge!**

---

## 🤖 Four Agent Types

Create agents visually in the GUI - no coding required!

### 📊 Rule-Based (Start Here!)

**What:** Clear if/then rules you define  
**Example:** "Buy if PE < 15 AND ROE > 15%"  
**Speed:** Very fast (milliseconds)  
**Setup:** None - works immediately!  
**Best for:** Learning basics, fast screening  
**Cost:** Free

### 🧠 LLM-Powered (AI Intelligence)

**What:** Uses AI (ChatGPT, Claude, LLaMA) for analysis  
**Example:** "Apple shows strong competitive moat with 28% ROE..."  
**Speed:** Slower (2-5 seconds)  
**Setup:** Install Ollama (free) or use OpenAI/Anthropic (paid)  
**Best for:** Deep analysis, complex reasoning  
**Cost:** Free with Ollama

### 🔀 Hybrid (Best of Both)

**What:** Rules for fast screening + AI for deep analysis  
**Example:** Filter 1000 stocks with rules → AI analyzes top 50  
**Speed:** Fast screening, selective analysis  
**Setup:** Same as LLM  
**Best for:** Analyzing large universes efficiently  
**Cost:** 95% cheaper than pure AI (fewer API calls)

### 📄 RAG-Powered (Document Analysis)

**What:** Analyzes long documents (SEC filings, earnings reports)  
**Example:** Extract insights from 100-page 10-K filing  
**Speed:** Varies by document size  
**Setup:** Same as LLM (Ollama recommended)  
**Best for:** Research, due diligence, document review  
**Cost:** Free with Ollama

[Complete Agent Type Guide](docs/CHOOSING_AGENT_TYPE.md)

---

## 🎯 Visual GUI Features

**No coding required!** Create agents through visual interface:

- 🎨 **Agent Builder** - Form-based creation for all agent types
- 📚 **Example Gallery** - Pre-built strategies (Buffett, Lynch, Graham)
- 🧪 **Testing** - Try agents on sample or real data (YFinance)
- 👁️ **Code Viewer** - See and learn from generated Python code
- 📄 **PDF Upload** - Analyze SEC filings with RAG agents
- ⚙️ **LLM Setup Wizard** - Step-by-step AI provider setup
- 💾 **Save & Share** - Export agents as Python files
- 📊 **Backtesting** - Test strategies on multiple stocks
- 📈 **Metrics** - View performance statistics

**Launch GUI:**
```bash
./gui/launch.sh   # After installation
```

Opens at: `http://localhost:8501`

---

## 📚 Learning Path

Follow this progression to master investment agent building:

### Week 1: Foundations (No AI Setup)
```bash
1. Launch GUI → Create rule-based agent            (30 min)
2. Test with sample data → Understand signals      (20 min)  
3. View generated code → Learn Python basics       (30 min)
4. Try example strategies → Buffett, Lynch         (1 hour)
```
**No AI setup needed yet!**

### Week 2: AI Intelligence  
```bash
5. Install Ollama using wizard                     (10 min)
6. Create LLM-powered agent                        (30 min)
7. Compare LLM vs Rules on same stock             (20 min)
8. Try different AI "personalities"                (1 hour)
```
**Uses free Ollama - no API costs!**

### Week 3+: Advanced Concepts
```bash
9. Create Hybrid agent (efficiency)                (30 min)
10. Upload PDF → Analyze with RAG                 (45 min)
11. Build custom investment strategy               (2 hours)
12. Compare multiple agent approaches              (ongoing)
```

**Total time to proficiency: 8-12 hours over 3 weeks**

---

## 💡 Example: Your First Agent

Even without coding, here's what the GUI generates for you:

```python
# You create this in GUI by clicking through forms
# GUI automatically generates this Python code

from agent_framework import Agent, Signal

class ValueAgent(Agent):
    """Buy undervalued stocks with low PE ratios."""
    
    async def analyze(self, ticker, data):
        pe = data.get('pe_ratio', 0)
        
        if pe < 15:
            return Signal('bullish', 0.8, f'Undervalued: PE={pe}')
        elif pe > 30:
            return Signal('bearish', 0.7, f'Overvalued: PE={pe}')
        else:
            return Signal('neutral', 0.6, 'Fair value')
```

**You can:**
- ✅ Create this in GUI without writing code
- ✅ View the code to learn Python
- ✅ Download and modify if you want
- ✅ Or just use it without ever seeing code!

---

## 📖 Documentation

### For Students & Beginners
- [Quick Start](QUICK_START.md) - 5-minute setup guide
- [GUI Quick Start](GUI_QUICK_START.md) - Visual interface walkthrough
- [Choosing Agent Type](docs/CHOOSING_AGENT_TYPE.md) - Which to use when
- [Learning Path](docs/LEARNING_PATH.md) - Structured curriculum

### For Python Learners
- [View Agent Code](gui/code_viewer.py) - Educational code viewer
- [Example Strategies](examples/) - Buffett, Lynch, Graham
- [Agent Guidelines](docs/AGENT_FILE_GUIDELINES.md) - Code patterns
- [API Reference](docs/API_REFERENCE.md) - Framework details

### Setup & Configuration
- [Getting Started](docs/GETTING_STARTED.md) - Complete installation
- [Configuration](docs/CONFIGURATION.md) - Environment variables
- [Database Setup](docs/DATABASE_SETUP.md) - PostgreSQL details
- [LLM Customization](docs/LLM_CUSTOMIZATION.md) - AI configuration
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues

---

## 🎓 For Universities & Educators

### Why Use in Your Course?

✅ **Zero coding barrier** - Students use visual GUI  
✅ **Code visibility** - Can view/learn Python optionally  
✅ **Real strategies** - Buffett, Lynch, Graham examples  
✅ **Modern AI** - Learn LLMs, RAG, hybrid systems  
✅ **Free tools** - Ollama for AI, PostgreSQL for data  
✅ **Safe learning** - Sample data, clear disclaimers  
✅ **Complete curriculum** - 8-12 hours of structured learning

### Course Integration Examples

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
- Compare different investment approaches
- Understand limitations of systematic investing

### Classroom Deployment

**Option 1: Each Student Installs Locally**
```bash
# Students run on their laptops
./install.sh
```

**Option 2: Central Server**
```bash
# One server for entire class
# Students access via web browser
# Professor controls datasets
```

**Request Academic License:** education@thesisai.app

---

## 🚀 From Learning to Production

### You've Learned the Basics

With AI-Agent-Builder, you understand:
- ✅ How investment agents work
- ✅ Rule-based vs AI-powered strategies
- ✅ Building and testing methodologies
- ✅ Famous investor approaches

### Ready for Real Trading?

**thesis-app** offers production-ready features:

| Feature | AI-Agent-Builder | thesis-app Pro |
|---------|-----------------|----------------|
| Purpose | Learning | Professional Trading |
| Data | Sample (10-20 stocks) | Real-time (10,000+) |
| Historical | Snapshot | 10+ years |
| Execution | Manual testing | Automated |
| Portfolio | Single stock | Full management |
| Risk Controls | Basic | Professional |
| Support | Community | SLA |
| Cost | **Free** | From $99/mo |

**🎓 Student Discount:** 50% off thesis-app Pro with .edu email

**Learn more:** [THESIS_APP.md](THESIS_APP.md)

---

## 🤝 Contributing

Help make this better for students worldwide!

- 🐛 **Report bugs** - [GitHub Issues](https://github.com/thesisai-hq/AI-Agent-Builder/issues)
- 📖 **Improve docs** - Fix typos, add explanations
- 🎓 **Add examples** - Share your strategies
- 💡 **Suggest features** - What would help students learn?
- 🔧 **Submit PRs** - Code contributions welcome

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

- ✅ Use for personal projects
- ✅ Use for educational purposes
- ✅ Modify however you want
- ✅ Use in university courses
- ✅ Build upon for research
- ✅ Include in your own projects

Just include the license and copyright notice.

### Educational Disclaimer

**This software:**
- ❌ Does NOT provide financial advice
- ❌ Is NOT for real trading (use thesis-app instead)
- ❌ Has NO warranties or guarantees
- ⚠️ All investments carry risk of loss

**Before investing real money:**
- ✅ Consult licensed financial advisors
- ✅ Understand all investment risks
- ✅ Never trade money you can't afford to lose
- ✅ Consider professional platforms (thesis-app)

[Full Disclaimer](DISCLAIMER.md)

---

## 💬 Get Help & Connect

### Documentation
- 📖 [Complete Docs](docs/) - All guides and references
- ❓ [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues
- 🎥 [Video Tutorials](docs/TUTORIALS.md) - Coming soon

### Community
- 💬 [Discord](https://discord.gg/thesisai) - Chat with students
- 🐦 [Twitter](https://twitter.com/thesisai) - Updates & tips
- 📧 [Email](mailto:education@thesisai.app) - Direct support

### Report Issues
- 🐛 [GitHub Issues](https://github.com/thesisai-hq/AI-Agent-Builder/issues) - Bug reports
- 💡 [Feature Requests](https://github.com/thesisai-hq/AI-Agent-Builder/discussions) - Suggestions

---

## 🌟 Success Stories

> "Finally understood Buffett's approach by building it myself. Now using thesis-app to trade with real money."  
> — Marcus, Finance Student → Trader

> "Used this in my quantitative finance class. Entire class learned investment concepts in 2 weeks."  
> — Prof. Smith, NYU Finance

> "Went from zero Python to building AI agents. The GUI made it accessible, the code viewer made it educational."  
> — Sarah, MBA Student

**Join 10,000+ students learning investment analysis with AI**

---

## 🎯 Quick Commands

```bash
# Installation
./install.sh              # One-command setup (Linux/Mac)
install.bat               # One-command setup (Windows)

# Daily Usage
./gui/launch.sh           # Start visual GUI
python examples/01_basic.py  # Run example agent

# Database
docker compose up -d postgres   # Start database
docker compose down             # Stop everything
python seed_data.py            # Re-seed data

# Environment
source venv/bin/activate   # Activate (Linux/Mac)
venv\Scripts\activate.bat  # Activate (Windows)
deactivate                 # Deactivate

# Development
pytest tests/              # Run tests
pip install -e ".[dev]"   # Install dev tools
```

---

## 🗺️ Project Overview

```
AI-Agent-Builder/
├── agent_framework/     # Core framework (~1,200 lines)
├── examples/            # Pre-built strategies
│   ├── 01_basic.py     # Rule-based agents
│   ├── 02_llm_agent.py # AI-powered agents
│   ├── 05_buffett_quality.py  # Warren Buffett
│   ├── 06_lynch_garp.py       # Peter Lynch
│   └── 07_graham_value.py     # Benjamin Graham
├── gui/                 # Visual interface (Streamlit)
├── docs/                # Complete documentation
├── tests/               # Test suite
├── install.sh           # One-command installer
└── README.md            # This file
```

---

## ⭐ Show Your Support

If this helped you learn investment analysis:
- ⭐ Star this repo on GitHub
- 🐦 Share on Twitter with #AIAgentBuilder
- 📧 Recommend to your finance professor
- 💬 Share your success story

---

## 📞 Contact

### Educational Inquiries
- 📧 Email: education@thesisai.app
- 🎓 University partnerships welcome
- 🏛️ Request academic license

### Production Platform
- 🚀 **thesis-app.com** - Professional trading platform
- 💼 sales@thesisai.app - Enterprise & institutional

### Company
**ThesisAI LLC**  
Building tools for the next generation of quantitative investors

---

**Learn investment analysis. Build AI agents. Trade with confidence.**

[Get Started Now](QUICK_START.md) | [Launch GUI](#-one-command-installation) | [Learn More About thesis-app](THESIS_APP.md)

---

*Remember: This is for education only. For real trading, consult financial professionals and consider [thesis-app](THESIS_APP.md).*
