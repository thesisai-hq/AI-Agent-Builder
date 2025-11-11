# Agent Builder GUI

Visual interface for creating and managing AI investment agents.

## Features

- 📋 **Browse Agents** - View all agents in `examples/` directory
- ➕ **Create Agents** - Build agents with visual interface
- 🧪 **Test Agents** - Test agents with mock or real data
- 💾 **Save Agents** - Save generated agents to `examples/`

## Quick Start

### 1. Install Dependencies

```bash
# From AI-Agent-Builder root directory
cd gui
pip install -r requirements.txt
```

### 2. Launch GUI

```bash
# From AI-Agent-Builder root directory
streamlit run gui/app.py
```

The GUI will open in your browser at `http://localhost:8501`

### 3. Create Your First Agent

1. Click "➕ Create Agent"
2. Enter agent name and description
3. Choose agent type:
   - **Rule-Based**: Simple if/then logic
   - **LLM-Powered**: AI-driven analysis
   - **Hybrid**: Combines rules + LLM
4. Configure parameters
5. Click "Generate Code" to preview
6. Click "💾 Save Agent" to save to `examples/`

### 4. Test Your Agent

1. Click "🧪 Test Agent"
2. Select your agent
3. Enter ticker symbol
4. Use mock data or connect to database
5. Click "🚀 Run Analysis"

## Architecture

```
gui/
├── app.py              # Main Streamlit application
├── agent_loader.py     # Load/save agents from examples/
├── agent_creator.py    # Generate agent code from templates
├── agent_tester.py     # Test agents with mock/real data
└── requirements.txt    # GUI dependencies
```

### Design Principles

**Simplicity**: Minimal code, clear structure
**Maintainability**: Each module has single responsibility
**Compatibility**: Works seamlessly with AI-Agent-Builder framework
**File-based**: Agents saved as .py files for version control

## Agent Types

### Rule-Based Agents

Simple if/then logic based on financial metrics.

**Example:**
```python
if pe_ratio < 15:
    return Signal('bullish', 0.8, 'Undervalued')
```

**When to use:**
- Clear investment criteria
- No need for complex reasoning
- Fast execution required

### LLM-Powered Agents

AI-driven analysis using OpenAI, Anthropic, or Ollama.

**Example:**
```python
# Agent uses natural language reasoning
system_prompt = "You are a conservative value investor..."
```

**When to use:**
- Need nuanced analysis
- Complex decision factors
- Natural language reasoning

### Hybrid Agents

Combines rule-based triggers with LLM analysis.

**Example:**
```python
if revenue_growth > 20:
    # Use LLM for detailed analysis
    return self._llm_analysis(ticker, data)
```

**When to use:**
- Rules identify opportunities
- LLM provides detailed reasoning
- Balance speed and depth

## Usage Guide

### Creating Rule-Based Agents

1. Select "Rule-Based" template
2. Add rules:
   - Choose metric (PE ratio, growth, etc.)
   - Set operator (<, >, ==)
   - Define threshold
   - Set signal (bullish/bearish/neutral)
   - Set confidence level
3. Generate and save

**Generated Code Pattern:**
```python
class MyAgent(Agent):
    def analyze(self, ticker: str, data: dict) -> Signal:
        if data.get('pe_ratio', 0) < 15:
            return Signal('bullish', 0.8, 'Undervalued')
        return Signal('neutral', 0.5, 'Fair value')
```

### Creating LLM-Powered Agents

1. Select "LLM-Powered" template
2. Choose provider (OpenAI, Anthropic, Ollama)
3. Set temperature (0.0-1.0):
   - Low (0.3): Focused, consistent
   - Medium (0.5): Balanced
   - High (0.9): Creative, diverse
4. Set max_tokens (100-4000)
5. Write system prompt (agent personality)
6. Generate and save

**Generated Code Pattern:**
```python
class MyAgent(Agent):
    def __init__(self):
        config = AgentConfig(
            name="MyAgent",
            llm=LLMConfig(
                provider='ollama',
                temperature=0.5,
                max_tokens=1000,
                system_prompt="You are a growth investor..."
            )
        )
        super().__init__(config)
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        response = self.llm.chat(prompt)
        return parse_llm_signal(response)
```

### Testing Agents

#### With Mock Data

1. Select agent
2. Enable "Use Mock Data"
3. Adjust financial metrics
4. Run analysis

**Best for:**
- Quick testing
- Edge case validation
- No database required

#### With Real Data

1. Select agent
2. Disable "Use Mock Data"
3. Enter ticker symbol
4. Run analysis (requires database)

**Best for:**
- Production validation
- Real-world scenarios
- Integration testing

## File Organization

### Agent Files

All agents saved to `examples/` directory:

```
examples/
├── 01_basic.py              # Framework examples
├── 02_llm_agent.py
├── 03_rag_agent.py
├── 04_custom_llm_config.py
├── my_value_agent.py        # Your custom agents
├── my_growth_agent.py
└── my_hybrid_agent.py
```

### Naming Conventions

