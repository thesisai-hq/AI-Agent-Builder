# Framework Quick Start - For Developers

**Use AI-Agent-Builder as a Python framework** without the GUI.

**Audience:** 💻 Developers, Researchers, Python programmers

**Alternative:** Prefer visual interface? See [GUI_QUICK_START.md](../GUI_QUICK_START.md)

---

## What is the Framework?

AI-Agent-Builder is a Python framework for building investment analysis agents programmatically.

**Use it when:**
- ✅ You want full programmatic control
- ✅ Building custom investment systems
- ✅ Integrating into larger applications
- ✅ Automating workflows
- ✅ Deploying as REST API service
- ✅ Prefer code over GUI

**Don't need the GUI?** Skip it entirely - use pure Python!

---

## 5-Minute Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/thesisai-hq/AI-Agent-Builder.git
cd AI-Agent-Builder

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate.bat  # Windows

# Install framework
pip install -e ".[all]"

# Setup database
cp .env.example .env
docker compose up -d postgres
sleep 10
python seed_data.py
```

---

### Your First Agent

```python
# my_first_agent.py
from agent_framework import Agent, Signal, Database, Config
import asyncio

class ValueAgent(Agent):
    """Simple value investing agent."""
    
    async def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze based on PE ratio."""
        pe = data.get('pe_ratio', 0)
        
        if pe < 15:
            return Signal(
                direction='bullish',
                confidence=0.8,
                reasoning=f'Undervalued: PE={pe:.1f}'
            )
        elif pe > 30:
            return Signal(
                direction='bearish',
                confidence=0.7,
                reasoning=f'Overvalued: PE={pe:.1f}'
            )
        else:
            return Signal(
                direction='neutral',
                confidence=0.6,
                reasoning=f'Fair value: PE={pe:.1f}'
            )

async def main():
    # Connect to database
    db = Database(Config.get_database_url())
    await db.connect()
    
    # Create agent
    agent = ValueAgent()
    
    # Analyze all stocks
    for ticker in await db.list_tickers():
        data = await db.get_fundamentals(ticker)
        signal = await agent.analyze(ticker, data)
        
        print(f"{ticker}: {signal.direction.upper()} ({signal.confidence:.0%})")
        print(f"  {signal.reasoning}")
    
    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

**Run it:**
```bash
python my_first_agent.py
```

**Output:**
```
AAPL: NEUTRAL (60%)
  Fair value: PE=28.5
MSFT: NEUTRAL (60%)
  Fair value: PE=32.1
TSLA: BEARISH (70%)
  Overvalued: PE=52.3
JPM: BULLISH (80%)
  Undervalued: PE=11.2
```

**✅ Done!** You've created and run your first agent.

---

## Core Framework Concepts

### 1. Agent Base Class

**All agents inherit from Agent:**

```python
from agent_framework import Agent, Signal

class MyAgent(Agent):
    async def analyze(self, ticker: str, data: dict) -> Signal:
        # Your logic here
        return Signal(direction='...', confidence=0.8, reasoning='...')
```

**Required:**
- Inherit from `Agent`
- Implement `async def analyze()`
- Return `Signal` object

**Optional:**
- Override `__init__()` for configuration
- Use `self.llm` for AI analysis
- Use `self.rag` for document analysis

---

### 2. Signal Object

**Every analysis returns a Signal:**

```python
from agent_framework import Signal

signal = Signal(
    direction='bullish',   # 'bullish', 'bearish', or 'neutral'
    confidence=0.75,       # 0.0 to 1.0
    reasoning='Strong fundamentals with PE=12'
)

# Immutable - can't change after creation
# signal.confidence = 0.5  # ❌ Error: frozen model

# Access properties
print(signal.direction)    # 'bullish'
print(signal.confidence)   # 0.75
print(signal.timestamp)    # Auto-generated
```

---

### 3. Database Client

**Access financial data:**

```python
from agent_framework import Database, Config
import asyncio

async def get_stock_data():
    db = Database(Config.get_database_url())
    await db.connect()
    
    # List available tickers
    tickers = await db.list_tickers()
    print(f"Available: {tickers}")
    
    # Get fundamentals
    data = await db.get_fundamentals('AAPL')
    print(f"PE Ratio: {data['pe_ratio']}")
    print(f"ROE: {data['roe']}%")
    
    # Get price history (last 30 days)
    prices = await db.get_prices('AAPL', days=30)
    print(f"Latest close: ${prices[0]['close']}")
    
    # Get news
    news = await db.get_news('AAPL', limit=5)
    for item in news:
        print(f"{item['date']}: {item['headline']}")
    
    await db.disconnect()

asyncio.run(get_stock_data())
```

---

### 4. LLM Integration

**Add AI to your agents:**

```python
from agent_framework import Agent, AgentConfig, LLMConfig, Signal
from agent_framework import format_fundamentals, parse_llm_signal

class AIValueAgent(Agent):
    """AI-powered value investor."""
    
    def __init__(self):
        config = AgentConfig(
            name="AI Value Agent",
            description="Uses AI for value analysis",
            llm=LLMConfig(
                provider='ollama',        # or 'openai', 'anthropic'
                model='llama3.2',
                temperature=0.5,          # Focused analysis
                max_tokens=1500,
                system_prompt="""You are a value investor like Warren Buffett.
                Focus on business quality, competitive advantages, and margin of safety.
                Be conservative and thorough."""
            )
        )
        super().__init__(config)
    
    async def analyze(self, ticker: str, data: dict) -> Signal:
        # Format data for LLM
        fundamentals = format_fundamentals(data)
        
        # Create prompt
        prompt = f"""Analyze {ticker} as a value investment:

