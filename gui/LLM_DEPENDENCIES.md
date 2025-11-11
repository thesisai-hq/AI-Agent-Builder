# LLM Dependencies Guide

## The Issue

When using LLM-powered agents on different machines, you may see:

```
ERROR: Failed to initialize ollama client: No module named 'ollama'
```

This happens because LLM packages are **optional dependencies** and may not be installed on all machines.

## Understanding Dependencies

The AI-Agent-Builder has three levels of dependencies:

### 1. Core (Always Installed)
```bash
pip install -e .
```

Includes:
- FastAPI
- Pydantic
- AsyncPG
- Basic framework

**Can use:**
- ✅ Rule-based agents
- ✅ Database connections
- ✅ Agent framework

**Cannot use:**
- ❌ LLM-powered agents
- ❌ Hybrid agents

### 2. LLM (Optional)
```bash
pip install 'ai-agent-framework[llm]'
```

Includes:
- OpenAI
- Anthropic
- Ollama

**Can use:**
- ✅ Everything from Core
- ✅ LLM-powered agents
- ✅ Hybrid agents
- ✅ All three LLM providers

### 3. Individual Providers
```bash
pip install ollama      # Just Ollama
pip install openai      # Just OpenAI
pip install anthropic   # Just Anthropic
```

## Solutions

### For Development Machine

Install all LLM providers:
```bash
cd ~/AI-Agent-Builder
pip install -e '.[llm]'
```

### For Production Machine

**Option 1: Install only what you need**
```bash
# If you use Ollama agents
pip install ollama

# If you use OpenAI agents
pip install openai

# If you use Anthropic agents
pip install anthropic
```

**Option 2: Use rule-based agents**
```bash
# Only install core framework
pip install -e .
```

Rule-based agents work without any LLM packages.

### For Shared Codebase

If agents are synced between machines:

1. **Check which providers are available:**
   ```bash
   python3 gui/check_llm_deps.py
   ```

2. **Install missing providers:**
   ```bash
   # See output from check command
   pip install <missing-provider>
   ```

3. **Or create separate agents:**
   - Machine A with Ollama → Create Ollama agents
   - Machine B without Ollama → Create rule-based agents

## Checking Your Setup

### Quick Check

```bash
python3 gui/check_llm_deps.py
```

Output shows:
```
✓ OpenAI      - Available
✓ Anthropic   - Available
✗ Ollama      - Not installed
  Install: pip install ollama
```

### Manual Check

```python
# Test OpenAI
try:
    import openai
    print("OpenAI available")
except ImportError:
    print("OpenAI not installed")

# Test Anthropic
try:
    import anthropic
    print("Anthropic available")
except ImportError:
    print("Anthropic not installed")

# Test Ollama
try:
    import ollama
    print("Ollama available")
except ImportError:
    print("Ollama not installed")
```

## Agent Type Guide

### Rule-Based Agents
```python
class MyAgent(Agent):
    def analyze(self, ticker, data):
        if data['pe_ratio'] < 15:
            return Signal('bullish', 0.8, 'Undervalued')
        return Signal('neutral', 0.5, 'Fair value')
```

**Dependencies:** None (core only)  
**Works on:** Any machine with core framework  
**Speed:** Very fast  
**Best for:** Clear criteria, production systems

### LLM-Powered Agents
```python
class MyLLMAgent(Agent):
    def __init__(self):
        config = AgentConfig(
            llm=LLMConfig(provider='ollama')
        )
        super().__init__(config)
```

**Dependencies:** Requires `ollama` package  
**Works on:** Machines with LLM packages installed  
**Speed:** Slower (API calls)  
**Best for:** Complex analysis, nuanced decisions

### Hybrid Agents
```python
class MyHybridAgent(Agent):
    def analyze(self, ticker, data):
        if data['pe_ratio'] < 10:  # Rule
            return self._llm_analysis(ticker, data)  # Then LLM
        return Signal('neutral', 0.5, 'No trigger')
```

**Dependencies:** Requires LLM packages  
**Works on:** Machines with LLM packages installed  
**Speed:** Medium  
**Best for:** Balanced approach

## Best Practices

### For Multi-Machine Setups

1. **Document your dependencies** in README:
   ```markdown
   ## Setup
   
   For rule-based agents only:
   pip install -e .
   
   For LLM agents:
   pip install -e '.[llm]'
   ```

2. **Create `.python-version` file:**
   ```
   3.10
   ```

3. **Create `requirements-llm.txt`:**
   ```
   openai>=1.3.0
   anthropic>=0.7.0
   ollama>=0.1.0
   ```

4. **Use environment checks** in code:
   ```python
   try:
       from .llm import LLMClient
       HAS_LLM = True
   except ImportError:
       HAS_LLM = False
   
   if HAS_LLM:
       # Use LLM agent
   else:
       # Fall back to rule-based
   ```

### For Agent Creation

1. **Choose appropriate type:**
   - Need it to work everywhere? → Rule-Based
   - Have LLM setup? → LLM-Powered
   - Complex logic? → Hybrid

2. **Add dependency notes in code:**
   ```python
   """
   DEPENDENCIES:
   - Requires: pip install ollama
   - Check: python3 gui/check_llm_deps.py
   """
   ```

3. **Test on target machine:**
   ```bash
   # On production machine
   python3 examples/my_agent.py
   ```

### For CI/CD

```yaml
# .github/workflows/test.yml
- name: Install core
  run: pip install -e .

- name: Test rule-based agents
  run: pytest tests/test_rule_based.py

- name: Install LLM
  run: pip install -e '.[llm]'

- name: Test LLM agents
  run: pytest tests/test_llm.py
```

## Troubleshooting

### Error: Module not found

```bash
# Check what's installed
pip list | grep -E "openai|anthropic|ollama"

# Install missing package
pip install ollama
```

### Error: Agent fails on other machine

```bash
# On the other machine
cd ~/AI-Agent-Builder
python3 gui/check_llm_deps.py

# Install missing providers
pip install <missing-provider>
```

### Error: Import error in agent

Check the agent file for:
```python
from agent_framework import LLMConfig
```

Make sure LLM dependencies are installed.

## Summary

| Scenario | Solution |
|----------|----------|
| Development machine | `pip install -e '.[llm]'` |
| Production (all agents) | `pip install -e '.[llm]'` |
| Production (rule-based only) | `pip install -e .` |
| Check availability | `python3 gui/check_llm_deps.py` |
| Fix missing Ollama | `pip install ollama` |
| Fix missing OpenAI | `pip install openai` |
| Fix missing Anthropic | `pip install anthropic` |

---

**Key Takeaway:** LLM packages are optional. Install only what you need for your agents.
