# GUI Quick Start

Build AI agents visually with no coding required.

---

## Setup & Launch

```bash
cd ~/AI-Agent-Builder

# One-time setup (installs ALL dependencies)
./gui/setup.sh

# Launch GUI
./gui/launch.sh
```

**What setup.sh installs:**
- ✅ Framework core (FastAPI, Database, Pydantic)
- ✅ GUI (Streamlit, PyPDF2)
- ✅ All LLM providers (Ollama, OpenAI, Anthropic)
- ✅ RAG support (sentence-transformers for document analysis)

**Everything is installed automatically!** You can use all agent types immediately.

Opens at: `http://localhost:8501`

---

## Additional Setup for LLM Agents

**For Ollama (Free, Local AI):**

The Ollama Python package is installed, but you also need the Ollama service:

```bash
# 1. Install Ollama service (one-time)
curl https://ollama.ai/install.sh | sh

# 2. Download a model (one-time)
ollama pull llama3.2

# 3. Start Ollama service (each time you use it)
ollama serve  # Keep this running in a separate terminal
```

**For OpenAI or Anthropic:**

Add your API key to `.env` file:

```bash
# Edit .env
nano .env

# Add your key:
OPENAI_API_KEY=sk-your-key-here
# or
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Rule-Based agents work immediately** with no additional setup!

---

## Create Your First Agent

### 1. Navigate
Click "➕ Create Agent" in sidebar

### 2. Configure
```
Agent Name: ValueAgent
Description: Buys undervalued stocks
Filename: value_agent.py
Type: Rule-Based
```

### 3. Add Rule
```
Metric: pe_ratio
Operator: <
Threshold: 15
Signal: bullish
Confidence: 0.8
```

### 4. Generate & Save
- Click "Generate Code"
- Review the code
- Click "💾 Save Agent"
- Done! File saved to `examples/`

---

## Test Your Agent

### For Rule-Based/LLM Agents

#### 1. Navigate
Click "🧪 Test Agent"

#### 2. Configure
```
Select Agent: ValueAgent
Ticker: AAPL
Use Mock Data: ✓
PE Ratio: 12
```

#### 3. Run
Click "🚀 Run Analysis"

#### 4. Result
```
Signal: 🟢 BULLISH
Confidence: 80%
Reasoning: Pe Ratio 12.0 is bullish
```

---

### For RAG Agents

#### 1. Navigate
Click "🧪 Test Agent"

#### 2. Select RAG Agent
```
Select Agent: SECAnalystAgent
Ticker: AAPL
```

#### 3. Upload PDF
**Drag and drop a PDF file:**
- SEC 10-K filing
- Earnings report
- News articles
- Research reports

#### 4. Run
Click "🚀 Run Analysis"

#### 5. Result
```
Signal: 🟢 BULLISH
Confidence: 75%
Reasoning: Strong growth prospects...

Detailed Insights:
  • Financial performance shows 15% revenue growth
  • Key risks include supply chain dependencies
  • Growth strategies focus on AI integration
```

---

## Backtest Your Agent

### Navigate
Click "📈 Backtest Agent" in sidebar

### Select Agent
```
Select Agent: ValueAgent
Data Source: Mock Data (Scenarios)
```

### Run Backtest
Click "🚀 Run Backtest"

### Results
```
Total Signals: 5
Avg Confidence: 75%
Bullish Signals: 60%

Signal Distribution:
🟢 Bullish: 3 (60%)
🔴 Bearish: 1 (20%)
🟡 Neutral: 1 (20%)

Interpretation: Balanced strategy
```

**What backtesting shows:**
- ✅ Signal distribution across scenarios
- ✅ Average confidence levels
- ✅ How rules perform on different market conditions

**What it does NOT show:**
- ❌ Actual profit/loss (educational only)
- ❌ Transaction costs or slippage
- ❌ Real market conditions

⚠️ **Remember:** This is for learning! Past performance doesn't guarantee future results.

---

## Troubleshooting

### GUI Won't Start

```bash
# Reinstall GUI dependencies
pip install --upgrade streamlit pypdf2

