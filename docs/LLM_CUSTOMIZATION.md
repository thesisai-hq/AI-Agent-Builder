# Making Your AI Smarter (or More Creative)

When using AI like ChatGPT or Claude in your agents, you can control **how** the AI thinks. This guide explains the two main settings: **temperature** and **max tokens**.

## The Two Magic Dials

Think of your AI agent as having two control dials:

### Dial 1: Temperature (Creativity vs. Focus)

**What it does:** Controls how creative vs. consistent the AI is.

```
0.0 ←―――――――― 0.5 ―――――――→ 1.0

Boring robot    Normal     Creative artist
Always same     Balanced   Always different
```

**Examples:**

**Temperature = 0.2** (Very focused)
- Ask 5 times: Gets nearly identical answers
- Good for: Analysis, math, consistent results
- Like: A very serious, methodical analyst

**Temperature = 0.7** (Balanced - Default)
- Ask 5 times: Similar answers with small variations
- Good for: General use, most tasks
- Like: A normal human expert

**Temperature = 0.9** (Very creative)
- Ask 5 times: Gets different creative answers each time
- Good for: Brainstorming, exploring ideas
- Like: A creative thinker with new perspectives

### Dial 2: Max Tokens (Response Length)

**What it does:** Controls how long the AI's response can be.

```
500 tokens ←―――― 1000 ―――→ 2000 ―――→ 4000

Brief summary   Standard    Detailed    Comprehensive
1-2 paragraphs  2-3 para.   5-6 para.   Multiple pages
```

**Rule of thumb:** 1000 tokens ≈ 750 words ≈ 3 paragraphs

**Examples:**

**500 tokens:**
```
"Apple looks good. Low PE ratio of 25. Revenue growing 
at 8%. Profit margins strong at 25%. Recommend buy."
```

**2000 tokens:**
```
"Apple Inc. presents a compelling investment opportunity 
for several reasons. First, the valuation metrics show 
a PE ratio of 25, which is reasonable given...

The company's revenue growth of 8% annually demonstrates 
stability while the profit margin of 25% indicates...

However, investors should consider the following risks:
1. Market saturation in smartphone segment
2. Dependence on China for manufacturing...

[Several more paragraphs of detailed analysis]"
```

## How to Use These Settings

### In Your Agent Code

```python
from agent_framework import Agent, AgentConfig, LLMConfig

class MyAgent(Agent):
    def __init__(self):
        config = AgentConfig(
            name="My Agent",
            llm=LLMConfig(
                provider='openai',
                temperature=0.5,    # ← Change this
                max_tokens=1500,    # ← Change this
                system_prompt="You are a financial analyst..."
            )
        )
        super().__init__(config)
```

### Quick Examples

**Conservative Risk Analyst** (Very focused, brief):
```python
llm=LLMConfig(
    provider='openai',
    temperature=0.2,   # Very consistent
    max_tokens=800,    # Brief summaries
    system_prompt="You are a conservative risk analyst."
)
```

**Creative Strategist** (More ideas, detailed):
```python
llm=LLMConfig(
    provider='anthropic',
    temperature=0.9,   # Creative thinking
    max_tokens=2500,   # Detailed analysis
    system_prompt="You are an innovative strategist."
)
```

**Balanced Analyst** (Middle ground):
```python
llm=LLMConfig(
    provider='ollama',
    temperature=0.5,   # Balanced
    max_tokens=1200,   # Standard detail
    system_prompt="You are a stock analyst."
)
```

## Temperature Guide - When to Use What

### Temperature 0.0 - 0.3 (The Robot)

**Best for:**
- Risk analysis (need consistent evaluation)
- Math calculations
- Following strict rules
- Compliance checks
- When you need the SAME answer every time

**Example use case:**
```python
# Risk assessment needs to be consistent
class RiskAnalyst(Agent):
    def __init__(self):
        config = AgentConfig(
            name="Risk Analyst",
            llm=LLMConfig(
                provider='openai',
                temperature=0.2,    # Very focused
                system_prompt="You are a risk analyst. Be conservative and consistent."
            )
        )
        super().__init__(config)
```

