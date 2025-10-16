# Creating Agents Guide

Learn how to build custom investment analysis agents from scratch.

---

## 🎯 What is an Agent?

An **agent** is a Python function that:
1. Receives a stock ticker
2. Analyzes available data
3. Returns a signal (bullish/bearish/neutral) with confidence

Think of agents as individual investment advisors, each with their own strategy and perspective.

---

## 🚀 Quick Start: Your First Agent

### Step 1: Create the Agent

Create a new file: `examples/my_agents.py`

```python
from agent_builder.agents import simple_agent

@simple_agent("My First Agent", weight=0.10)
def my_first_agent(ticker, context):
    """
    Simple P/E ratio strategy
    
    Strategy:
    - Buy if P/E < 15 (undervalued)
    - Sell if P/E > 30 (overvalued)
    - Hold otherwise
    """
    # Get P/E ratio from database
    pe_ratio = context.get_metric('pe_ratio')
    
    # Make decision
    if pe_ratio < 15:
        return "bullish", 0.8    # High confidence buy
    elif pe_ratio > 30:
        return "bearish", 0.7    # High confidence sell
    else:
        return "neutral", 0.5    # Uncertain
```

### Step 2: Register the Agent

```python
from agent_builder.agents.registry import get_registry

registry = get_registry()
registry.register(my_first_agent.agent, tags=['fundamental', 'value'])
```

### Step 3: Test It

```python
from agent_builder.agents.context import AgentContext

# Create context for AAPL
context = AgentContext("AAPL")

# Run agent
signal, confidence = my_first_agent("AAPL", context)

print(f"Signal: {signal}")
print(f"Confidence: {confidence}")
```

**That's it!** You've created your first agent.

---

## 📚 Agent Anatomy

### Basic Structure

```python
@simple_agent(
    name="Agent Name",        # Display name
    weight=0.10               # Importance (0.0-1.0)
)
def agent_function(ticker, context):
    """
    Agent description and strategy
    
    Args:
        ticker: Stock ticker symbol (e.g., "AAPL")
        context: AgentContext object for data access
    
    Returns:
        tuple: (signal, confidence)
        - signal: "bullish", "bearish", or "neutral"
        - confidence: 0.0 to 1.0
    """
    # 1. Get data
    data = context.get_metric('some_metric')
    
    # 2. Analyze
    if condition:
        signal = "bullish"
        confidence = 0.8
    else:
        signal = "bearish"
        confidence = 0.7
    
    # 3. Return
    return signal, confidence
```

### Required Elements

1. **`@simple_agent` decorator** - Registers the agent
2. **Name** - Unique, descriptive identifier
3. **Weight** - How much this agent influences consensus
4. **Function signature** - `(ticker, context)` parameters
5. **Return value** - `(signal, confidence)` tuple

### Signal Types

| Signal | Meaning | When to Use |
|--------|---------|-------------|
| `"bullish"` | Positive outlook | Recommend buying |
| `"bearish"` | Negative outlook | Recommend selling |
| `"neutral"` | No clear direction | Hold or uncertain |

### Confidence Levels

| Range | Interpretation | Example |
|-------|----------------|---------|
| 0.9 - 1.0 | Very high confidence | Strong signals aligned |
| 0.75 - 0.9 | High confidence | Multiple confirmations |
| 0.6 - 0.75 | Moderate confidence | Some uncertainty |
| 0.5 - 0.6 | Low confidence | Weak or mixed signals |
| 0.0 - 0.5 | Very uncertain | Avoid (use neutral) |

---

## 💡 Agent Patterns

### Pattern 1: Single Metric Agent

Simple threshold-based decision:

```python
@simple_agent("P/E Ratio", weight=0.10)
def pe_ratio_agent(ticker, context):
    """Buy low P/E stocks"""
    pe = context.get_metric('pe_ratio')
    
    if pe < 15:
        return "bullish", 0.8
    elif pe > 30:
        return "bearish", 0.7
    else:
        return "neutral", 0.5
```

