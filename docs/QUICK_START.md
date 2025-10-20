
# Quick Start Guide

Get up and running with AI Agent Builder in **5 minutes**.

---

## 📋 Prerequisites

- **Python 3.8+** (check: `python --version`)
- **Docker** (for PostgreSQL)
- **Make**
- **Git**

---

## 🚀 Installation

### **Step 1: Get the Code**

```bash
# Clone repository
git clone <your-repo>
cd ai-agent-builder

# Or download and extract
```

### **Step 2: Install Core Dependencies**
- You can also use Conda instead if you are using Miniconda3.
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install core packages
pip install fastapi uvicorn pydantic psycopg2-binary python-dotenv requests

# Or install everything
pip install -r requirements.txt
```

### **Step 3: Setup Mock Database**

```bash
# Copy environment template
cp .env.example .env

# Start PostgreSQL in Docker
make start

# Load mock data
make seed

# Verify
make test
```

**Expected output:**
```
          status
--------------------------
 Database Setup Complete!
(1 row)

      table_name       | records
-----------------------+---------
 mock_analyst_ratings  |       8
 mock_fundamentals     |       5
 mock_insider_trades   |       8
 mock_macro_indicators |      10
 mock_news             |       7
 mock_options          |       8
 mock_prices           |      38
 mock_sec_filings      |       5
(8 rows)

✅ Data loaded
```
### **Step 4: View Mock Database with DBeaver**
Make sure PostgreSQL is running
```
make start
```
Verify it's running
```
make status
```
Should see:
```
# CONTAINER ID   IMAGE                  STATUS
# abc123def456   postgres:15-alpine     Up 2 minutes
```

Create Connection in DBeaver:

1. **Open DBeaver**

2. **Click "New Database Connection"** (or `Ctrl+N` / `Cmd+N`)

3. **Select PostgreSQL**
   - In the database list, find and click **PostgreSQL**
   - Click **Next**

4. **Enter Connection Details:**
```
   Host:     localhost
   Port:     5432
   Database: agentbuilder
   Username: agent_user
   Password: agent_password
```

5. **Test Connection**
   - Click **Test Connection**
   - First time: DBeaver will offer to download PostgreSQL driver
   - Click **Download** and wait
   - Should see: "Connected (PostgreSQL 15.x)"

6. **Click Finish**

View Tables in DBeaver:
```
Database Navigator (left sidebar)
└── agentbuilder
    └── Schemas
        └── public
            └── Tables
                ├── analyses
                ├── mock_analyst_ratings
                ├── mock_fundamentals
                ├── mock_insider_trades
                ├── mock_macro_indicators
                ├── mock_news
                ├── mock_options
                ├── mock_prices
                └── mock_sec_filings
```

### **Step 5: Install Package**

```bash
# Install in development mode
pip install -e .
```

### **Step 6: Run the API**

```bash
python main.py
```

**You should see:**
```
🚀 Starting AI Agent Builder API
   Server: 0.0.0.0:8000
   Docs: http://localhost:8000/docs
INFO:     Started server process [69251]
INFO:     Waiting for application startup.
INFO:agent_builder.api.app:🚀 Starting API...
INFO:agent_builder.core.database:✅ Database pool initialized (2-10 connections)
INFO:agent_builder.core.database:✅ Database tables ready

======================================================================
REGISTERING TEST AGENTS
======================================================================
INFO:agent_builder.agents.registry:✅ Registered: pe_ratio_agent
✅ Registered: PE Ratio Agent
INFO:agent_builder.agents.registry:✅ Registered: price_trend_agent
✅ Registered: Price Trend Agent
INFO:agent_builder.agents.registry:✅ Registered: news_sentiment_agent
✅ Registered: News Sentiment Agent

📊 Total agents registered: 3
📊 Enabled agents: 3
📊 Agent IDs: pe_ratio_agent, price_trend_agent, news_sentiment_agent
======================================================================