**What it feels like:**
- Asks about Apple 5 times → Gets nearly identical answers
- Very predictable
- Sometimes feels "boring" but that's the point!

### Temperature 0.4 - 0.7 (The Professional)

**Best for:**
- General stock analysis
- Writing reports
- Most everyday tasks
- When you want "normal" AI behavior

**This is the DEFAULT for good reason!**

**Example use case:**
```python
# Standard analysis
class StandardAnalyst(Agent):
    def __init__(self):
        config = AgentConfig(
            name="Analyst",
            llm=LLMConfig(
                provider='openai',
                temperature=0.5,    # Balanced
                system_prompt="You are a stock analyst."
            )
        )
        super().__init__(config)
```

**What it feels like:**
- Asks about Apple 5 times → Similar answers, slight variations
- Professional and reasonable
- What most people expect from AI

### Temperature 0.8 - 1.0 (The Creative)

**Best for:**
- Brainstorming investment ideas
- Finding non-obvious opportunities
- Strategy development
- When you want DIFFERENT perspectives

**Example use case:**
```python
# Creative strategy
class Strategist(Agent):
    def __init__(self):
        config = AgentConfig(
            name="Creative Strategist",
            llm=LLMConfig(
                provider='anthropic',
                temperature=0.9,    # Very creative
                system_prompt="Think outside the box. Find unique opportunities."
            )
        )
        super().__init__(config)
```

**What it feels like:**
- Asks about Apple 5 times → Gets 5 different creative angles
- Sometimes brilliant, sometimes odd
- Good for exploring possibilities

## Max Tokens Guide - How Much Detail?

### 500-1000 Tokens (The Summary)

**Best for:**
- Quick buy/sell/hold signals
- Trading decisions
- Brief summaries
- When time matters

**Example:**
```python
llm=LLMConfig(
    provider='openai',
    temperature=0.5,
    max_tokens=600,     # Brief
    system_prompt="Give quick, actionable recommendations."
)
```

**You get:**
- 2-3 short paragraphs
- Key points only
- Fast to read
- Good for quick decisions

### 1000-2000 Tokens (The Standard)

**Best for:**
- Regular analysis
- Most use cases
- Balanced detail
- Daily work

**Example:**
```python
llm=LLMConfig(
    provider='openai',
    temperature=0.5,
    max_tokens=1500,    # Standard
    system_prompt="Provide balanced analysis."
)
```

**You get:**
- 4-6 paragraphs
- Key points + some detail
- Reasonable length
- Most common setting

### 2000-4000 Tokens (The Deep Dive)

**Best for:**
- Research reports
- Comprehensive analysis
- Due diligence
- When detail matters more than speed

**Example:**
```python
llm=LLMConfig(
    provider='anthropic',  # Claude handles long responses well
    temperature=0.5,
    max_tokens=3000,       # Detailed
    system_prompt="Provide comprehensive, detailed analysis."
)
```

**You get:**
- Full analysis (multiple pages)
- Multiple perspectives
- Detailed reasoning
- Takes longer to read

## Real-World Examples

### Example 1: Trading Bot (Quick Decisions)

```python
class TradingBot(Agent):
    def __init__(self):
        config = AgentConfig(
            name="Trading Bot",
            llm=LLMConfig(
                provider='openai',
                model='gpt-3.5-turbo',   # Fast
                temperature=0.3,         # Consistent
                max_tokens=500,          # Brief
                system_prompt="Give quick buy/sell/hold recommendations with brief reasoning."
            )
        )
        super().__init__(config)
```

**Why these settings?**
- Low temperature: Need consistent signals, not random ones
- Low tokens: Just need the decision, not an essay
- Fast model: Speed matters for trading

### Example 2: Research Analyst (Detailed Reports)

```python
class ResearchAnalyst(Agent):
    def __init__(self):
        config = AgentConfig(
            name="Research Analyst",
            llm=LLMConfig(
                provider='anthropic',
                model='claude-3-5-sonnet-20241022',  # Good at long responses
                temperature=0.5,                      # Balanced
                max_tokens=3000,                      # Detailed
                system_prompt="Provide comprehensive stock analysis covering valuation, growth, risks, and opportunities."
            )
        )
        super().__init__(config)
```

