# Agent Builder GUI

Visual interface for creating and managing AI investment agents without coding.

## Quick Start

```bash
# Setup (one time)
cd ~/AI-Agent-Builder
chmod +x gui/setup.sh gui/launch.sh
./gui/setup.sh

# Launch
./gui/launch.sh
```

Opens at: `http://localhost:8501`

## Features

### 📋 Browse Agents
- View all agents in `examples/` directory
- **Search and filter** agents
- **Statistics dashboard** (total, by type, custom count)
- **Strategy examples** (Buffett, Lynch, Graham)
- Preview source code
- **Duplicate agents** for variations
- **Export agents** to share
- **Delete agents** with safety confirmations
- See agent types and metadata

### ➕ Create Agents

**Four agent types:**

1. **Rule-Based** - Simple if/then logic, no coding required
   - Visual rule builder
   - Fast execution
   - Best for: Clear investment criteria
   - Dependencies: None (core only)
   - **NEW:** Advanced rules with AND/OR logic, score-based strategies

2. **LLM-Powered** - AI-driven analysis
   - OpenAI, Anthropic, or Ollama support
   - Configurable temperature (creativity)
   - Custom system prompts (personality)
   - Best for: Complex, nuanced analysis
   - Dependencies: LLM packages

3. **Hybrid** - Combines rules + LLM
   - Rules trigger deeper analysis
   - LLM provides reasoning
   - Best for: Balanced speed and intelligence
   - Dependencies: LLM packages

4. **RAG-Powered** - Document analysis with retrieval (NEW)
   - Analyzes SEC filings, news, earnings calls
   - Vector-based document search
   - LLM synthesis of retrieved content
   - Best for: Long documents, text analysis
   - Dependencies: LLM + RAG packages

### 🧪 Test Agents
- Mock data testing (no database needed)
- Real data testing (with database)
- Execution timing
- Visual results

## Creating Your First Agent

### Example: Simple Value Agent

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

4. Click "Generate Code" → Preview appears

5. Click "💾 Save Agent" → File saved to `examples/`

6. Verify:
   ```bash
   ls examples/value_agent.py
   python3 examples/value_agent.py
   ```

### Example: AI-Powered Conservative Agent

1. Navigate to "➕ Create Agent"

2. Configure:
   ```
   Agent Name: ConservativeAgent
   Type: LLM-Powered
   Provider: ollama
   Temperature: 0.3 (focused analysis)
   Max Tokens: 1000
   ```

3. System Prompt:
   ```
   You are a conservative value investor.
   Focus on:
   - Low PE ratios (< 15)
   - High dividend yields (> 2%)
   - Strong balance sheets
   Analyze critically and conservatively.
   ```

4. Generate → Save

### Example: RAG Document Analyzer (NEW)

1. Navigate to "➕ Create Agent"

2. Configure:
   ```
   Agent Name: SECAnalystAgent
   Type: RAG-Powered
   Provider: ollama
   Temperature: 0.5
   Max Tokens: 2000
   Chunk Size: 300
   Chunk Overlap: 50
   Top K: 3
   ```

3. System Prompt:
   ```
   You are an SEC filing analyst.
   Extract key insights:
   - Financial performance trends
   - Risk factors
   - Strategic initiatives
   Provide clear, actionable analysis.
   ```

4. Generate → Save

**Note:** RAG agents require both LLM and RAG dependencies:
```bash
pip install 'ai-agent-framework[llm,rag]'
```

## Testing Agents

### With Mock Data

1. Navigate to "🧪 Test Agent"
2. Select: `ValueAgent`
3. Ticker: `AAPL`
4. Enable "Use Mock Data"
5. Set: PE Ratio = 12
6. Click "🚀 Run Analysis"
7. Result: BULLISH (80% confidence)

### With Real Data

1. Ensure database is running: `docker-compose up postgres`
2. Navigate to "🧪 Test Agent"
3. Select agent
4. Ticker: `AAPL`
5. Disable "Use Mock Data"
6. Run Analysis

