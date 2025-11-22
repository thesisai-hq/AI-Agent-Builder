# GUI Quick Start - Visual Agent Builder

Build investment agents with no coding required.

---

## 🚀 Setup & Launch (5 Minutes)

```bash
cd AI-Agent-Builder

# One-time setup (installs EVERYTHING)
./gui/setup.sh

# Launch GUI
./gui/launch.sh
```

**Opens at:** http://localhost:8501

**That's it!** Start creating agents visually.

---

## What Gets Installed

The `./gui/setup.sh` script installs everything you need:

✅ **GUI** (Streamlit, PyPDF2)
✅ **All LLM providers** (Ollama, OpenAI, Anthropic packages)
✅ **RAG support** (sentence-transformers for document analysis)
✅ **Data sources** (YFinance for real market data)
✅ **All dependencies** - No "optional" packages!

**After setup, all agent types work!**

---

## 🔧 Additional Setup for AI Agents

**Rule-Based agents work immediately** - no extra setup needed!

**For LLM/RAG/Hybrid agents, you also need:**

### Option A: Ollama (Free, Local) - Recommended

The Python package is installed, but you also need the Ollama service:

```bash
# 1. Install Ollama service (one-time)
curl https://ollama.ai/install.sh | sh

# 2. Download AI model (one-time, ~4GB)
ollama pull llama3.2

# 3. Start service (each time you use LLM agents)
ollama serve  # Keep this running in a terminal
```

**Or use the visual wizard:**
1. Launch GUI
2. Click **"⚙️ LLM Setup"** in sidebar
3. Follow step-by-step instructions
4. Test connection when done

### Option B: OpenAI/Anthropic (Cloud, Paid)

Add API key to `.env` file:

```bash
nano .env

# Add one of these:
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Or use the wizard** to configure automatically!

---

## 📚 GUI Overview

### Navigation

**📋 Browse Agents** - View and manage existing agents
- See all example strategies (Buffett, Lynch, Graham)
- View code with educational annotations
- Duplicate agents to create variations
- Download or delete agents

**➕ Create Agent** - Build new agents visually
- Choose type (Rule/LLM/RAG/Hybrid)
- Configure with forms (no coding!)
- Generate Python code automatically
- Save to `examples/` folder

**🧪 Test Agent** - Try agents with data
- Test with mock data (fictional)
- Test with YFinance (real market data)
- Upload PDFs (for RAG agents)
- See results and reasoning

**📚 How to Use Agents** - Complete tutorials
- Getting started guide
- Rule-based agent tutorial
- LLM agent tutorial
- RAG agent tutorial
- Hybrid agent tutorial
- Understanding signals

**⚙️ LLM Setup** - Interactive setup wizard
- Step-by-step Ollama installation
- Model download guidance
- Connection testing
- OpenAI/Anthropic configuration

---

## 🎯 Create Your First Agent (10 Minutes)

### 1. Launch GUI

```bash
./gui/launch.sh
```

### 2. Navigate to "➕ Create Agent"

### 3. Fill in the Form

**Basic Info:**
```
Agent Name: ValueHunter
Description: Finds undervalued quality stocks
Filename: value_hunter.py
Type: Rule-Based
```

**Add a Rule:**
```
Metric: pe_ratio
Operator: <
Threshold: 15
Signal: bullish
Confidence: 0.8
```

### 4. Generate & Save

- Click **"Generate Code"**
- Review the Python code (optional)
- Click **"💾 Save Agent"**

✅ **Done!** Your agent is created and saved!

### 5. Test Your Agent

- Go to **"🧪 Test Agent"**
- Select "ValueHunter"
- Choose "Mock Data"
- Set PE Ratio: 12
- Click **"🚀 Run Analysis"**

**Result:**
```
Signal: 🟢 BULLISH
Confidence: 80%
Reasoning: "PE ratio 12.0 is bullish"
```

---

## 🤖 Create an AI Agent (15 Minutes)

### Prerequisites

Install Ollama first (use the wizard!):
1. Click **"⚙️ LLM Setup"** in sidebar
2. Select "Ollama (Free, Local)"
3. Follow the 4 steps
4. Test connection ✅

### Create LLM Agent

**Navigate to "➕ Create Agent"**

**Fill in:**
```
Agent Name: AIValueInvestor
Description: AI-powered value analysis
Filename: ai_value_investor.py
Type: LLM-Powered

LLM Configuration:
Provider: ollama
Model: llama3.2
Temperature: 0.5
Max Tokens: 1500

System Prompt:
You are a value investor inspired by Warren Buffett.
Focus on business quality, competitive advantages,
and margin of safety. Be conservative but thorough.
```

**Generate & Save!**

### Test AI Agent

**Make sure Ollama is running:**
```bash
# In separate terminal
ollama serve
```

**Then in GUI:**
1. Go to "🧪 Test Agent"
2. Select "AIValueInvestor"
3. Choose data source (Mock or YFinance)
4. Click "Run Analysis"
5. Read AI's reasoning!

**AI provides detailed analysis:**
```
Signal: 🟢 BULLISH
Confidence: 75%