**Use for:** Simple, single-factor strategies

### Pattern 2: Multi-Metric Scoring

Combine multiple factors with scoring:

```python
@simple_agent("Quality Score", weight=0.15)
def quality_agent(ticker, context):
    """Score based on multiple quality metrics"""
    
    score = 0
    
    # Profitability
    if context.get_metric('roe') > 20:
        score += 3
    if context.get_metric('profit_margin') > 15:
        score += 2
    
    # Growth
    if context.get_metric('revenue_growth') > 10:
        score += 2
    
    # Health
    if context.get_metric('debt_to_equity') < 0.5:
        score += 2
    
    # Decision
    if score >= 7:
        return "bullish", 0.9
    elif score >= 5:
        return "bullish", 0.75
    elif score >= 3:
        return "neutral", 0.6
    else:
        return "bearish", 0.65
```

**Use for:** Multi-factor fundamental analysis

### Pattern 3: Comparative Analysis

Compare current vs historical:

```python
@simple_agent("Momentum", weight=0.12)
def momentum_agent(ticker, context):
    """Compare recent vs older prices"""
    
    prices = context.get_price_data(days=20)
    
    if len(prices) < 20:
        return "neutral", 0.5
    
    # Recent average (5 days)
    recent = sum(p['close'] for p in prices[:5]) / 5
    
    # Older average (days 10-15)
    older = sum(p['close'] for p in prices[10:15]) / 5
    
    # Calculate momentum
    momentum = ((recent - older) / older) * 100
    
    if momentum > 5:
        return "bullish", 0.8
    elif momentum < -5:
        return "bearish", 0.8
    else:
        return "neutral", 0.5
```

**Use for:** Trend following, momentum strategies

### Pattern 4: Divergence Detection

Identify when signals conflict:

```python
@simple_agent("Price-Volume Divergence", weight=0.10)
def divergence_agent(ticker, context):
    """Detect price-volume divergences"""
    
    prices = context.get_price_data(days=10)
    
    if len(prices) < 10:
        return "neutral", 0.5
    
    # Price trend
    price_up = prices[0]['close'] > prices[9]['close']
    
    # Volume trend
    recent_vol = sum(p['volume'] for p in prices[:5]) / 5
    older_vol = sum(p['volume'] for p in prices[5:10]) / 5
    volume_up = recent_vol > older_vol
    
    # Divergence analysis
    if price_up and not volume_up:
        return "bearish", 0.7  # Weak rally
    elif not price_up and volume_up:
        return "bullish", 0.7  # Capitulation
    elif price_up and volume_up:
        return "bullish", 0.8  # Confirmed uptrend
    else:
        return "bearish", 0.6  # Confirmed downtrend
```

**Use for:** Identifying false signals, reversals

### Pattern 5: Cross-Source Validation

Combine different data sources:

```python
@simple_agent("Fundamental + Technical", weight=0.15)
def hybrid_agent(ticker, context):
    """Combine fundamental value with technical momentum"""
    
    # Fundamental: Is it cheap?
    pe = context.get_metric('pe_ratio')
    is_cheap = pe < 20
    
    # Technical: Is it trending up?
    technicals = context.get_latest_technicals()
    rsi = technicals.get('rsi_14', 50)
    is_oversold = rsi < 35
    
    # Combine
    if is_cheap and is_oversold:
        return "bullish", 0.9  # Value + technical confirmation
    elif is_cheap:
        return "bullish", 0.7  # Value alone
    elif is_oversold:
        return "bullish", 0.6  # Technical alone
    else:
        return "neutral", 0.5
```

**Use for:** Multi-factor strategies, confirmation signals

---

## 📊 Accessing Data

### Fundamental Data