# Verify
streamlit --version
```

### "No module named" Errors

If you see module errors, re-run setup:

```bash
./gui/setup.sh
```

This installs ALL dependencies including:
- Ollama (local AI)
- OpenAI (ChatGPT API)
- Anthropic (Claude API)
- sentence-transformers (document analysis)

### LLM Agents Not Working

**For Ollama:**
```bash
# Check if Ollama service is running
curl http://localhost:11434/api/tags

# If not, start it:
ollama serve  # Keep running in separate terminal

# Check if model is downloaded
ollama list | grep llama3.2

# If not, download it:
ollama pull llama3.2
```

**For OpenAI/Anthropic:**
```bash
# Check .env file has your API key
cat .env | grep API_KEY

# Add if missing:
nano .env
# OPENAI_API_KEY=sk-your-key-here
```

### RAG Agents Not Working

**Error: "No module named 'sentence_transformers'"**

This should not happen if you ran `./gui/setup.sh`. If it does:

```bash
# Manual install
pip install sentence-transformers

# Or reinstall everything
pip install -e ".[all]"
```

### PDF Upload Errors

```bash
# Install PyPDF2 if missing
pip install pypdf2

# Verify
python3 -c "import PyPDF2; print('OK')"
```

### Files Not Saving

```bash
# Check directory exists and has permissions
ls -ld examples/
chmod 755 examples/

# Test
python3 gui/test_setup.py
```

**For more help:** See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

## Agent Types Explained

### Rule-Based ✨
- **Setup needed:** None (works immediately)
- **Use for:** Clear investment criteria, fast screening
- **Example:** Buy stocks with PE < 15

### LLM-Powered 🤖
- **Setup needed:** Ollama service + model (see above)
- **Use for:** Deep analysis, complex reasoning
- **Example:** Analyze company quality holistically

### Hybrid ⚡
- **Setup needed:** Ollama service + model (see above)
- **Use for:** Large-scale screening + selective deep analysis
- **Example:** Screen 500 stocks → Analyze top 20

### RAG-Powered 📄
- **Setup needed:** Ollama service + model (see above)
- **Use for:** Document analysis (PDFs, SEC filings)
- **Example:** Extract insights from 10-K filing

**All packages are already installed by setup.sh!** You just need to:
- Start Ollama service (for LLM/Hybrid/RAG)
- Add API keys (for OpenAI/Anthropic)

---

## Quick Start Tips

### For Beginners
1. **Start with Rule-Based** - Works immediately, no LLM needed
2. **Test with mock data** - No database required
3. **Try the examples** - Buffett, Lynch, Graham strategies included

### For Advanced Users
1. **Set up Ollama** - Free local AI for LLM agents
2. **Create Hybrid agents** - Best performance for production
3. **Upload PDFs** - Analyze real SEC filings with RAG

### For thesis-ai Integration
```python
# Import generated agents in thesis-ai
from AI_Agent_Builder.examples.value_agent import ValueAgent

agent = ValueAgent()
signal = agent.analyze('AAPL', data)
```

---

## Full Documentation

See `gui/README.md` for complete documentation.

**Having issues?** See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

## ⚖️ Legal & License

**Educational use only.** This GUI and framework are for learning purposes only.

- **Disclaimer:** [DISCLAIMER.md](DISCLAIMER.md) - Complete legal terms
- **License:** [LICENSE](LICENSE) - MIT License  
- **Not financial advice** - Do not use for real trading

**GUI is part of the AI-Agent-Builder framework** and subject to the same MIT License.

Copyright (c) 2025 ThesisAI LLC

**For production systems:** [thesis-app](https://thesisai.app)

---

## Quick Reference

**Three steps to start:**
1. Run setup: `./gui/setup.sh` (installs everything)
2. Start Ollama: `ollama serve` (for LLM agents)
3. Launch GUI: `./gui/launch.sh`

**Create agents:**
- Rule-Based: Ready immediately ✅
- LLM/Hybrid/RAG: Needs Ollama running ⚡

**Get help:**
- Setup issues: `python3 gui/test_setup.py`
- Dependencies: All installed by setup.sh ✅
- Troubleshooting: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