## Integration with thesis-ai

### Method 1: Direct Import

```python
# In thesis-ai/server/multi_agent_system/advisor/orchestrator.py
from ....AI-Agent-Builder.examples.value_agent import ValueAgent

class Orchestrator:
    def __init__(self):
        self.custom_agent = ValueAgent()
        
    async def analyze(self, ticker, data):
        signal = self.custom_agent.analyze(ticker, data)
        return signal
```

### Method 2: Add to Agent Suite

```python
# In orchestrator.py
self.agents = {
    'fundamental': FundamentalAgent(),
    'technical': TechnicalAgent(),
    'risk': RiskAgent(),
    'macro': MacroAgent(),
    'sentiment': SentimentAgent(),
    'custom_value': ValueAgent()  # Your agent
}
```

## Configuration

### Valid Filenames

✓ Good:
- `value_agent.py`
- `my_agent_v2.py`
- `GrowthAgent.py`

✗ Bad:
- `my agent.py` (space)
- `agent-name.py` (hyphen)
- `1_agent.py` (starts with number)

### LLM Temperature Guide

| Range | Behavior | Use Case |
|-------|----------|----------|
| 0.0-0.3 | Focused, consistent | Value investing |
| 0.4-0.6 | Balanced | General analysis |
| 0.7-1.0 | Creative, diverse | Growth/speculation |

### Agent Types Comparison

| Type | Speed | Complexity | Best For | Dependencies |
|------|-------|------------|----------|-------------|
| Rule-Based | Fast | Low | Clear criteria | None |
| LLM-Powered | Slow | High | Nuanced analysis | LLM |
| Hybrid | Medium | Medium | Balanced approach | LLM |
| RAG-Powered | Slow | High | Document analysis | LLM + RAG |

## File Structure

```
AI-Agent-Builder/
├── gui/
│   ├── app.py              # Main GUI
│   ├── agent_loader.py     # Load/save agents
│   ├── agent_creator.py    # Generate code
│   ├── agent_tester.py     # Test agents
│   ├── test_setup.py       # Diagnostic tool
│   ├── setup.sh            # Setup script
│   └── launch.sh           # Launch script
│
└── examples/               # Agents saved here
    ├── 01_basic.py
    ├── 02_llm_agent.py
    ├── value_agent.py      # Your custom agents
    └── ...
```

## Troubleshooting

### LLM Dependencies (Important!)

**Error: "No module named 'ollama'" or similar**

LLM packages (OpenAI, Anthropic, Ollama) are **optional dependencies**. If you create or use LLM-powered agents, you need to install them.

**Check what's installed:**
```bash
python3 gui/check_llm_deps.py
```

**Install LLM dependencies:**

```bash
# Option 1: Install all LLM providers (recommended)
pip install 'ai-agent-framework[llm]'

# Option 2: Install specific provider
pip install ollama      # For Ollama agents
pip install openai      # For OpenAI agents
pip install anthropic   # For Anthropic agents
```

**Which agents need LLM packages?**
- ❌ Rule-Based agents: No LLM needed (work everywhere)
- ✅ LLM-Powered agents: Need LLM packages
- ✅ Hybrid agents: Need LLM packages
- ✅ RAG-Powered agents: Need LLM + RAG packages

**For RAG agents, also install:**
```bash
pip install sentence-transformers  # For embeddings
```

**For multi-machine setup:**
1. Install dependencies on all machines: `pip install 'ai-agent-framework[llm,rag]'`
2. OR use only Rule-Based agents (no dependencies)

### Files Not Saving

**Test the setup:**
```bash
python3 gui/test_setup.py
```

**Check permissions:**
```bash
ls -ld ~/AI-Agent-Builder/examples/
# Should show: drwxr-xr-x

# Fix if needed:
chmod 755 ~/AI-Agent-Builder/examples/
```

**Verify directory exists:**
```bash
mkdir -p ~/AI-Agent-Builder/examples
```

### GUI Won't Start

```bash
# Install/upgrade Streamlit
pip install --upgrade streamlit

# Verify installation
streamlit --version
```