```python
# Single metric
pe = context.get_metric('pe_ratio')
roe = context.get_metric('roe')
sector = context.get_metric('sector')

# All fundamentals
fundamentals = context.get_fundamentals()
# Returns: {'pe_ratio': 28.5, 'roe': 25.3, ...}

# Balance sheet
balance_sheet = context.get_balance_sheet()
cash = balance_sheet.get('cash_and_equivalents', 0)

# Cash flow
cash_flow = context.get_cash_flow()
fcf = cash_flow.get('free_cash_flow', 0)

# Earnings
earnings = context.get_earnings()
eps_surprise = earnings.get('eps_surprise', 0)
```

### Technical Data

```python
# Price data
prices = context.get_price_data(days=30)
current_price = context.get_latest_price()

# Loop through prices
for price in prices:
    date = price['date']
    close = price['close']
    volume = price['volume']

# Technical indicators
technicals = context.get_technical_indicators(days=10)
latest = context.get_latest_technicals()

rsi = latest.get('rsi_14', 50)
macd = latest.get('macd', 0)
sma_20 = latest.get('sma_20', 0)
```

### Sentiment Data

```python
# News
news = context.get_news(limit=20)
for article in news:
    headline = article['headline']
    sentiment = article['sentiment']  # positive/negative/neutral
    score = article['sentiment_score']  # -1.0 to 1.0

# Analyst ratings
ratings = context.get_analyst_ratings(limit=15)
for rating in ratings:
    firm = rating['analyst_firm']
    rating_type = rating['rating']  # buy/hold/sell
    target = rating['price_target']

# Insider trades
trades = context.get_insider_trades(limit=15)
for trade in trades:
    insider = trade['insider_name']
    type = trade['transaction_type']  # buy/sell
    value = trade['transaction_value']
```

### Risk Data

```python
# Risk metrics
risk = context.get_latest_risk_metrics()

volatility = risk.get('historical_volatility_30d', 0)
max_dd = risk.get('max_drawdown', 0)
sharpe = risk.get('sharpe_ratio', 0)
var_95 = risk.get('value_at_risk_95', 0)

# Options data
options = context.get_latest_options_data()
pc_ratio = options.get('put_call_ratio', 0)
iv = options.get('iv_30d', 0)
```

### Macro Data

```python
# Macro indicators (shared across all stocks)
macro = context.get_macro_indicators()

fed_rate = macro.get('fed_funds_rate', 0)
gdp = macro.get('gdp_growth', 0)
inflation = macro.get('inflation_rate', 0)
vix = macro.get('vix_level', 0)
```

### Complete Example

```python
@simple_agent("Comprehensive Analyzer", weight=0.20)
def comprehensive_agent(ticker, context):
    """Analyze using all data sources"""
    
    # Fundamentals
    pe = context.get_metric('pe_ratio')
    roe = context.get_metric('roe')
    
    # Technical
    technicals = context.get_latest_technicals()
    rsi = technicals.get('rsi_14', 50)
    
    # Sentiment
    news = context.get_news(limit=10)
    avg_sentiment = sum(n['sentiment_score'] for n in news) / len(news) if news else 0
    
    # Risk
    risk = context.get_latest_risk_metrics()
    sharpe = risk.get('sharpe_ratio', 0)
    
    # Macro
    macro = context.get_macro_indicators()
    gdp = macro.get('gdp_growth', 0)
    
    # Combine all factors
    score = 0
    if pe < 20: score += 1
    if roe > 15: score += 1
    if rsi < 40: score += 1
    if avg_sentiment > 0.2: score += 1
    if sharpe > 1.0: score += 1
    if gdp > 2.5: score += 1
    
    if score >= 5:
        return "bullish", 0.85
    elif score >= 3:
        return "bullish", 0.70
    elif score <= 1:
        return "bearish", 0.70
    else:
        return "neutral", 0.50
```

---

## 🎨 Agent Design Patterns

### Pattern: Threshold Strategy

Simple if/else based on thresholds:

