# Creating Custom Agents

## Agent Basics

An agent is a function that:
1. Takes a ticker symbol
2. Accesses data via context
3. Returns a signal (bullish/bearish/neutral) and confidence

## Simple Agent

```python
from agent_builder.agents.builder import simple_agent

@simple_agent("My Agent", weight=0.15)
def my_agent(ticker, context):
    # Get data
    pe_ratio = context.get_metric('pe_ratio')
    
    # Make decision
    if pe_ratio < 15:
        return "bullish", 0.8
    else:
        return "neutral", 0.6
```

## AgentContext Methods

### Get Single Metric
```python
pe = context.get_metric('pe_ratio', default=0)
roe = context.get_metric('roe', default=0)
```

### Get All Fundamentals
```python
fund = context.get_fundamentals()
# Returns: {'pe_ratio': 18.5, 'roe': 22.3, ...}
```

### Get News
```python
news = context.get_news(limit=10)
# Returns: [{'headline': '...', 'sentiment': 'positive'}, ...]
```

### Get Price Data
```python
prices = context.get_price_data(days=30)
# Returns: [{'date': '2024-10-15', 'close': 175.23}, ...]
```

### Get Insider Trades
```python
trades = context.get_insider_trades(limit=15)
# Returns: [{'insider_name': 'CEO', 'transaction_type': 'buy'}, ...]
```

## Multi-Factor Agent

```python
@simple_agent("Multi-Factor Agent", weight=0.20)
def multi_factor_agent(ticker, context):
    # Get multiple metrics
    fund = context.get_fundamentals()
    
    # Score multiple factors
    score = 0
    if fund['pe_ratio'] < 20: score += 1
    if fund['roe'] > 15: score += 1
    if fund['debt_to_equity'] < 0.5: score += 1
    if fund['profit_margin'] > 15: score += 1
    
    # Return based on score
    if score >= 3:
        return "bullish", 0.85
    elif score >= 2:
        return "neutral", 0.65
    else:
        return "bearish", 0.70
```

## LLM-Powered Agent

```python
@simple_agent("LLM Analyst", weight=0.18)
def llm_analyst(ticker, context):
    from agent_builder.llm.factory import get_llm_provider
    from agent_builder.agents.personas import AgentPersonas
    
    llm = get_llm_provider()
    if not llm:
        return "neutral", 0.5
    
    fund = context.get_fundamentals()
    
    prompt = f"Analyze {ticker}: PE={fund['pe_ratio']}, ROE={fund['roe']}"
    
    response = llm.generate(
        prompt=prompt,
        system_prompt=AgentPersonas.FUNDAMENTAL_ANALYST
    )
    
    if "bullish" in response.lower():
        return "bullish", 0.80
    else:
        return "neutral", 0.65
```

## Register Your Agent

```python
# In examples/register_agents.py

from agent_builder.agents.registry import get_registry

registry = get_registry()
registry.register(
    my_agent.agent,
    weight=0.15,
    tags=['custom', 'my-strategy']
)
```

## Best Practices

1. **Use context methods** - Don't query database directly
2. **Cache is automatic** - AgentContext caches queries
3. **Handle missing data** - Use default parameters
4. **Clear logic** - Comment your thresholds
5. **Test independently** - Before registering with API

## Examples

See `examples/` directory for:
- Basic agents
- Fundamental analysis agents
- LLM-powered agents
- Sentiment analysis agents