**Class Names**: PascalCase
- `ValueAgent`, `GrowthAgent`, `MomentumAgent`

**File Names**: snake_case
- `value_agent.py`, `growth_agent.py`, `momentum_agent.py`

## Integration with thesis-ai

Agents created in GUI can be imported directly in thesis-ai:

```python
# In thesis-ai/server/multi_agent_system/advisor/agents/
from AI-Agent-Builder.examples.my_agent import MyAgent

# Use in orchestrator
agent = MyAgent()
signal = agent.analyze('AAPL', data)
```

## Common Patterns

### Basic Value Agent

```python
class ValueAgent(Agent):
    def analyze(self, ticker: str, data: dict) -> Signal:
        pe = data.get('pe_ratio', 0)
        
        if pe < 15:
            return Signal('bullish', 0.8, f'Undervalued at PE={pe:.1f}')
        elif pe > 30:
            return Signal('bearish', 0.7, f'Overvalued at PE={pe:.1f}')
        else:
            return Signal('neutral', 0.6, 'Fair value')
```

### LLM Agent with Persona

```python
class ConservativeAgent(Agent):
    def __init__(self):
        config = AgentConfig(
            name="Conservative Investor",
            llm=LLMConfig(
                provider='ollama',
                temperature=0.3,  # Focused analysis
                system_prompt="You are a risk-averse value investor..."
            )
        )
        super().__init__(config)
```

### Hybrid Agent

```python
class HybridAgent(Agent):
    def analyze(self, ticker: str, data: dict) -> Signal:
        # Rule-based trigger
        if data.get('revenue_growth', 0) > 30:
            # Detailed LLM analysis
            return self._llm_analysis(ticker, data)
        
        # Default neutral
        return Signal('neutral', 0.5, 'No strong signals')
```

## Troubleshooting

### GUI Won't Start

```bash
# Check Streamlit installation
pip list | grep streamlit

# Reinstall if needed
pip install --upgrade streamlit
```

### Agent Won't Load

- Ensure file ends with `.py`
- Check file contains `class XAgent(Agent):`
- Verify file in `examples/` directory

### LLM Agent Fails

- Check LLM provider is running (Ollama)
- Verify API keys in `.env` (OpenAI, Anthropic)
- Test with rule-based fallback

### Can't Save Agent

- Check filename is valid (letters, numbers, underscores)
- Ensure filename doesn't already exist
- Verify write permissions on `examples/` directory

## Advanced Usage

### Custom Templates

Add your own templates in `agent_creator.py`:

```python
def _generate_custom_agent(self, ...):
    return '''
    # Your custom template
    '''
```

### Database Connection

Agents automatically connect to database from `.env`:

```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/db
```

### Multiple Providers

Test same agent with different LLM providers:

1. Create agent with OpenAI
2. Save as `agent_openai.py`
3. Create same agent with Ollama
4. Save as `agent_ollama.py`
5. Compare results

## Best Practices

### Agent Design

- **Single Responsibility**: One agent, one strategy
- **Clear Naming**: Describe what agent does
- **Error Handling**: Always include fallback logic
- **Documentation**: Add docstrings and comments

### Testing

- **Start Simple**: Test with mock data first
- **Edge Cases**: Test with extreme values
- **Real Data**: Validate with actual tickers
- **Performance**: Check execution time

### Code Quality

- **Readability**: Use clear variable names
- **Maintainability**: Keep methods small
- **Consistency**: Follow framework patterns
- **Comments**: Explain complex logic

## Performance Tips

### Rule-Based Agents

- Fastest execution
- No API calls
- Predictable behavior
- Best for high-frequency use

### LLM Agents

- Slower (API latency)
- More intelligent
- Variable behavior
- Best for detailed analysis

### Optimization

- Use rules for quick filters
- Use LLM for deep analysis
- Cache LLM responses
- Batch similar queries

## Security

### API Keys

Never commit API keys to code:

```python
# ❌ Don't do this
api_key = "sk-123456..."

# ✅ Do this
api_key = Config.get_openai_api_key()
```

### User Input

GUI validates all input:
- Filename validation
- Code injection prevention
- SQL injection protection (when using DB)

## Support

### Documentation

- **Framework**: `~/AI-Agent-Builder/README.md`
- **Examples**: `~/AI-Agent-Builder/examples/`
- **API Docs**: `~/AI-Agent-Builder/docs/`

### Getting Help

1. Check examples for patterns
2. Review framework documentation
3. Test with mock data first
4. Check error messages carefully

## Future Enhancements

Planned features:
- [ ] Visual rule builder with drag-and-drop
- [ ] Real-time agent performance charts
- [ ] Multi-agent comparison view
- [ ] Export agents to different formats
- [ ] Import agents from GitHub
- [ ] Agent marketplace/sharing

## Version History

**v1.0.0** (Current)
- Browse agents from examples/
- Create rule-based agents
- Create LLM-powered agents  
- Create hybrid agents
- Test with mock data
- Save agents to examples/

---

**Maintainer**: Your Team  
**Last Updated**: 2025-01-23  
**Status**: Production Ready