```python
@simple_agent("Dividend Yield", weight=0.08)
def dividend_agent(ticker, context):
    """High dividend yield strategy"""
    dividend_yield = context.get_metric('dividend_yield')
    
    if dividend_yield > 4.0:
        return "bullish", 0.8   # High yield
    elif dividend_yield > 2.5:
        return "bullish", 0.6   # Moderate yield
    elif dividend_yield < 1.0:
        return "bearish", 0.6   # Low yield
    else:
        return "neutral", 0.5
```

### Pattern: Scoring System

Accumulate points across multiple factors:

```python
@simple_agent("Growth Score", weight=0.12)
def growth_score_agent(ticker, context):
    """Multi-factor growth scoring"""
    score = 0
    
    # Revenue growth
    if context.get_metric('revenue_growth') > 20:
        score += 3
    elif context.get_metric('revenue_growth') > 10:
        score += 2
    
    # Earnings growth
    if context.get_metric('earnings_growth') > 20:
        score += 3
    elif context.get_metric('earnings_growth') > 10:
        score += 2
    
    # Margins expanding
    if context.get_metric('profit_margin') > 15:
        score += 2
    
    # Convert score to signal
    if score >= 7:
        return "bullish", 0.9
    elif score >= 5:
        return "bullish", 0.75
    elif score >= 3:
        return "neutral", 0.6
    else:
        return "bearish", 0.65
```

### Pattern: Ratio Analysis

Calculate and compare ratios:

```python
@simple_agent("Efficiency Analyzer", weight=0.09)
def efficiency_agent(ticker, context):
    """Analyze operational efficiency"""
    
    asset_turnover = context.get_metric('asset_turnover')
    inventory_turnover = context.get_metric('inventory_turnover')
    profit_margin = context.get_metric('profit_margin')
    
    # Efficient operations + good margins
    if asset_turnover > 1.5 and profit_margin > 10:
        return "bullish", 0.75
    
    # Poor efficiency
    elif asset_turnover < 0.5:
        return "bearish", 0.65
    
    else:
        return "neutral", 0.5
```

### Pattern: Time Series Analysis

Analyze trends over time:

```python
@simple_agent("Price Momentum", weight=0.11)
def price_momentum_agent(ticker, context):
    """20-day price momentum"""
    
    prices = context.get_price_data(days=20)
    
    if len(prices) < 20:
        return "neutral", 0.5
    
    # Current vs 20 days ago
    current = prices[0]['close']
    baseline = prices[19]['close']
    
    momentum = ((current - baseline) / baseline) * 100
    
    if momentum > 10:
        return "bullish", 0.85
    elif momentum > 5:
        return "bullish", 0.70
    elif momentum < -10:
        return "bearish", 0.85
    elif momentum < -5:
        return "bearish", 0.70
    else:
        return "neutral", 0.5
```

### Pattern: Contrarian Strategy

Do the opposite of crowd sentiment:

```python
@simple_agent("Contrarian", weight=0.10)
def contrarian_agent(ticker, context):
    """Buy fear, sell greed"""
    
    news = context.get_news(limit=20)
    
    if not news:
        return "neutral", 0.5
    
    # Calculate sentiment
    positive = sum(1 for n in news if n['sentiment'] == 'positive')
    negative = sum(1 for n in news if n['sentiment'] == 'negative')
    
    sentiment_ratio = positive / len(news)
    
    # Contrarian: Do opposite
    if sentiment_ratio > 0.75:
        return "bearish", 0.7   # Too bullish = sell
    elif sentiment_ratio < 0.25:
        return "bullish", 0.8   # Too bearish = buy
    else:
        return "neutral", 0.5
```

### Pattern: Database Query

Access database directly for complex queries:

