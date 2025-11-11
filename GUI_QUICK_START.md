# GUI Quick Start

Build AI agents visually with no coding required.

## Setup & Launch

```bash
cd ~/AI-Agent-Builder

# One-time setup
./gui/setup.sh

# Launch GUI
./gui/launch.sh
```

Opens at: `http://localhost:8501`

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

## Test Your Agent

### 1. Navigate
Click "🧪 Test Agent"

### 2. Configure
```
Select Agent: ValueAgent
Ticker: AAPL
Use Mock Data: ✓
PE Ratio: 12
```

### 3. Run
Click "🚀 Run Analysis"

### 4. Result
```
Signal: 🟢 BULLISH
Confidence: 80%
Reasoning: Pe Ratio 12.0 is bullish
```

## Agent Types

### Rule-Based
- Visual rule builder
- No coding needed
- Fast execution

### LLM-Powered
- AI-driven analysis
- Custom personalities
- Detailed reasoning

### Hybrid
- Rules + LLM
- Best of both worlds

## Verify Setup

```bash
# Test everything works
python3 gui/test_setup.py

# Check files
ls examples/

# Test agent
python3 examples/value_agent.py
```

## Troubleshooting

### LLM Dependencies

**Error: "No module named 'ollama'"**

LLM packages are optional. Install them if you want to use LLM-powered or hybrid agents:

```bash
# Install all LLM providers
pip install 'ai-agent-framework[llm]'

# OR install specific provider
pip install ollama      # For Ollama
pip install openai      # For OpenAI
pip install anthropic   # For Anthropic

# Check what's installed
python3 gui/check_llm_deps.py
```

**Rule-based agents don't need LLM packages** - they work on any machine.

### Other Issues

### Files not saving?
```bash
python3 gui/test_setup.py
chmod 755 examples/
```

### GUI won't start?
```bash
pip install --upgrade streamlit
```

### Module errors?
```bash
pip install -e .
```

## Integration with thesis-ai

```python
# In thesis-ai orchestrator
from AI-Agent-Builder.examples.value_agent import ValueAgent

agent = ValueAgent()
signal = agent.analyze('AAPL', data)
```

## Full Documentation

See `gui/README.md` for complete documentation.

---

**Three simple steps:**
1. Setup: `./gui/setup.sh`
2. Launch: `./gui/launch.sh`
3. Create your first agent!