{fundamentals}

Provide recommendation.
Format: DIRECTION|CONFIDENCE|REASONING"""
        
        # Query LLM (uses system_prompt automatically)
        response = self.llm.chat(prompt)
        
        # Parse response into Signal
        return parse_llm_signal(response, f"AI analysis of {ticker}")
```

**Prerequisites:**
```bash
# For Ollama (free, local)
pip install ollama
ollama pull llama3.2
ollama serve  # Keep running

# For OpenAI (paid)
# Add to .env: OPENAI_API_KEY=sk-...

# For Anthropic (paid)
# Add to .env: ANTHROPIC_API_KEY=sk-ant-...
```

---

### 5. RAG Document Analysis

**Analyze long documents:**

```python
from agent_framework import Agent, AgentConfig, LLMConfig, RAGConfig, Signal

class SECAnalystAgent(Agent):
    """Analyzes SEC filings."""
    
    def __init__(self):
        config = AgentConfig(
            name="SEC Analyst",
            llm=LLMConfig(provider='ollama', model='llama3.2'),
            rag=RAGConfig(chunk_size=300, top_k=5)
        )
        super().__init__(config)
    
    async def analyze(self, ticker: str, data: dict) -> Signal:
        # data should contain 'document' key with filing text
        document = data.get('document', '')
        
        # Add document to RAG
        self.rag.add_document(document)
        
        # Query for specific information
        risk_context = self.rag.query("What are the main risk factors?")
        
        # Use LLM to analyze
        prompt = f"Analyze risks for {ticker}: {risk_context}"
        response = self.llm.chat(prompt)
        
        return parse_llm_signal(response)

# Usage
async def analyze_filing():
    db = Database(Config.get_database_url())
    await db.connect()
    
    # Get SEC filing
    filing_text = await db.get_filing('AAPL')
    
    agent = SECAnalystAgent()
    signal = await agent.analyze('AAPL', {'document': filing_text})
    
    print(f"{signal.direction}: {signal.reasoning}")
    
    await db.disconnect()
```

---

## Advanced Usage

### Multi-Agent Orchestration

**Run multiple agents in parallel:**

```python
import asyncio
from agent_framework import Database, Config

async def consensus_analysis(ticker: str):
    """Get consensus from multiple agents."""
    
    db = Database(Config.get_database_url())
    await db.connect()
    
    data = await db.get_fundamentals(ticker)
    
    # Create different agents
    agents = {
        'value': ValueAgent(),
        'growth': GrowthAgent(),
        'quality': QualityAgent()
    }
    
    # Run all in parallel (fast!)
    signals = await asyncio.gather(*[
        agent.analyze(ticker, data)
        for agent in agents.values()
    ])
    
    # Aggregate results
    bullish = sum(1 for s in signals if s.direction == 'bullish')
    bearish = sum(1 for s in signals if s.direction == 'bearish')
    
    # Consensus logic
    if bullish > bearish:
        consensus = 'bullish'
        confidence = bullish / len(signals)
    elif bearish > bullish:
        consensus = 'bearish'
        confidence = bearish / len(signals)
    else:
        consensus = 'neutral'
        confidence = 0.5
    
    await db.disconnect()
    
    return consensus, confidence, signals

# Run
consensus, conf, details = asyncio.run(consensus_analysis('AAPL'))
print(f"Consensus: {consensus} ({conf:.0%})")
```

---

### Deploy as REST API

**Make your agents available via HTTP:**

```python
# server.py
from agent_framework import api_app, register_agent_instance
import uvicorn

# Create and register agents
value_agent = ValueAgent()
ai_agent = AIValueAgent()

register_agent_instance("value", value_agent)
register_agent_instance("ai", ai_agent)

# Run server
if __name__ == "__main__":
    uvicorn.run(api_app, host="0.0.0.0", port=8000)
```

**Start server:**
```bash
python server.py
```

**Use API:**
```bash
# Health check
curl http://localhost:8000/health

# List agents
curl http://localhost:8000/agents

# Run analysis
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"agent_name":"value","ticker":"AAPL"}'
```

**API docs:** http://localhost:8000/docs (automatic Swagger UI)

---

### Custom Database Queries

**Direct SQL access when needed:**

```python
async def custom_query():
    db = Database(Config.get_database_url())
    await db.connect()
    
    # Custom SQL query
    async with db.acquire() as conn:
        rows = await conn.fetch("""
            SELECT ticker, pe_ratio, roe, profit_margin
            FROM fundamentals
            WHERE sector = $1 
              AND pe_ratio < $2
              AND roe > $3
            ORDER BY pe_ratio ASC
        """, 'Technology', 20, 15)
        
        for row in rows:
            print(f"{row['ticker']}: PE={row['pe_ratio']}, ROE={row['roe']}%")
    
    await db.disconnect()
```

---

## Framework Architecture

### Import Patterns

```python
# Core classes
from agent_framework import Agent, Signal, AgentConfig

# Database
from agent_framework import Database, DatabaseConfig

# LLM
from agent_framework import LLMConfig, LLMClient

# RAG
from agent_framework import RAGConfig, RAGSystem

# API
from agent_framework import api_app, register_agent_instance

# Utilities
from agent_framework import (
    parse_llm_signal,
    format_fundamentals,
    calculate_sentiment_score
)

# Confidence
from agent_framework import (
    ConfidenceCalculator,
    EnhancedConfidenceCalculator
)

# Configuration
from agent_framework import Config
```

---

### Class Hierarchy

```
Agent (ABC)
├── Your custom agents inherit from this
├── Implement: async def analyze(ticker, data) -> Signal
└── Optional: self.llm, self.rag for AI features

Signal (Pydantic)
├── Immutable result object
├── direction: 'bullish' | 'bearish' | 'neutral'
├── confidence: float (0.0 to 1.0)
└── reasoning: str (explanation)

Database
├── PostgreSQL client with connection pooling
├── async operations (asyncpg)
└── Methods: get_fundamentals, get_prices, get_news, etc.

LLMClient
├── Unified interface for OpenAI, Anthropic, Ollama
├── Automatic retries with backoff
└── System prompt support

RAGSystem
├── Document chunking and retrieval
├── Semantic search with embeddings
└── Context extraction for LLMs
```

---

## Learning Path (Code-Based)

### Step 1: Run Examples (30 minutes)

```bash
# Rule-based (no AI needed)
python examples/01_basic.py

# LLM-powered (requires Ollama or API key)
ollama pull llama3.2
python examples/02_llm_agent.py

# Hybrid (rules + AI)
python examples/03_hybrid.py

# RAG document analysis
python examples/04_rag_agent.py

# Famous strategies
python examples/05_buffett_quality.py
python examples/06_lynch_garp.py
python examples/07_graham_value.py
```

**Read the code!** Each example is fully commented and educational.

---

### Step 2: Modify Examples (1 hour)

```bash
# Copy an example
cp examples/01_basic.py my_custom_agent.py

# Modify the rules
# Change PE threshold from 15 to 12
# Add ROE requirement

# Run your modified version
python my_custom_agent.py
```

---

### Step 3: Build Custom Agent (1-2 hours)

**Create new agent from scratch:**

```python
from agent_framework import Agent, Signal

class MyCustomStrategy(Agent):
    """Your custom investment strategy."""
    
    async def analyze(self, ticker: str, data: dict) -> Signal:
        # Your unique logic here
        
        # Example: Combine multiple factors
        pe = data.get('pe_ratio', 0)
        roe = data.get('roe', 0)
        growth = data.get('revenue_growth', 0)
        
        # Custom scoring
        score = 0
        if pe < 20: score += 1
        if roe > 15: score += 1
        if growth > 10: score += 1
        
        # Custom rules
        if score >= 2:
            return Signal('bullish', 0.75, f'Score: {score}/3')
        elif score == 1:
            return Signal('neutral', 0.6, f'Score: {score}/3')
        else:
            return Signal('bearish', 0.5, f'Score: {score}/3')
```

---

### Step 4: Deploy as API (30 minutes)

```python
# api_server.py
from agent_framework import api_app, register_agent_instance
from my_custom_agent import MyCustomStrategy
import uvicorn

# Register agents
register_agent_instance("custom", MyCustomStrategy())
register_agent_instance("value", ValueAgent())

# Run server
if __name__ == "__main__":
    uvicorn.run(api_app, host="0.0.0.0", port=8000, reload=True)
```

**Test:**
```bash
curl http://localhost:8000/agents
# ["custom", "value"]

curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"agent_name":"custom","ticker":"AAPL"}'
```

---

## Common Patterns

### Pattern 1: Batch Analysis

```python
async def analyze_portfolio(tickers: list):
    """Analyze multiple stocks."""
    db = Database(Config.get_database_url())
    await db.connect()
    
    agent = ValueAgent()
    results = {}
    
    for ticker in tickers:
        data = await db.get_fundamentals(ticker)
        signal = await agent.analyze(ticker, data)
        results[ticker] = signal
    
    await db.disconnect()
    return results

# Run
portfolio = ['AAPL', 'MSFT', 'TSLA']
results = asyncio.run(analyze_portfolio(portfolio))

for ticker, signal in results.items():
    print(f"{ticker}: {signal.direction}")
```

---

### Pattern 2: Scheduled Analysis

```python
import schedule
import time

def analyze_daily():
    """Run analysis every day."""
    results = asyncio.run(analyze_portfolio(['AAPL', 'MSFT']))
    # Save results, send alerts, etc.

# Schedule for 9:30 AM daily
schedule.every().day.at("09:30").do(analyze_daily)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

### Pattern 3: Integration with pandas

```python
import pandas as pd
import asyncio

async def create_dataframe():
    """Get data as pandas DataFrame."""
    db = Database(Config.get_database_url())
    await db.connect()
    
    agent = ValueAgent()
    
    data_list = []
    for ticker in await db.list_tickers():
        fund = await db.get_fundamentals(ticker)
        signal = await agent.analyze(ticker, fund)
        
        data_list.append({
            'ticker': ticker,
            'pe_ratio': fund['pe_ratio'],
            'signal': signal.direction,
            'confidence': signal.confidence
        })
    
    await db.disconnect()
    
    df = pd.DataFrame(data_list)
    return df

# Use
df = asyncio.run(create_dataframe())
print(df)

# Filter bullish signals
bullish = df[df['signal'] == 'bullish']
print(f"\nBullish stocks: {list(bullish['ticker'])}")
```

---

### Pattern 4: Save Results to File

```python
import json
from datetime import datetime

async def save_analysis():
    """Save analysis results to JSON."""
    db = Database(Config.get_database_url())
    await db.connect()
    
    agent = ValueAgent()
    results = []
    
    for ticker in await db.list_tickers():
        data = await db.get_fundamentals(ticker)
        signal = await agent.analyze(ticker, data)
        
        results.append({
            'ticker': ticker,
            'timestamp': signal.timestamp.isoformat(),
            'direction': signal.direction,
            'confidence': signal.confidence,
            'reasoning': signal.reasoning
        })
    
    await db.disconnect()
    
    # Save to file
    filename = f"analysis_{datetime.now().strftime('%Y%m%d')}.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Saved to {filename}")

asyncio.run(save_analysis())
```

---

## Configuration

**All settings via .env file:**

```bash
# Database
DB_HOST=localhost
DB_PORT=5433
DB_USER=postgres
DB_PASSWORD=postgres

# LLM (if using AI)
OPENAI_API_KEY=sk-...
OLLAMA_BASE_URL=http://localhost:11434

# See .env.example for all options
```

**Access in code:**
```python
from agent_framework import Config

db_url = Config.get_database_url()
llm_model = Config.get_llm_model('openai')
```

**[Complete Configuration Guide →](CONFIGURATION.md)**

---

## Troubleshooting

### Import Errors

```bash
# Make sure framework is installed
pip install -e ".[all]"

# Activate virtual environment
source venv/bin/activate  # If using venv
```

### Database Connection

```bash
# Start database
docker compose up -d postgres

# Verify
docker ps | grep postgres
```

### LLM Errors

```bash
# For Ollama
ollama serve  # Must be running

# For OpenAI/Anthropic
# Add API key to .env
```

**[Complete Troubleshooting →](TROUBLESHOOTING.md)**

---

## Next Steps

**Explore:**
- 📖 [API Reference](API_REFERENCE.md) - Complete API documentation
- 📊 [Project Structure](PROJECT_STRUCTURE.md) - Code organization
- 🧪 [Testing Guide](../tests/README.md) - Writing tests

**Examples:**
- 📁 [examples/](../examples/) - All working code
- 📄 [Example README](../examples/README.md) - Code learning path


---

## Framework vs GUI

**Same functionality, different interface:**

| Task | GUI | Framework |
|------|-----|-----------|
| Create agent | Fill forms | Write Python class |
| Test agent | Click buttons | Run Python script |
| View code | Click "View" button | It IS the code |
| Save agent | Click "Save" | Save .py file |
| Run analysis | GUI testing tab | `python my_agent.py` |
| Modify agent | Edit in forms | Edit in your editor |
| Version control | Export files | Native git |
| Automation | Manual | Scriptable |

**Choose based on your workflow!**

**Try both:** GUI for quick prototyping, framework for production deployment.

---

## Resources

**Documentation:**
- [Getting Started](GETTING_STARTED.md) - Detailed installation
- [Configuration](CONFIGURATION.md) - Environment setup
- [Database Setup](DATABASE_SETUP.md) - PostgreSQL guide
- [LLM Customization](LLM_CUSTOMIZATION.md) - AI configuration

**Community:**
- [GitHub Issues](https://github.com/thesisai-hq/AI-Agent-Builder/issues) - Bug reports
- [GitHub Discussions](https://github.com/thesisai-hq/AI-Agent-Builder/discussions) - Questions

---

**No GUI needed - build powerful investment agents with pure Python!** 🚀