```python
@simple_agent("Custom Query", weight=0.10)
def custom_query_agent(ticker, context):
    """Execute custom database queries"""
    from agent_builder.repositories.connection import get_db_cursor
    
    with get_db_cursor() as cursor:
        if cursor is None:
            return "neutral", 0.5
        
        # Custom query
        cursor.execute("""
            SELECT AVG(sentiment_score)
            FROM mock_news
            WHERE ticker = %s
            AND published_at > NOW() - INTERVAL '7 days'
        """, (ticker,))
        
        result = cursor.fetchone()
        
        if result and result[0]:
            avg_sentiment = result[0]
            
            if avg_sentiment > 0.5:
                return "bullish", 0.8
            elif avg_sentiment < -0.5:
                return "bearish", 0.8
        
        return "neutral", 0.5
```

**Use for:** Complex queries, custom aggregations

---

## 🎯 Advanced Techniques

### Combining Multiple Signals

```python
@simple_agent("Multi-Signal Confluence", weight=0.15)
def confluence_agent(ticker, context):
    """Require multiple confirmations"""
    
    bullish_signals = 0
    bearish_signals = 0
    
    # Check fundamental
    if context.get_metric('pe_ratio') < 20:
        bullish_signals += 1
    
    # Check technical
    technicals = context.get_latest_technicals()
    if technicals.get('rsi_14', 50) < 35:
        bullish_signals += 1
    
    # Check sentiment
    news = context.get_news(limit=10)
    if news:
        avg_sentiment = sum(n['sentiment_score'] for n in news) / len(news)
        if avg_sentiment > 0.3:
            bullish_signals += 1
        elif avg_sentiment < -0.3:
            bearish_signals += 1
    
    # Require 2+ confirmations
    if bullish_signals >= 2:
        return "bullish", 0.85
    elif bearish_signals >= 2:
        return "bearish", 0.85
    else:
        return "neutral", 0.5
```

### Dynamic Confidence

Adjust confidence based on signal strength:

```python
@simple_agent("Dynamic Confidence", weight=0.12)
def dynamic_confidence_agent(ticker, context):
    """Confidence scales with signal strength"""
    
    pe = context.get_metric('pe_ratio')
    
    # Calculate deviation from average P/E of 20
    deviation = abs(pe - 20) / 20
    
    # More extreme = higher confidence
    base_confidence = min(0.5 + (deviation * 0.5), 0.95)
    
    if pe < 20:
        return "bullish", base_confidence
    elif pe > 20:
        return "bearish", base_confidence
    else:
        return "neutral", 0.5
```

### Sector-Specific Logic

```python
@simple_agent("Sector Specialist", weight=0.11)
def sector_specialist_agent(ticker, context):
    """Different logic for different sectors"""
    
    sector = context.get_metric('sector')
    pe = context.get_metric('pe_ratio')
    
    # Tech stocks: Higher P/E acceptable
    if sector == 'Technology':
        if pe < 30:
            return "bullish", 0.75
        elif pe > 50:
            return "bearish", 0.75
    
    # Banks: Low P/E preferred
    elif sector == 'Banking':
        if pe < 12:
            return "bullish", 0.8
        elif pe > 15:
            return "bearish", 0.7
    
    # Default logic for other sectors
    else:
        if pe < 18:
            return "bullish", 0.7
        elif pe > 25:
            return "bearish", 0.7
    
    return "neutral", 0.5
```

### Error Handling

```python
@simple_agent("Safe Agent", weight=0.10)
def safe_agent(ticker, context):
    """Proper error handling"""
    
    try:
        pe = context.get_metric('pe_ratio')
        
        # Validate data
        if pe is None or pe <= 0:
            logger.warning(f"Invalid P/E for {ticker}: {pe}")
            return "neutral", 0.5
        
        # Normal logic
        if pe < 15:
            return "bullish", 0.8
        else:
            return "bearish", 0.6
            
    except Exception as e:
        logger.error(f"Agent error for {ticker}: {e}")
        return "neutral", 0.5  # Safe default
```

---

## 🧪 Testing Your Agent

### Unit Testing

