# Agent Builder GUI

Visual interface for creating and managing AI investment agents without coding.

---

## Quick Start

```bash
cd ~/AI-Agent-Builder

# One-time setup (installs ALL dependencies)
chmod +x gui/setup.sh gui/launch.sh
./gui/setup.sh

# Launch
./gui/launch.sh
```

**What gets installed:**
- ✅ GUI framework (Streamlit)
- ✅ PDF processing (PyPDF2)
- ✅ All LLM providers (Ollama, OpenAI, Anthropic)
- ✅ RAG support (sentence-transformers)
- ✅ Framework core (FastAPI, PostgreSQL, Pydantic)

**No optional dependencies!** Everything is installed for full functionality.

Opens at: `http://localhost:8501`

---

## Additional Setup for LLM Features

### For Ollama (Free, Local AI)

Python package is installed, but you need the Ollama service:

```bash
# Install Ollama (one-time)
curl https://ollama.ai/install.sh | sh

# Download model (one-time)
ollama pull llama3.2

# Start service (each session)
ollama serve  # Keep running in separate terminal
```

### For OpenAI or Anthropic

Add API key to `.env`:

```bash
nano .env
# Add: OPENAI_API_KEY=sk-your-key-here
# or: ANTHROPIC_API_KEY=sk-ant-your-key-here
```

---

## Features

### 📋 Browse Agents
- View all agents in `examples/` directory
- Search and filter
- Statistics dashboard (total, by type, custom count)
- Preview source code
- Duplicate agents for variations
- Export to share
- Delete with safety confirmations

### ➕ Create Agents

**Four agent types (all fully supported):**

1. **Rule-Based** - Visual rule builder
   - No LLM needed (works immediately)
   - Fast execution
   - Best for: Clear investment criteria
   - Advanced rules with AND/OR logic
   - Score-based strategies

2. **LLM-Powered** - AI-driven analysis
   - Requires: Ollama/OpenAI/Anthropic
   - Configurable temperature (creativity)
   - Custom system prompts (personality)
   - Best for: Complex, nuanced analysis

3. **Hybrid** - Rules + LLM
   - Requires: Ollama/OpenAI/Anthropic
   - Two-stage: Screen with rules → Analyze with LLM
   - Best for: Large-scale with depth

4. **RAG-Powered** - Document analysis
   - Requires: Ollama/OpenAI/Anthropic (already installed)
   - Analyzes PDFs, SEC filings, reports
   - Vector-based document search
   - Best for: Long documents, text analysis

### 🧪 Test Agents
- Mock data testing (no database needed)
- Real data testing (with database)
- PDF upload for RAG agents
- Execution timing
- Visual results with insights

### 📈 Backtest Agents
- Test on multiple scenarios
- Signal distribution analysis
- Average confidence calculation
- Educational backtesting (not production)

---

## Agent Type Comparison

| Type | Dependencies | Setup Difficulty | Best For |
|------|--------------|------------------|----------|
| **Rule-Based** | None | ⚡ Easy | Clear criteria, fast screening |
| **LLM-Powered** | Ollama service | ⚡⚡ Moderate | Deep analysis, small datasets |
| **Hybrid** | Ollama service | ⚡⚡ Moderate | Large-scale + depth |
| **RAG-Powered** | Ollama service | ⚡⚡ Moderate | Document analysis |

**All Python packages installed by setup.sh!** Only need to start Ollama service for LLM features.

---

## Creating Your First Agent

### Example: Value Agent (Rule-Based)

**No LLM needed - works immediately!**

1. Navigate to "➕ Create Agent"
2. Configure:
   ```
   Agent Name: ValueAgent
   Description: Buys undervalued stocks
   Filename: value_agent.py
   Type: Rule-Based
   ```
3. Add Rule:
   ```
   Metric: pe_ratio
   Operator: <
   Threshold: 15
   Signal: bullish
   Confidence: 0.8
   ```
4. Generate → Save

---

### Example: AI Quality Agent (LLM-Powered)

**Requires Ollama service running**

1. Start Ollama (separate terminal):
   ```bash
   ollama serve
   ```