### Module Not Found

```bash
# Install framework
cd ~/AI-Agent-Builder
pip install -e .

# Verify
python3 -c "import agent_framework; print('OK')"
```

### LLM Agents Fail

**For Ollama:**
```bash
# Check if running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Pull model
ollama pull llama3.2
```

**For OpenAI:**
```bash
# Check API key exists
grep OPENAI_API_KEY ~/AI-Agent-Builder/.env

# Test connection
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Agent Not Loading

**Check file format:**
- Must be in `examples/` directory
- Must have `.py` extension
- Must contain class inheriting from `Agent`

```python
# Minimum valid agent
from agent_framework import Agent, Signal

class MyAgent(Agent):
    def analyze(self, ticker, data):
        return Signal('neutral', 0.5, 'test')
```

## Commands Reference

```bash
# Setup
./gui/setup.sh                    # One-time setup
python3 gui/test_setup.py         # Test setup

# Launch
./gui/launch.sh                   # Start GUI

# Verify
ls examples/                      # List agents
python3 examples/my_agent.py      # Test agent

# Database
docker-compose up postgres        # Start database
docker-compose down               # Stop database

# Framework
pip install -e .                  # Install framework
pytest tests/                     # Run tests
```

## Common Patterns

### Basic Value Agent
```python
class ValueAgent(Agent):
    def analyze(self, ticker, data):
        pe = data.get('pe_ratio', 0)
        if pe < 15:
            return Signal('bullish', 0.8, f'Undervalued at PE={pe}')
        return Signal('neutral', 0.5, 'Fair value')
```

### Growth Agent
```python
class GrowthAgent(Agent):
    def analyze(self, ticker, data):
        growth = data.get('revenue_growth', 0)
        margin = data.get('profit_margin', 0)
        
        if growth > 20 and margin > 15:
            return Signal('bullish', 0.9, 'Strong growth + margins')
        return Signal('neutral', 0.5, 'Moderate growth')
```

### Hybrid Agent
```python
class HybridAgent(Agent):
    def __init__(self):
        config = AgentConfig(
            llm=LLMConfig(provider='ollama', temperature=0.5)
        )
        super().__init__(config)
    
    def analyze(self, ticker, data):
        # Use rules first
        if data.get('revenue_growth', 0) > 30:
            # Then LLM for detailed analysis
            return self._llm_analysis(ticker, data)
        return Signal('neutral', 0.5, 'No triggers')
```

## Requirements

- Python 3.10+
- Streamlit 1.28+
- AI-Agent-Builder framework
- Optional: PostgreSQL (for real data testing)
- Optional: Ollama/OpenAI/Anthropic (for LLM agents)

## Support

**Quick Help:**
1. Run `python3 gui/test_setup.py` to diagnose issues
2. Check sidebar "Save Location" in GUI
3. Review terminal logs when GUI is running
4. Check framework docs: `~/AI-Agent-Builder/README.md`

**Common Issues:**
- Files not saving → Run `python3 gui/test_setup.py`
- GUI won't start → `pip install --upgrade streamlit`
- Import errors → `pip install -e .`
- LLM fails → Check provider is running

## Tips

**Agent Design:**
- Start simple, add complexity gradually
- Test with multiple tickers
- Use clear, descriptive names
- Include error handling

**Rule-Based Agents:**
- Fast execution
- Predictable behavior
- Good for screening

**LLM Agents:**
- More intelligent
- Slower (API latency)
- Good for detailed analysis
- Use low temperature for consistency

**Testing:**
- Use mock data for quick tests
- Test edge cases (extreme values)
- Verify with real data before deployment

## Version

**Version:** 1.0.0  
**Status:** Production Ready  
**Last Updated:** 2025-01-23

---

**Documentation:**
- Framework: `~/AI-Agent-Builder/README.md`
- Examples: `~/AI-Agent-Builder/examples/`
- Quick Start: `~/AI-Agent-Builder/GUI_QUICK_START.md`