```python
# test_my_agent.py
import pytest
from agent_builder.agents.context import AgentContext
from examples.my_agents import my_first_agent

def test_bullish_signal():
    """Test agent returns bullish for low P/E"""
    context = AgentContext("AAPL")
    signal, confidence = my_first_agent("AAPL", context)
    
    # Assuming AAPL has low P/E in test data
    assert signal == "bullish"
    assert confidence > 0.7

def test_bearish_signal():
    """Test agent returns bearish for high P/E"""
    context = AgentContext("TSLA")  # High P/E stock
    signal, confidence = my_first_agent("TSLA", context)
    
    assert signal in ["bearish", "neutral"]
```

### Integration Testing

```python
def test_agent_with_real_analysis():
    """Test agent in full analysis"""
    from agent_builder.agents.registry import get_registry
    
    registry = get_registry()
    registry.register(my_first_agent.agent)
    
    # Run full analysis
    agents = registry.get_enabled_agents()
    context = AgentContext("AAPL")
    
    signals = []
    for agent in agents:
        signal = agent.analyze("AAPL")
        signals.append(signal)
    
    assert len(signals) > 0
```

### Manual Testing

```python
if __name__ == "__main__":
    # Test your agent directly
    from agent_builder.agents.context import AgentContext
    
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA']
    
    for ticker in tickers:
        context = AgentContext(ticker)
        signal, confidence = my_first_agent(ticker, context)
        print(f"{ticker}: {signal} ({confidence:.2f})")
```

---

## 📋 Best Practices

### DO ✅

**1. Document your strategy**
```python
@simple_agent("My Agent", weight=0.10)
def my_agent(ticker, context):
    """
    Clear description of what this agent does
    
    Strategy:
    - Buy when X happens
    - Sell when Y happens
    
    Edge cases:
    - Returns neutral if data missing
    """
```

**2. Handle missing data**
```python
pe = context.get_metric('pe_ratio', default=0)
if pe <= 0:
    return "neutral", 0.5  # Can't analyze without data
```

**3. Use appropriate confidence**
```python
# Strong signal with multiple confirmations
if all_factors_bullish:
    return "bullish", 0.9

# Weak signal with limited data
elif limited_data:
    return "bullish", 0.55
```

**4. Keep logic simple**
```python
# Good: Single clear purpose
def pe_agent(ticker, context):
    pe = context.get_metric('pe_ratio')
    return ("bullish" if pe < 20 else "bearish"), 0.7

# Bad: Too many factors, unclear
def everything_agent(ticker, context):
    # 50 lines of complex logic
    # Mixing fundamental, technical, sentiment
    # Hard to understand and maintain
```

**5. Add tags for organization**
```python
registry.register(
    my_agent.agent,
    tags=['fundamental', 'value', 'custom']
)
```

### DON'T ❌

**1. Don't ignore errors**
```python
# Bad
def bad_agent(ticker, context):
    pe = context.get_metric('pe_ratio')
    # What if pe is None? Division by zero!
    score = 100 / pe
    return "bullish", score
```

**2. Don't use hardcoded values**
```python
# Bad
if ticker == "AAPL":
    return "bullish", 0.9

# Good
sector = context.get_metric('sector')
if sector == "Technology":
    # Sector-specific logic
```

**3. Don't make assumptions about data**
```python
# Bad
prices = context.get_price_data(days=30)
current_price = prices[0]['close']  # Crashes if empty!

# Good
prices = context.get_price_data(days=30)
if not prices:
    return "neutral", 0.5
current_price = prices[0]['close']
```

**4. Don't return invalid values**
```python
# Bad
return "maybe", 1.5  # Invalid signal and confidence

# Good
return "neutral", 0.5  # Valid signal, valid confidence
```

**5. Don't access database directly (usually)**
```python
# Bad (bypasses pooling and caching)
import psycopg2
conn = psycopg2.connect(...)

# Good (uses connection pool)
with get_db_cursor() as cursor:
    cursor.execute(...)
```

---

## 🎓 Real-World Examples

### Example 1: Magic Formula (Joel Greenblatt)

