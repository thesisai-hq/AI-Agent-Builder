# Agent Builder GUI - Quick Start

Visual interface for creating AI investment agents.

## Installation

### Option 1: Automated Setup (Recommended)

```bash
# From AI-Agent-Builder directory
chmod +x gui/setup.sh
./gui/setup.sh
```

### Option 2: Manual Setup

```bash
# Install framework
pip install -e .

# Install GUI dependencies
pip install -r gui/requirements.txt
```

## Launch

```bash
# From AI-Agent-Builder directory
chmod +x gui/launch.sh
./gui/launch.sh
```

Or manually:

```bash
streamlit run gui/app.py
```

Opens browser at `http://localhost:8501`

## Usage

### 1. Browse Agents

View all agents in `examples/` directory:
- See agent names and types
- View source code
- Understand patterns

### 2. Create Agent

**Rule-Based Agent:**
1. Enter name: `MyValueAgent`
2. Choose "Rule-Based" template
3. Add rules:
   - Metric: `pe_ratio`
   - Operator: `<`
   - Threshold: `15`
   - Signal: `bullish`
   - Confidence: `0.8`
4. Generate → Save

**LLM-Powered Agent:**
1. Enter name: `MyLLMAgent`
2. Choose "LLM-Powered" template
3. Configure:
   - Provider: `ollama`
   - Temperature: `0.5`
   - Max Tokens: `1000`
   - System Prompt: "You are a growth investor..."
4. Generate → Save

### 3. Test Agent

1. Select your agent
2. Enter ticker: `AAPL`
3. Use mock data or database
4. Run analysis
5. View results

## Example Workflow

```bash
# 1. Setup
./gui/setup.sh

# 2. Launch
./gui/launch.sh

# 3. Create agent via GUI
#    - Name: ValueAgent
#    - Type: Rule-Based
#    - Rule: PE < 15 → Bullish

# 4. Test in GUI
#    - Agent: ValueAgent
#    - Ticker: AAPL
#    - Mock Data: PE=12
#    - Result: Bullish signal

# 5. Use in thesis-ai
# Import: from AI-Agent-Builder.examples.value_agent import ValueAgent
```

## Directory Structure

```
AI-Agent-Builder/
├── gui/
│   ├── app.py           # Main GUI application
│   ├── agent_loader.py  # Load/save agents
│   ├── agent_creator.py # Generate code
│   ├── agent_tester.py  # Test agents
│   ├── setup.sh         # Setup script
│   ├── launch.sh        # Launch script
│   └── README.md        # Full documentation
│
└── examples/            # Agents saved here
    ├── 01_basic.py      # Framework examples
    ├── 02_llm_agent.py
    ├── my_agent.py      # Your agents
    └── ...
```

## Requirements

- Python 3.10+
- Streamlit 1.28+
- AI-Agent-Builder framework

## Features

✅ Visual agent builder  
✅ Rule-based agents  
✅ LLM-powered agents  
✅ Hybrid agents  
✅ Mock data testing  
✅ Code generation  
✅ File-based storage  
✅ Compatible with thesis-ai

## Documentation

- **Full Guide**: `gui/README.md`
- **Framework**: `README.md`
- **Examples**: `examples/`

## Troubleshooting

**GUI won't start:**
```bash
pip install --upgrade streamlit
```

**Module not found:**
```bash
pip install -e .
```

**Permission denied:**
```bash
chmod +x gui/*.sh
```

## Next Steps

1. ✅ Create your first agent
2. ✅ Test with mock data
3. ✅ Deploy to thesis-ai
4. ✅ Monitor performance

---

Full documentation: `gui/README.md`