**Why these settings?**
- Medium temperature: Want thorough but not random
- High tokens: Need detailed analysis
- Claude: Better at long, structured responses

### Example 3: Opportunity Scout (Creative Ideas)

```python
class OpportunityScout(Agent):
    def __init__(self):
        config = AgentConfig(
            name="Opportunity Scout",
            llm=LLMConfig(
                provider='openai',
                model='gpt-4',          # Most creative
                temperature=0.9,        # High creativity
                max_tokens=2000,        # Detailed enough
                system_prompt="Find non-obvious investment opportunities. Think creatively about future potential."
            )
        )
        super().__init__(config)
```

**Why these settings?**
- High temperature: Want creative, diverse ideas
- Medium-high tokens: Need reasoning for ideas
- GPT-4: Most capable for creative thinking

## Creating Multiple Agents with Different Settings

You can create a "team" of agents with different personalities:

```python
# Conservative analyst (focused, brief)
conservative = Agent(AgentConfig(
    name="Conservative",
    llm=LLMConfig(provider='openai', temperature=0.2, max_tokens=800)
))

# Balanced analyst (middle ground)
balanced = Agent(AgentConfig(
    name="Balanced",
    llm=LLMConfig(provider='openai', temperature=0.5, max_tokens=1200)
))

# Aggressive trader (creative, brief)
aggressive = Agent(AgentConfig(
    name="Aggressive",
    llm=LLMConfig(provider='openai', temperature=0.9, max_tokens=1000)
))

# Get different perspectives on same stock!
for agent in [conservative, balanced, aggressive]:
    signal = agent.analyze('AAPL', data)
    print(f"{agent.config.name}: {signal.direction}")
```

**Result:** Three different opinions on the same stock!

## Common Questions

**Q: What settings should I use?**  
A: Start with `temperature=0.5, max_tokens=1500` (the defaults). Adjust based on results.

**Q: Higher temperature = smarter AI?**  
A: No! Higher = more creative/random. Lower = more focused/consistent. Neither is "smarter."

**Q: Do more tokens cost more money?**  
A: Yes! More tokens = more words = higher API costs. Use only what you need.

**Q: Can I change settings for each query?**  
A: No, settings are set when you create the agent. But you can create multiple agents with different settings!

**Q: What if I want consistent AND creative?**  
A: You can't have both simultaneously. Create two agents: one focused (temp=0.3) and one creative (temp=0.9).

## Troubleshooting

**AI responses are too random:**
```python
# Lower the temperature
temperature=0.3  # Instead of 0.7
```

**AI responses are too boring:**
```python
# Raise the temperature
temperature=0.8  # Instead of 0.5
```

**Responses are too short:**
```python
# Increase max_tokens
max_tokens=2000  # Instead of 1000
```

**Responses are too long (wasting money):**
```python
# Decrease max_tokens
max_tokens=800  # Instead of 2000
```

**Responses cut off mid-sentence:**
```python
# Response hit the limit! Increase max_tokens
max_tokens=2000  # Or more
```

## Cost Considerations

More tokens = more money spent on API calls.

**Approximate costs (OpenAI GPT-4):**
- 500 tokens: ~$0.01 per analysis
- 1000 tokens: ~$0.02 per analysis
- 2000 tokens: ~$0.04 per analysis
- 4000 tokens: ~$0.08 per analysis

**If analyzing 100 stocks/day:**
- 500 tokens: $1/day = $30/month
- 2000 tokens: $4/day = $120/month

**💡 Pro tip:** Use `gpt-3.5-turbo` for quick tasks (10x cheaper!) and `gpt-4` only when you need maximum quality.

## Next Steps

1. **Start with defaults**: `temperature=0.5, max_tokens=1500`
2. **Test on a few stocks**: See if you like the responses
3. **Adjust one setting at a time**: See what changes
4. **Create specialized agents**: Different settings for different tasks

## More Examples

See [examples/04_custom_llm_config.py](../examples/04_custom_llm_config.py) for working code with different temperature and token settings!

---

**Remember**: There's no "perfect" setting - it depends on your use case. Experiment and find what works for you!