```python
@simple_agent("Magic Formula", weight=0.15)
def magic_formula_agent(ticker, context):
    """
    Joel Greenblatt's Magic Formula
    High earnings yield + high return on capital
    """
    # Earnings yield (inverse of P/E)
    pe = context.get_metric('pe_ratio')
    earnings_yield = (1 / pe * 100) if pe > 0 else 0
    
    # Return on invested capital
    roic = context.get_metric('roic')
    
    # Score both factors
    score = 0
    
    if earnings_yield > 10:  # E/P > 10%
        score += 2
    elif earnings_yield > 7:
        score += 1
    
    if roic > 20:
        score += 2
    elif roic > 15:
        score += 1
    
    # Need both factors
    if score >= 3:
        return "bullish", 0.85
    elif score >= 2:
        return "bullish", 0.7
    else:
        return "neutral", 0.5
```

### Example 2: Piotroski F-Score

```python
@simple_agent("Piotroski F-Score", weight=0.14)
def piotroski_agent(ticker, context):
    """
    9-point fundamental scoring system
    """
    score = 0
    
    # Profitability (4 points)
    if context.get_metric('net_income') > 0:
        score += 1
    if context.get_metric('roe') > 0:
        score += 1
    
    cash_flow = context.get_cash_flow()
    if cash_flow and cash_flow.get('operating_cash_flow', 0) > 0:
        score += 1
    if cash_flow and cash_flow.get('operating_cash_flow', 0) > context.get_metric('net_income'):
        score += 1  # Quality earnings
    
    # Leverage (3 points)
    if context.get_metric('debt_to_equity') < 0.5:
        score += 1
    if context.get_metric('current_ratio') > 1.5:
        score += 1
    
    # Operating Efficiency (2 points)
    if context.get_metric('gross_margin') > 40:
        score += 1
    if context.get_metric('asset_turnover') > 1.0:
        score += 1
    
    # F-Score interpretation
    if score >= 8:
        return "bullish", 0.9
    elif score >= 6:
        return "bullish", 0.75
    elif score >= 4:
        return "neutral", 0.6
    elif score >= 2:
        return "bearish", 0.65
    else:
        return "bearish", 0.8
```

### Example 3: Turtle Trading System (Simplified)

```python
@simple_agent("Turtle Breakout", weight=0.12)
def turtle_breakout_agent(ticker, context):
    """
    Breakout strategy based on Turtle Trading
    Buy 20-day highs, sell 20-day lows
    """
    prices = context.get_price_data(days=21)
    
    if len(prices) < 21:
        return "neutral", 0.5
    
    current_price = prices[0]['close']
    
    # 20-day high and low (excluding current)
    high_20 = max(p['high'] for p in prices[1:21])
    low_20 = min(p['low'] for p in prices[1:21])
    
    # Breakout above 20-day high
    if current_price > high_20:
        return "bullish", 0.85
    
    # Breakdown below 20-day low
    elif current_price < low_20:
        return "bearish", 0.85
    
    # Within range
    else:
        return "neutral", 0.5
```

---

## 🛠️ Debugging Agents

### Add Logging

```python
import logging
logger = logging.getLogger(__name__)

@simple_agent("Debug Agent", weight=0.10)
def debug_agent(ticker, context):
    """Agent with debug logging"""
    
    pe = context.get_metric('pe_ratio')
    logger.info(f"[{ticker}] P/E ratio: {pe}")
    
    if pe < 20:
        logger.info(f"[{ticker}] Bullish signal (low P/E)")
        return "bullish", 0.8
    else:
        logger.info(f"[{ticker}] Bearish signal (high P/E)")
        return "bearish", 0.6
```

### Test with Print Statements

```python
@simple_agent("Print Debug", weight=0.10)
def print_debug_agent(ticker, context):
    """Debug with print statements"""
    
    fundamentals = context.get_fundamentals()
    print(f"\n=== {ticker} ===")
    print(f"P/E: {fundamentals.get('pe_ratio')}")
    print(f"ROE: {fundamentals.get('roe')}")
    print(f"Debt/Equity: {fundamentals.get('debt_to_equity')}")
    
    # Your logic here
    return "neutral", 0.5
```