INFO:agent_builder.api.app:✅ 3 agents registered (3 enabled)
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## 🧪 Test the API

### **Option 1: Web Browser**

Visit: **http://localhost:8000/docs**

1. Click **POST /analyze**
2. Click **"Try it out"**
3. Enter:
   ```json
   {
     "ticker": "AAPL"
   }
   ```
4. Click **"Execute"**
5. Copy the `analysis_id` from **Response body**.
6. Use **GET /analyze/{analysis_id}** to get results. Agin, Click **"Try it out""**, type the copyed `analysis_id`, and click **"Execute"**.

### **Option 2: Command Line**

```bash
# Health check
curl http://localhost:8000/health

# List agents
curl http://localhost:8000/agents

# Run analysis
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL"}'

# Response: {"analysis_id":"abc-123","status":"pending"}

# Get results (replace with your analysis_id)
curl http://localhost:8000/analyze/abc-123
```

### **Expected Result:**
```json
{
  "ticker": "AAPL",
  "status": "completed",
  "signals": [
    {
      "agent_name": "PE Ratio Agent",
      "signal_type": "bullish",
      "confidence": 0.8,
      "reasoning": "Low P/E ratio of 28.5 suggests good value"
    },
    {
      "agent_name": "Price Trend Agent",
      "signal_type": "bullish",
      "confidence": 0.7,
      "reasoning": "Price $189.50 is 3.2% above SMA20"
    },
    {
      "agent_name": "News Sentiment Agent",
      "signal_type": "bullish",
      "confidence": 0.75,
      "reasoning": "Positive news sentiment: 0.66 from 3 articles"
    }
  ],
  "consensus": {
    "signal": "bullish",
    "confidence": 0.75,
    "agreement": 1.0
  }
}
```

---

## 🎓 Next Steps

### **1. Add LLM Support (Optional)**

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama
ollama serve

# Pull model
ollama pull llama3.2
ollama pull nomic-embed-text

# Test LLM agents
python examples/llm_agent_example.py
```

### **2. Add RAG Support (Optional)**

```bash
# Install RAG dependencies
pip install sentence-transformers chromadb

# Test RAG agents
python examples/rag_agents.py
```

### **3. Create Your First Custom Agent**

Create `examples/my_agents.py`:
```python
from agent_builder import agent, get_registry

@agent("My First Agent", "Custom analysis logic")
def my_agent(ticker, context):
    # Get data
    pe = context.get_fundamental("pe_ratio", 20)
    growth = context.get_fundamental("revenue_growth", 0)
    
    # Your logic
    score = 0
    if pe < 20:
        score += 1
    if growth > 10:
        score += 1
    
    # Return signal
    if score >= 2:
        return "bullish", 0.8, f"Strong metrics: PE={pe}, growth={growth}%"
    elif score == 0:
        return "bearish", 0.6, "Weak metrics"
    
    return "neutral", 0.5, "Mixed signals"

# Register
def register_my_agents():
    registry = get_registry()
    registry.register(my_agent.agent, weight=1.0, tags=["custom"])
```

Add to `examples/register_agents.py`:
```python
from examples.my_agents import register_my_agents

def register_all_agents():
    # ... existing agents ...
    register_my_agents()
```

Restart API and test!
You should see My First Agent is added to the result:
```
    {
      "ticker": "AAPL",
      "reasoning": "Weak metrics",
      "timestamp": "2025-10-17T15:04:51.200605",
      "agent_name": "My First Agent",
      "confidence": 0.6,
      "signal_type": "bearish"
    }
```


---

## 🎯 Common Use Cases

### **Use Case 1: Simple Stock Screening**
```python
# Create screening agent
@agent("Value Screener")
def value_screener(ticker, context):
    pe = context.get_fundamental("pe_ratio")
    debt = context.get_fundamental("debt_to_equity")
    
    if pe < 15 and debt < 1.0:
        return "bullish", 0.9, "Undervalued with low debt"
    
    return "neutral", 0.4