Reasoning: The company demonstrates exceptional business 
quality with ROE of 28% and margins of 25%, indicating 
strong competitive advantages. The PE ratio of 12 suggests 
undervaluation relative to quality. Debt levels at 0.8x 
are manageable. Good long-term value opportunity.
```

---

## 📄 Analyze Documents with RAG (20 Minutes)

### Create RAG Agent

**In "➕ Create Agent":**
```
Agent Name: SECAnalyst
Description: Analyzes SEC 10-K filings
Filename: sec_analyst.py
Type: RAG-Powered

LLM: ollama / llama3.2 / temp=0.5
RAG: chunk_size=300, overlap=50, top_k=3

System Prompt:
You are an SEC filing expert. Extract key financial 
trends, risks, and strategic initiatives from filings.
Be precise and cite specific details.
```

### Test with PDF

1. Go to "🧪 Test Agent"
2. Select "SECAnalyst"
3. **Upload PDF:**
   - Drag and drop a SEC 10-K filing
   - Or any financial document
4. Click "Run Analysis"

**RAG extracts insights:**
```
Detailed Insights:
1. Financial Performance: Revenue up 8% to $394B, 
   Services growing 16%...
2. Risk Factors: China supply chain concentration,
   EU regulatory scrutiny...
3. Growth Strategy: India expansion, Vision Pro launch,
   AI/ML R&D investment...

Signal: 🟢 BULLISH (70%)
```

---

## 👁️ View and Learn from Code

**Every agent you create:**
1. Click **"👁️ View"** button
2. See code broken into sections
3. Read explanations for each part
4. Download to experiment

**What you see:**
```
[Expandable] 1. Imports - Getting Tools
  → Explanation of imports
  → Learning tip

[Expandable] 4. Analysis Logic - THE BRAIN ⭐
  → This is where decisions happen
  → Learning tip: Focus here!

[Full Code with line numbers below]
```

**Benefits:**
- Understand code structure
- Learn Python by example
- See how your strategy becomes code
- Modify and experiment (optional)

---

## 🐛 Troubleshooting

### GUI Won't Start

```bash
# Reinstall dependencies
pip install -e ".[all]"

# Verify Streamlit
streamlit --version
```

### LLM Agents Not Working

**Use the wizard:**
1. Click "⚙️ LLM Setup" in sidebar
2. Follow Ollama setup
3. Test connection
4. Follow error messages if any

**Or manually:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve

# Check if model downloaded
ollama list

# If not, download it
ollama pull llama3.2
```

### Files Not Saving

```bash
# Check directory permissions
ls -ld examples/
chmod 755 examples/

# Test
python3 gui/test_setup.py
```

### More Help

- Check [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
- Use **⚙️ LLM Setup wizard** in GUI
- Review error messages (they include solutions!)

---

## 🎨 GUI Tips

### For Beginners
- ✅ Start with Rule-Based agents (no AI needed)
- ✅ Use mock data for testing
- ✅ View code to learn (but don't need to understand it)
- ✅ Try example strategies (duplicate and modify)

### For Learning AI
- ✅ Use the **⚙️ LLM Setup wizard**
- ✅ Start with Ollama (free!)
- ✅ Try different temperatures (0.3 vs 0.8)
- ✅ Compare LLM vs Rule agents on same stock

### For Advanced Users
- ✅ Create Hybrid agents (rules + AI)
- ✅ Upload real SEC filings (RAG)
- ✅ Download code and modify manually
- ✅ Integrate with your Python projects

---

## 📊 What Each Agent Type Can Do

| Type | Data Input | Output | Setup Time |
|------|-----------|--------|------------|
| **Rule-Based** | Mock or YFinance | Buy/Sell/Hold signal | 0 minutes |
| **LLM** | Mock or YFinance | AI reasoning + signal | 10 minutes* |
| **RAG** | PDF documents | Document insights + signal | 10 minutes* |
| **Hybrid** | Mock or YFinance | Filtered + AI analysis | 10 minutes* |

*Using Ollama wizard

---

## 🔗 Quick Links

**In the GUI:**
- **⚙️ LLM Setup** → Step-by-step AI configuration
- **📚 How to Use** → Complete tutorials
- **👁️ View** → See code with explanations

**Documentation:**
- [Full Setup Guide](docs/GETTING_STARTED.md)
- [Agent Type Comparison](docs/CHOOSING_AGENT_TYPE.md)
- [LLM Customization](docs/LLM_CUSTOMIZATION.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

---

## ⚖️ Legal

**Educational use only.** See [DISCLAIMER.md](DISCLAIMER.md) for complete terms.

**MIT License.** See [LICENSE](LICENSE) for details.

**For production:** [thesis-app](THESIS_APP.md) (coming soon)

---

## 🎉 You're Ready!

```bash
./gui/launch.sh
```

**Then:**
1. Create your first agent (Rule-Based recommended)
2. Test it with mock data
3. View the code to learn
4. Set up AI when ready (use wizard!)

**Have fun learning!** 🚀