### Check Data Availability

```python
@simple_agent("Data Checker", weight=0.10)
def data_checker_agent(ticker, context):
    """Verify what data is available"""
    
    fundamentals = context.get_fundamentals()
    prices = context.get_price_data(days=5)
    news = context.get_news(limit=5)
    
    print(f"\n{ticker} Data Availability:")
    print(f"  Fundamentals: {len(fundamentals)} fields")
    print(f"  Prices: {len(prices)} days")
    print(f"  News: {len(news)} articles")
    
    if not fundamentals or not prices:
        return "neutral", 0.5  # Insufficient data
    
    # Continue with analysis
    return "neutral", 0.5
```

---

## 📦 Organizing Agents

### File Structure

```python
# examples/my_strategy_agents.py

from agent_builder.agents import simple_agent
import logging

logger = logging.getLogger(__name__)

# Group related agents together
@simple_agent("Strategy A", weight=0.15)
def strategy_a_agent(ticker, context):
    pass

@simple_agent("Strategy B", weight=0.12)
def strategy_b_agent(ticker, context):
    pass

# Registration function
def register_my_strategy_agents():
    """Register all agents from this file"""
    from agent_builder.agents.registry import get_registry
    
    registry = get_registry()
    
    registry.register(strategy_a_agent.agent, tags=['custom', 'strategy_a'])
    registry.register(strategy_b_agent.agent, tags=['custom', 'strategy_b'])
    
    logger.info("✅ Registered 2 custom strategy agents")
```

### Tags for Organization

Use tags to categorize agents:

```python
registry.register(
    agent=my_agent.agent,
    tags=[
        'fundamental',  # Category
        'value',        # Sub-category
        'dividend',     # Strategy
        'conservative', # Style
        'custom'        # Source
    ]
)

# Later, retrieve by tag
value_agents = registry.get_by_tag('value')
```

---

## 🎯 Agent Weights

### Understanding Weights

Weights control agent influence in consensus:

```python
@simple_agent("High Weight Agent", weight=0.20)  # 20% influence
@simple_agent("Medium Weight Agent", weight=0.10)  # 10% influence
@simple_agent("Low Weight Agent", weight=0.05)  # 5% influence
```

**Note:** Weights are informational only in current consensus algorithm. Future versions will use weighted voting.

### Choosing Weights

**High Weight (0.15-0.25):**
- Proven strategies
- Multiple confirmations
- Composite agents
- Core strategies

**Medium Weight (0.08-0.14):**
- Single-factor strategies
- Sector-specific logic
- Specialized agents

**Low Weight (0.05-0.07):**
- Experimental strategies
- Narrow focus
- Secondary indicators

### Example Portfolio

```python
# Conservative portfolio (total weight ~1.0)
registry.register(value_investor.agent, weight=0.25)      # Core
registry.register(quality_screener.agent, weight=0.20)    # Core
registry.register(downside_protection.agent, weight=0.20) # Risk
registry.register(balance_sheet.agent, weight=0.15)       # Health
registry.register(dividend_yield.agent, weight=0.10)      # Income
registry.register(news_sentiment.agent, weight=0.10)      # Sentiment
```

---

## 🚀 Next Steps

### Learn More

- **[Architecture Guide](architecture.md)** - Understand the system
- **[API Reference](api-reference.md)** - API documentation
- **Example Agents** - Study 61 professional agents in `examples/`

### Build Your Strategy

1. Identify your investment philosophy
2. Break it into individual factors
3. Create agents for each factor
4. Test with mock data
5. Combine into portfolio
6. Backtest and refine

### Deploy to Production

1. Replace mock data with real APIs
2. Add authentication
3. Set up monitoring
4. Deploy with Docker/Kubernetes

---

**Ready to build?** Start with the patterns above and iterate!