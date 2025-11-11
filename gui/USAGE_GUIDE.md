# Agent Builder GUI - Complete Usage Guide

## Table of Contents

1. [Getting Started](#getting-started)
2. [Creating Your First Agent](#creating-your-first-agent)
3. [Advanced Agent Patterns](#advanced-agent-patterns)
4. [Testing and Validation](#testing-and-validation)
5. [Integration with thesis-ai](#integration-with-thesis-ai)
6. [Tips and Best Practices](#tips-and-best-practices)
7. [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites

- Python 3.10+
- AI-Agent-Builder framework installed
- Optional: PostgreSQL database for real data testing

### Installation

```bash
# Navigate to AI-Agent-Builder
cd ~/AI-Agent-Builder

# Run setup script (recommended)
chmod +x gui/setup.sh gui/launch.sh
./gui/setup.sh
```

### Launch

```bash
./gui/launch.sh
```

Opens at: `http://localhost:8501`

## Creating Your First Agent

### Example 1: Simple Value Agent

**Goal**: Buy stocks with PE ratio < 15

**Steps**:

1. **Navigate to Create Agent**
   - Click "➕ Create Agent" in sidebar

2. **Basic Information**
   ```
   Agent Class Name: SimpleValueAgent
   Description: Buys undervalued stocks based on PE ratio
   Filename: simple_value_agent.py
   ```

3. **Select Template**
   ```
   Template: Rule-Based
   ```

4. **Add Rule**
   ```
   Rule 1:
   - Metric: pe_ratio
   - Operator: <
   - Threshold: 15
   - Signal: bullish
   - Confidence: 0.8
   ```

5. **Generate and Save**
   - Click "Generate Code"
   - Review generated code
   - Click "💾 Save Agent"

**Generated Code**:
```python
class SimpleValueAgent(Agent):
    """Buys undervalued stocks based on PE ratio"""
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        pe_ratio = data.get('pe_ratio', 0)
        
        if data.get('pe_ratio', 0) < 15:
            return Signal(
                direction='bullish',
                confidence=0.8,
                reasoning=f"Pe Ratio {pe_ratio:.1f} is bullish"
            )
        
        return Signal(
            direction='neutral',
            confidence=0.5,
            reasoning='No rules matched'
        )
```

### Example 2: Growth Investor Agent

**Goal**: Find high-growth companies with healthy margins

**Steps**:

1. **Basic Information**
   ```
   Agent Class Name: GrowthInvestorAgent
   Description: Seeks high-growth companies with strong margins
   Filename: growth_investor_agent.py
   Template: Rule-Based
   ```

2. **Add Rules**
   ```
   Rule 1:
   - Metric: revenue_growth
   - Operator: >
   - Threshold: 20
   - Signal: bullish
   - Confidence: 0.75
   
   Rule 2:
   - Metric: profit_margin
   - Operator: >
   - Threshold: 15
   - Signal: bullish
   - Confidence: 0.7
   ```

3. **Generate and Save**

**Result**: Agent that signals bullish when either condition is met

### Example 3: AI-Powered Conservative Agent

**Goal**: Conservative investor with risk-averse analysis

**Steps**:

1. **Basic Information**
   ```
   Agent Class Name: ConservativeAIAgent
   Description: AI-powered conservative investment analysis
   Filename: conservative_ai_agent.py
   Template: LLM-Powered
   ```

2. **LLM Configuration**
   ```
   Provider: ollama
   Temperature: 0.3  (low = focused)
   Max Tokens: 1000
   System Prompt:
   "You are a conservative value investor with 30 years of experience.
   
   Your philosophy:
   - Safety of principal is paramount
   - Focus on low PE ratios (< 15)
   - Prefer high dividend yields (> 2%)
   - Avoid high-debt companies
   - Be skeptical of high-growth narratives
   
   Analyze critically and conservatively."
   ```

3. **Generate and Save**

**Result**: LLM agent with conservative personality

## Advanced Agent Patterns

### Pattern 1: Momentum + Fundamentals (Hybrid)

**Concept**: Use rules to identify momentum, LLM for fundamental analysis

```python
# In GUI:
Template: Hybrid
Rules:
- revenue_growth > 30
LLM: Detailed fundamental analysis
```

**Use Case**: Filter for high-growth, then deep dive

### Pattern 2: Multi-Criteria Screening

**Concept**: Multiple rules for comprehensive screening

```python
# In GUI:
Rule 1: pe_ratio < 20
Rule 2: revenue_growth > 15
Rule 3: profit_margin > 10
Rule 4: debt_to_equity < 1.0
Rule 5: roe > 12
```

**Use Case**: Quality stock screening

### Pattern 3: Sector-Specific Analysis

**Concept**: Different rules for different sectors

```python
# Create separate agents:
- tech_growth_agent.py    (high growth, low margin OK)
- value_dividend_agent.py (low PE, high dividend)
- bank_quality_agent.py   (ROE, capital ratios)
```

**Use Case**: Specialized sector analysis

### Pattern 4: Risk-Adjusted Agent

**Concept**: Consider volatility in signals

```python
# In GUI:
Rules include:
- Low beta (< 1.2)
- High sharpe ratio
- Stable earnings
```

**Use Case**: Conservative portfolio management

## Testing and Validation

### Testing with Mock Data

**Purpose**: Quick validation without database

**Steps**:

1. **Navigate to Test Agent**
   - Click "🧪 Test Agent"

2. **Configure Test**
   ```
   Select Agent: SimpleValueAgent
   Ticker: AAPL
   Use Mock Data: ✓ Enabled
   ```

3. **Set Mock Data**
   ```
   PE Ratio: 12.0
   Revenue Growth: 15.0
   Profit Margin: 25.0
   ROE: 28.0
   Debt/Equity: 0.5
   Dividend Yield: 0.5
   ```

4. **Run Analysis**
   - Click "🚀 Run Analysis"
   - Review results

**Expected Output**:
```
Signal: 🟢 BULLISH
Confidence: 80%
Reasoning: Pe Ratio 12.0 is bullish
Runtime: 0.01s
```

### Testing Edge Cases

**Test 1: Extreme Values**
```
PE Ratio: 100
Expected: Bearish or Neutral
```

**Test 2: Missing Data**
```
PE Ratio: 0 (missing)
Expected: Handle gracefully
```

**Test 3: Boundary Values**
```
PE Ratio: 15 (exactly at threshold)
Expected: Clear behavior
```

### Testing with Real Data

**Prerequisite**: Database connection configured

**Steps**:

1. **Disable Mock Data**
   ```
   Use Mock Data: ✗ Disabled
   ```

2. **Enter Real Ticker**
   ```
   Ticker: AAPL
   ```

3. **Run Analysis**
   - Uses actual database data
   - Tests real-world integration

## Integration with thesis-ai

### Option 1: Direct Import

```python
# In thesis-ai/server/multi_agent_system/advisor/orchestrator.py

# Add custom agent
from ....AI-Agent-Builder.examples.simple_value_agent import SimpleValueAgent

class Orchestrator:
    def __init__(self):
        self.agents = {
            'fundamental': FundamentalAgent(),
            'technical': TechnicalAgent(),
            'risk': RiskAgent(),
            'macro': MacroAgent(),
            'sentiment': SentimentAgent(),
            'custom_value': SimpleValueAgent()  # Your custom agent
        }
```

### Option 2: Dynamic Loading

```python
# Load agents dynamically
import importlib
import sys
from pathlib import Path

# Add AI-Agent-Builder to path
agent_builder_path = Path.home() / "AI-Agent-Builder"
sys.path.insert(0, str(agent_builder_path))

# Load agent
module = importlib.import_module('examples.simple_value_agent')
CustomAgent = getattr(module, 'SimpleValueAgent')

# Use agent
agent = CustomAgent()
signal = agent.analyze('AAPL', data)
```

### Option 3: Standalone Service

```python
# Create separate endpoint for custom agents
@app.post("/api/v1/custom-analyze")
async def custom_analyze(ticker: str, agent_name: str):
    # Load agent from examples/
    agent = load_custom_agent(agent_name)
    
    # Run analysis
    data = await db.get_fundamentals(ticker)
    signal = agent.analyze(ticker, data)
    
    return signal
```

## Tips and Best Practices

### Agent Design

**DO**:
- ✅ Start simple, add complexity gradually
- ✅ Use clear, descriptive names
- ✅ Test with multiple tickers
- ✅ Include error handling
- ✅ Document your reasoning

**DON'T**:
- ❌ Overfit to specific stocks
- ❌ Use too many rules
- ❌ Ignore edge cases
- ❌ Skip testing
- ❌ Make overly complex logic

### Rule-Based Agents

**Best Practices**:
```python
# Good: Clear threshold
if pe_ratio < 15:
    return Signal('bullish', 0.8, 'Undervalued')

# Better: Include context
if pe_ratio < 15 and profit_margin > 10:
    return Signal('bullish', 0.85, 'Undervalued with healthy margins')
```

### LLM Agents

**Temperature Guide**:
- `0.0-0.3`: Conservative, focused (value investing)
- `0.4-0.6`: Balanced (general analysis)
- `0.7-1.0`: Creative, diverse (growth/speculation)

**System Prompt Tips**:
```python
# Good system prompt
"""You are a value investor focusing on:
1. Low PE ratios (< 15)
2. High margins (> 15%)
3. Strong ROE (> 15%)

Analyze conservatively."""

# Bad system prompt
"""Analyze stocks."""  # Too vague
```

### Testing Strategy

**Progressive Testing**:
1. Mock data (quick validation)
2. Historical data (backtesting)
3. Recent data (current relevance)
4. Live data (production readiness)

**Test Matrix**:
```
Ticker | Expected | Actual | Pass/Fail
-------|----------|--------|----------
AAPL   | Bullish  | Bullish| ✓
TSLA   | Neutral  | Neutral| ✓
JPM    | Bearish  | Bearish| ✓
```

### Code Quality

**Naming Conventions**:
```python
# Good
class ValueInvestorAgent(Agent)      # Clear purpose
class MomentumScreenerAgent(Agent)    # Describes strategy

# Bad
class Agent1(Agent)                   # Generic
class MyAgent(Agent)                  # Vague
```

**Documentation**:
```python
class ValueInvestorAgent(Agent):
    """Value investing agent using PE ratio screening.
    
    Strategy:
    - Bullish when PE < 15 (undervalued)
    - Bearish when PE > 30 (overvalued)
    - Considers profit margins for confidence
    
    Use Case: Conservative portfolio building
    """
```

## Troubleshooting

### Common Issues

#### Issue 1: GUI Won't Start

**Symptoms**:
```bash
$ streamlit run gui/app.py
Command not found: streamlit
```

**Solution**:
```bash
pip install --upgrade streamlit
```

#### Issue 2: Agent Won't Load

**Symptoms**: Agent not showing in browse list

**Solutions**:
1. Check filename ends with `.py`
2. Verify class inherits from `Agent`
3. Ensure file in `examples/` directory
4. Check for syntax errors

#### Issue 3: LLM Agent Fails

**Symptoms**:
```
⚠️ LLM error: Connection refused
```

**Solutions**:

For Ollama:
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Pull model if needed
ollama pull llama3.2
```

For OpenAI/Anthropic:
```bash
# Check API key in .env
grep API_KEY .env

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

#### Issue 4: Can't Save Agent

**Symptoms**: "File already exists" error

**Solutions**:
1. Choose different filename
2. Delete/rename existing file
3. Add version suffix: `agent_v2.py`

#### Issue 5: Generated Code Has Errors

**Symptoms**: Agent fails to execute

**Solutions**:
1. Check for syntax errors in generated code
2. Verify all imports are available
3. Test manually before saving
4. Report bug if template issue

### Getting Help

**Self-Help Resources**:
1. Check `gui/README.md` for detailed docs
2. Review examples in `examples/` directory
3. Read framework docs in `docs/`
4. Check error messages carefully

**Community Support**:
1. GitHub Issues
2. Framework documentation
3. Code examples
4. Team Slack/Discord

## Advanced Workflows

### Workflow 1: Agent Portfolio

**Goal**: Create suite of specialized agents

```bash
# Create agents for different strategies
1. value_agent.py       (PE-based)
2. growth_agent.py      (Growth-based)
3. momentum_agent.py    (Technical)
4. dividend_agent.py    (Income)
5. quality_agent.py     (Quality metrics)
```

**Usage**: Run all, aggregate signals

### Workflow 2: Strategy Comparison

**Goal**: Compare different approaches

```bash
# Same strategy, different parameters
1. conservative_value_agent.py  (PE < 12)
2. moderate_value_agent.py      (PE < 18)
3. aggressive_value_agent.py    (PE < 25)
```

**Analysis**: Backtest to find optimal threshold

### Workflow 3: Sector Rotation

**Goal**: Different agents per sector

```bash
1. tech_agent.py        (Growth focus)
2. financial_agent.py   (Value focus)
3. utility_agent.py     (Dividend focus)
4. healthcare_agent.py  (Quality focus)
```

**Usage**: Select agent based on sector

### Workflow 4: Multi-Timeframe

**Goal**: Different horizons

```bash
1. day_trading_agent.py    (Technical)
2. swing_trading_agent.py  (Momentum)
3. long_term_agent.py      (Fundamental)
```

**Usage**: Match agent to investment horizon

## Appendix

### Keyboard Shortcuts

Streamlit shortcuts:
- `R`: Rerun app
- `C`: Clear cache
- `Ctrl+C`: Stop app

### Configuration Files

**Location**: `AI-Agent-Builder/.env`

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/db

# LLM Providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Ollama (if not default)
OLLAMA_URL=http://localhost:11434
```

### File Permissions

Make scripts executable:
```bash
chmod +x gui/setup.sh
chmod +x gui/launch.sh
```

### Version Information

Check versions:
```bash
# Streamlit
streamlit version

# Python
python --version

# Framework
pip show agent-framework
```

---

**Version**: 1.0.0  
**Last Updated**: 2025-01-23  
**For Support**: See gui/README.md
