# Agent File Organization - Best Practice

## ✅ **Required: One Agent Per File**

This framework enforces a simple, clear principle:

**ONE Agent Class = ONE Python File**

---

## 🎯 Why This Rule?

### 1. **Clarity**
```python
# CLEAR ✅
value_agent.py        → class ValueAgent
growth_agent.py       → class GrowthAgent  
dividend_agent.py     → class DividendAgent

# CONFUSING ❌
strategies.py → ValueAgent, GrowthAgent, DividendAgent
# Which one am I testing? Which one am I looking at?
```

### 2. **No Ambiguity**
```
File name = Agent name = Strategy
No guessing, no confusion
```

### 3. **Easy Testing**
```
Select "ValueAgent" → Loads value_agent.py → Runs ValueAgent
Simple, predictable, works every time
```

### 4. **Better Organization**
```bash
ls examples/
  buffett_quality.py
  graham_value.py
  lynch_garp.py
  
# Easy to find what you need!
```

### 5. **Version Control**
```bash
git commit -m "Improved value_agent PE threshold"
# Clear what changed

vs

git commit -m "Updated strategies.py"
# Which strategy? Unclear!
```

### 6. **Sharing & Collaboration**
```
# Send one file to a friend
scp value_agent.py friend@server:

# They know exactly what they're getting!
```

---

## 📝 Naming Convention

### Pattern:
```
Filename: snake_case.py
Class: PascalCase

Examples:
value_agent.py           → class ValueAgent
growth_strategy.py       → class GrowthStrategy
buffett_quality.py       → class BuffettQualityAgent
my_custom_approach.py    → class MyCustomApproach
```

### File Structure:
```python
"""My Value Investment Strategy

Buys undervalued stocks with strong dividends.

Strategy:
- PE Ratio < 15
- Dividend Yield > 2%
- Debt-to-Equity < 0.5

⚠️ DISCLAIMER: Educational use only. Not financial advice.
"""

from agent_framework import Agent, Signal

class MyValueStrategy(Agent):
    """One agent, one file, one clear purpose."""
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        # Your strategy here
        ...

# ONE agent per file!
```

---

## ⚠️ What If I Have Multiple Agents in One File?

### Current Behavior:
- **GUI shows:** First agent only with warning "⚠️ (+2 more in file)"
- **GUI loads:** First agent class found
- **Recommendation:** Split into separate files

### How to Split:

**Before (Don't Do This):**
```python
# strategies.py
class ValueAgent(Agent): ...
class GrowthAgent(Agent): ...
class DividendAgent(Agent): ...
```

**After (Do This):**
```python
# value_agent.py
class ValueAgent(Agent): ...

# growth_agent.py  
class GrowthAgent(Agent): ...

# dividend_agent.py
class DividendAgent(Agent): ...
```

### Using the GUI to Split:
```
1. Browse Agents
2. Click "📋 Copy" on the multi-agent file
3. Duplicate 3 times with different names:
   - value_agent.py
   - growth_agent.py
   - dividend_agent.py
4. Edit each file to remove the other agents
5. Keep only ONE agent per file
```

---

## 📚 For Framework Examples

### Recommendation: Same Rule!

Even framework examples should follow one-agent-per-file:

**Recommended:**
```
examples/
├── 01_value_basic.py              # ValueAgent
├── 02_growth_basic.py             # GrowthAgent
├── 03_conservative_llm.py         # ConservativeAgent
├── 04_aggressive_llm.py           # AggressiveAgent
├── 05_buffett_quality.py          # BuffettQualityAgent
├── 06_lynch_garp.py               # LynchGARPAgent
└── 07_graham_value.py             # GrahamValueAgent
```

**Why:**
- Students learn by example
- If examples have multiple agents, students will too
- Consistency between framework and GUI
- Simpler to understand and explain

---

## 🔧 Best Practices

### DO ✅

```python
# ONE clear strategy per file
# value_agent.py

"""Value Investment Strategy

Warren Buffett-inspired approach focusing on undervalued stocks.
"""

from agent_framework import Agent, Signal

class ValueAgent(Agent):
    """Seeks undervalued stocks with PE < 15"""
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        pe = data.get('pe_ratio', 0)
        
        if pe < 15:
            return Signal('bullish', 0.8, f'Undervalued at PE={pe}')
        ...
```

### DON'T ❌

```python
# MULTIPLE unrelated strategies in one file
# strategies.py

from agent_framework import Agent, Signal

class ValueAgent(Agent): ...
class GrowthAgent(Agent): ...
class MomentumAgent(Agent): ...
class DividendAgent(Agent): ...

# Confusing! Which one do I want? Which one runs?
```

---

## 🎓 Educational Benefits

Students who follow this pattern learn:

1. **Clear Code Organization**
   - One responsibility per file
   - Easy to navigate
   - Professional practice

2. **Modular Design**
   - Each strategy is self-contained
   - Easy to reuse and share
   - Clear dependencies

3. **Version Control Skills**
   - Meaningful commit messages
   - Clear change history
   - Easy code reviews

4. **Professional Habits**
   - Industry-standard practices
   - Clean project structure
   - Maintainable codebases

---

## 🚀 For Multi-Agent Systems

### Same Recommendation:

```python
# Multi-agent system structure:
# server/multi_agent_system/agents/
├── value_agent.py          # One agent
├── growth_agent.py         # One agent
├── sentiment_agent.py      # One agent
└── risk_agent.py           # One agent

# Clear, organized, professional
```

### Import Pattern:
```python
from agents.value_agent import ValueAgent
from agents.growth_agent import GrowthAgent

# Explicit, clear, maintainable
```

---

## ❓ FAQ

### Q: But what about comparing similar strategies?

**A:** Use descriptive filenames:
```
value_conservative.py    # Strict value rules
value_moderate.py        # Relaxed value rules
value_dividend.py        # Value + dividends
```

### Q: Can I still have multiple agents if I want?

**A:** Technically yes, but:
- GUI will only show/load the first one
- You'll see a warning "⚠️ (+X more in file)"
- Strongly not recommended
- Better to split into separate files

### Q: What about helper classes?

**A:** Helper classes are fine:
```python
# value_agent.py

class ValueCalculator:  # Helper class (not an Agent)
    def calculate_score(self, data): ...

class ValueAgent(Agent):  # The ONE agent
    def analyze(self, ticker, data): ...
```

---

## ✅ Summary

**Rule:** One Agent class per Python file

**Benefits:**
- Clear identity (filename = agent = strategy)
- Easy to find, test, manage, share
- Professional code organization
- Best practice for beginners and experts

**Enforcement:**
- GUI creates one-per-file automatically
- GUI shows warning if multiple detected
- GUI loads first agent only from multi-agent files

**Recommendation:**
Follow this rule everywhere for maximum clarity and best educational experience.

---

**See Also:**
- [Data Flow](DATA_FLOW.md) - Understand agent data processing ⭐
- [Multi-Agent Systems](MULTI_AGENT_SYSTEMS.md) - Organize multiple agents ⭐
- [Project Structure](PROJECT_STRUCTURE.md)
- [Getting Started](GETTING_STARTED.md)
- [Contributing Guidelines](../CONTRIBUTING.md)