```

### **Use Case 2: AI-Powered Analysis**
```python
# LLM analyzes fundamentals
@agent("AI Analyst")
def ai_analyst(ticker, context):
    llm = get_llm_provider("ollama")
    fundamentals = context.get_fundamentals()
    
    prompt = f"Analyze {ticker}: {fundamentals}"
    response = llm.generate(prompt)
    
    return parse_response(response)
```

### **Use Case 3: SEC Filing Deep Dive**
```python
# RAG searches through SEC filings
@agent("SEC Deep Dive")
def sec_agent(ticker, context):
    rag = RAGEngine(context.db, embedding="ST", vectorstore="chroma")
    rag.index_sec_filings(ticker)
    
    relevant = rag.search_sec_filings("risk factors and outlook")
    
    # Analyze with LLM
    llm = get_llm_provider("ollama")
    response = llm.generate(f"Analyze risks: {relevant}")
    
    return parse_response(response)
```

---

## 📊 Available Test Tickers

The mock database includes data for:

- **AAPL** - Apple Inc. (Technology)
- **TSLA** - Tesla Inc. (Automotive/EVs)
- **MSFT** - Microsoft Corp. (Software)
- **GOOGL** - Alphabet Inc. (Internet)
- **NVDA** - NVIDIA Corp. (Semiconductors)

Each has:
- ✅ Complete fundamental metrics
- ✅ 10 days of price history
- ✅ Recent news articles
- ✅ Analyst ratings
- ✅ Insider trades
- ✅ SEC filings with full text
- ✅ Options data
- ✅ Macro indicators

---

## 🎨 Customization

### **Change LLM Provider**

In `.env`:
```bash
# Use Ollama (local)
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2

# Use OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4

# Use Claude
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

### **Change RAG Configuration**

In your agent:
```python
# Fast but simple
rag = RAGEngine(db, embedding="simple", vectorstore="memory")

# Best quality
rag = RAGEngine(db, embedding="sentence-transformers", vectorstore="chroma")

# Fastest search
rag = RAGEngine(db, embedding="sentence-transformers", vectorstore="faiss")
```

---

## 🐛 Common Issues

### **"Module not found: agent_builder"**
```bash
pip install -e .
# or
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### **"Database connection failed"**
```bash
# Check database is running
make status

# Restart
make restart

# Check .env has correct DATABASE_URL
cat .env | grep DATABASE_URL
```

### **"Ollama connection refused"**
```bash
# Start Ollama
ollama serve

# In another terminal
ollama pull llama3.2
ollama pull nomic-embed-text
```

### **"No data returned from database"**
```bash
# Reload mock data
make seed

# Verify
make shell
SELECT COUNT(*) FROM mock_fundamentals;
\q
```

---

## 🎉 Success!

If you see:
- ✅ API running on http://localhost:8000
- ✅ 3+ agents registered
- ✅ Analysis completes successfully
- ✅ Database queries return data

**You're ready to build!** 🚀

---

## 📚 Learn More

- [README.md](README.md) - Full documentation
- [RAG_USAGE.md](RAG_USAGE.md) - RAG configuration guide
- [DOCKER_README.md](DOCKER_README.md) - Docker setup
- API Docs: http://localhost:8000/docs

---

## 💡 Tips

1. **Start simple** - Test with 3 basic agents first
2. **Add LLM** - When comfortable, add Ollama
3. **Add RAG** - When ready, enable semantic search
4. **Scale up** - Add more agents as needed

The system is designed for **progressive enhancement**!

---

## 🎯 What's Next?

- [ ] Test the 3 basic agents
- [ ] Try analyzing different tickers
- [ ] Add Ollama for LLM analysis
- [ ] Install RAG for semantic search
- [ ] Create your first custom agent
- [ ] Deploy to production

**Happy building! 🚀**