2. Navigate to "➕ Create Agent"

3. Configure:
   ```
   Agent Name: QualityAgent
   Type: LLM-Powered
   Provider: ollama
   Model: llama3.2
   Temperature: 0.5
   ```

4. System Prompt:
   ```
   You are a quality-focused investor.
   Focus on strong ROE, margins, and low debt.
   Analyze companies for long-term potential.
   ```

5. Generate → Save

---

### Example: Document Analyzer (RAG)

**Requires Ollama service running**

1. Start Ollama:
   ```bash
   ollama serve
   ```

2. Navigate to "➕ Create Agent"

3. Configure:
   ```
   Agent Name: SECAnalystAgent
   Type: RAG-Powered
   Provider: ollama
   Model: llama3.2
   Chunk Size: 300
   ```

4. Generate → Save

5. Test with PDF upload in "🧪 Test Agent"

---

## Testing

### Rule-Based Agents
```bash
# Test immediately (no LLM needed)
python3 gui/test_setup.py
```

### LLM/Hybrid/RAG Agents
```bash
# 1. Start Ollama
ollama serve  # Separate terminal

# 2. Verify model
ollama list | grep llama3.2

# 3. Test agent in GUI
# Navigate to "🧪 Test Agent"
```

---

## Troubleshooting

### Setup Issues

**Dependencies not installed:**
```bash
# Rerun setup (installs everything)
./gui/setup.sh

# Verify
python3 gui/test_setup.py
```

### LLM Issues

**Ollama not working:**
```bash
# Check service is running
curl http://localhost:11434/api/tags

# Start if not running
ollama serve

# Check model exists
ollama list
```

**API key issues:**
```bash
# Check .env
cat .env | grep API_KEY

# Add if missing
nano .env
```

### RAG Issues

**sentence-transformers error:**
```bash
# Should not happen if you ran ./gui/setup.sh
# If it does, reinstall:
pip install sentence-transformers

# Verify
python3 -c "import sentence_transformers; print('OK')"
```

### File Issues

**Can't save agents:**
```bash
# Check permissions
ls -ld examples/
chmod 755 examples/

# Test
python3 gui/test_setup.py
```

**For complete troubleshooting:** [TROUBLESHOOTING.md](../docs/TROUBLESHOOTING.md)

---

## Integration with thesis-ai

```python
# Import generated agents
from AI_Agent_Builder.examples.value_agent import ValueAgent

# Use in orchestrator
agent = ValueAgent()
signal = agent.analyze('AAPL', data)
```

---

## Requirements

**Installed by setup.sh:**
- Python 3.10+
- Streamlit 1.28+
- PyPDF2 3.0+
- Ollama, OpenAI, Anthropic packages
- sentence-transformers
- AI-Agent-Builder framework

**Additional (manual):**
- Docker (for database)
- Ollama service (for LLM agents)
- API keys (for OpenAI/Anthropic)

---

## Commands

```bash
# Setup
./gui/setup.sh              # Install all dependencies
python3 gui/test_setup.py   # Verify setup

# Launch
./gui/launch.sh             # Start GUI
streamlit run gui/app.py    # Alternative launch

# Ollama (for LLM agents)
ollama serve                # Start service
ollama pull llama3.2        # Download model
ollama list                 # List models

# Development
ls examples/                # List agents
python3 examples/my_agent.py  # Test agent
```

---

## Support

**Quick diagnostics:**
```bash
python3 gui/test_setup.py   # Check installation
python3 gui/check_llm_deps.py  # Check LLM packages (all should be installed)
```

**Documentation:**
- GUI Quick Start: [GUI_QUICK_START.md](../GUI_QUICK_START.md)
- Framework docs: [README.md](../README.md)
- Troubleshooting: [docs/TROUBLESHOOTING.md](../docs/TROUBLESHOOTING.md)

---

## Version

**Version:** 1.0.0  
**Dependencies:** All installed by setup.sh  
**Status:** Production Ready

---

**Educational use only · Not financial advice · MIT License**

See [DISCLAIMER.md](../DISCLAIMER.md) for complete legal terms.
