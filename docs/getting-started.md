# Getting Started

Welcome to the AI Investment Advisor framework! This guide will walk you through installation, setup, and your first analysis.

---

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.8 or higher** (3.11 recommended)
- **Docker Desktop** or Docker Engine + Docker Compose
- **Git** (for cloning the repository)
- **4GB RAM minimum** (8GB recommended)
- **10GB disk space** (for Docker images and data)

### Check Your Environment

```bash
# Check Python version
python --version
# Should show: Python 3.8.0 or higher

# Check Docker
docker --version
docker-compose --version

# Check available RAM
docker info | grep "Total Memory"
```

---

## ⚡ Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd ai-investment-advisor
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 pydantic-2.5.0 ...
```

### Step 4: Verify Installation

```bash
python verify_installation.py
```

**Expected output:**
```
✅ INSTALLATION VERIFIED
🎉 Everything looks good!
```

---

## 🗄️ Database Setup

### Step 1: Start PostgreSQL

```bash
# Start database with Docker
docker-compose -f docker-compose.test.yml up -d

# Wait 10 seconds for startup
sleep 10

# Verify it's running
docker-compose -f docker-compose.test.yml ps
```

**Expected output:**
```
NAME              IMAGE                STATUS
agent-test-db     postgres:15-alpine   Up 10 seconds
```

### Step 2: Configure Environment

Create `.env` file:

```bash
# Copy example configuration
cp .env.example .env

# Or create manually
cat > .env << 'EOF'
DATABASE_URL=postgresql://agent_user:agent_password@localhost:5432/agent_test
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
SENTIMENT_ANALYZER=vader
EOF
```

### Step 3: Setup Test Database

```bash
python setup_test_database.py
```

**Expected output:**
```
🔨 CREATING DATABASE SCHEMA
✅ Schema created (13 tables)

📊 GENERATING TEST DATA
✅ Generated: 8 companies, 5,000+ records

🎉 SUCCESS! Test database is ready!
```

**What this creates:**
- 13 database tables
- 8 test stocks (AAPL, MSFT, GOOGL, TSLA, AMZN, JPM, XOM, WMT)
- 90 days of price history
- Technical indicators, risk metrics, news, analyst ratings
- ~5,000 total records

---

## 🚀 Start the API Server

### Basic Start

```bash
python -m agent_builder.api.main
```

**Expected output:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
✅ Database connected with connection pool
✅ Agents registered
✅ Registry ready: 61 agents, 61 enabled
```

### With Custom Port

```bash
API_PORT=9000 python -m agent_builder.api.main
```

### View Server Logs

The server will log all activity:
- Database connections
- Agent registrations
- API requests
- Analysis executions
- Errors and warnings

---

## 🧪 Your First Analysis

### Method 1: Using curl

```bash
# Request analysis
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'
```

**Response:**
```json
{
  "analysis_id": "abc-123-def-456",
  "status": "pending"
}
```

**Get results** (wait 2-3 seconds):
```bash
curl http://localhost:8000/analyze/abc-123-def-456
```

**Response:**
```json
{
  "id": "abc-123-def-456",
  "ticker": "AAPL",
  "status": "completed",
  "consensus": {
    "signal": "bullish",
    "confidence": 0.75,
    "agreement": 0.82
  },
  "signals": [
    {
      "agent_name": "Value Investor",
      "signal_type": "bullish",
      "confidence": 0.85,
      "reasoning": "Value Investor analysis"
    }
  ]
}
```

### Method 2: Using API Docs (Interactive)

1. Open browser: **http://localhost:8000/docs**
2. Find `POST /analyze` endpoint
3. Click "Try it out"
4. Enter: `{"ticker": "AAPL"}`
5. Click "Execute"
6. Copy the `analysis_id` from response
7. Use `GET /analyze/{analysis_id}` to get results

### Method 3: Using Python

```python
import requests
import time

# Request analysis
response = requests.post(
    'http://localhost:8000/analyze',
    json={'ticker': 'AAPL'}
)

analysis_id = response.json()['analysis_id']
print(f"Analysis ID: {analysis_id}")

# Wait for completion
time.sleep(3)

# Get results
results = requests.get(
    f'http://localhost:8000/analyze/{analysis_id}'
).json()

print(f"Consensus: {results['consensus']['signal']}")
print(f"Confidence: {results['consensus']['confidence']}")
print(f"Agreement: {results['consensus']['agreement']}")
```

---

## 🎯 Understanding the Results

### Consensus Object

```json
"consensus": {
  "signal": "bullish",        // Overall recommendation
  "confidence": 0.75,         // Average confidence (0-1)
  "agreement": 0.82,          // Agent agreement (0-1)
  "distribution": {
    "bullish": 45,            // Number of bullish agents
    "bearish": 10,            // Number of bearish agents
    "neutral": 6              // Number of neutral agents
  }
}
```

### Interpreting Signals

- **Signal**: "bullish", "bearish", or "neutral"
- **Confidence**: 
  - 0.9+ = Very high confidence
  - 0.75-0.9 = High confidence
  - 0.6-0.75 = Moderate confidence
  - 0.5-0.6 = Low confidence
  - < 0.5 = Very uncertain

- **Agreement**:
  - 0.9+ = Strong consensus (>90% agree)
  - 0.75-0.9 = Good consensus
  - 0.6-0.75 = Moderate consensus
  - < 0.6 = Divided opinion

### Example Interpretations

**Strong Buy:**
```json
{
  "signal": "bullish",
  "confidence": 0.85,
  "agreement": 0.92
}
```
→ 92% of agents agree, very confident

**Weak Buy:**
```json
{
  "signal": "bullish",
  "confidence": 0.62,
  "agreement": 0.68
}
```
→ Only 68% agree, lower confidence

**Divided Opinion:**
```json
{
  "signal": "neutral",
  "confidence": 0.55,
  "agreement": 0.45
}
```
→ Agents disagree, no clear signal

---

## 🔍 Exploring the System

### List All Agents

```bash
curl http://localhost:8000/agents | jq
```

This shows all 61 registered agents with their metadata.

### Check Specific Stock Data

```bash
# Connect to database
docker exec -it agent-test-db psql -U agent_user -d agent_test

# Inside psql:
\dt                                    # List tables
SELECT * FROM mock_fundamentals WHERE ticker = 'AAPL';
SELECT * FROM mock_latest_prices;
\q                                     # Exit
```

### Test Different Stocks

```bash
# Microsoft
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "MSFT"}'

# Tesla
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "TSLA"}'

# Amazon
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AMZN"}'
```

**Available tickers:** AAPL, MSFT, GOOGL, TSLA, AMZN, JPM, XOM, WMT

---

## 🎓 Next Steps

### 1. Understand the Agents

Read about each agent type:
- [Fundamental Agents](../examples/fundamental_agents.py) - Value, growth, quality
- [Technical Agents](../examples/technical_agents.py) - Charts, indicators
- [Macro Agents](../examples/macro_agents.py) - Economy, rates, sentiment
- [Sentiment Agents](../examples/sentiment_agents.py) - News, analysts, insiders
- [Risk Agents](../examples/risk_agents.py) - Volatility, downside protection

### 2. Create Your First Agent

See [Creating Agents Guide](creating-agents.md) for step-by-step tutorial.

### 3. Explore the Data

```bash
# Check what data is available
curl http://localhost:8000/health

# Connect to database
docker exec -it agent-test-db psql -U agent_user -d agent_test

# Sample queries
SELECT ticker, pe_ratio, roe, profit_margin 
FROM mock_fundamentals 
ORDER BY market_cap DESC;

SELECT ticker, sentiment, COUNT(*) 
FROM mock_news 
GROUP BY ticker, sentiment;
```

### 4. Customize Agent Weights

Enable/disable agents or change their influence:

```bash
# Disable an agent
curl -X POST http://localhost:8000/agents/value_investor/disable

# Enable it again
curl -X POST http://localhost:8000/agents/value_investor/enable

# Run analysis with specific agents only
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "agent_ids": ["value_investor", "rsi_momentum"]
  }'
```

---

## 🐛 Troubleshooting

### API Won't Start

**Error:** `Address already in use`
```bash
# Port 8000 is busy, use different port
API_PORT=9000 python -m agent_builder.api.main
```

**Error:** `Cannot connect to database`
```bash
# Check database is running
docker-compose -f docker-compose.test.yml ps

# Check logs
docker-compose -f docker-compose.test.yml logs postgres
```

### No Agents Registered

**Check API startup logs:**
```
⚠️  No agents to register
```

**Solution:** Agents need to be registered. This happens automatically if you have `examples/register_agents.py` and it's imported in `api/main.py`.

### Analysis Returns Empty Signals

**Cause:** No agents enabled or agents failing

**Check:**
```bash
# List agents
curl http://localhost:8000/agents

# Check API logs for errors
# Look for agent execution errors
```

### Database Connection Issues

```bash
# Test database connection
docker exec -it agent-test-db pg_isready -U agent_user

# Try connecting manually
psql postgresql://agent_user:agent_password@localhost:5432/agent_test

# Reset database
docker-compose -f docker-compose.test.yml down -v
docker-compose -f docker-compose.test.yml up -d
sleep 10
python setup_test_database.py
```

---

## 💡 Tips

### Development Workflow

```bash
# 1. Start database once
docker-compose -f docker-compose.test.yml up -d

# 2. Edit code (agents, config, etc.)

# 3. Restart API to reload changes
# Press Ctrl+C, then:
python -m agent_builder.api.main

# 4. Test changes
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'
```

### Hot Reload (Development)

```bash
# Use --reload for automatic reloading
uvicorn agent_builder.api.main:app --reload --host 0.0.0.0 --port 8000
```

Now when you edit agent files, the server automatically restarts!

### Quick Database Reset

```bash
# Reset and regenerate all data
docker-compose -f docker-compose.test.yml restart postgres
sleep 5
python setup_test_database.py
```

### View All Available Data

```bash
# List all tables
docker exec -it agent-test-db psql -U agent_user -d agent_test -c "\dt"

# Count records in each table
docker exec -it agent-test-db psql -U agent_user -d agent_test -c "
SELECT 
  (SELECT COUNT(*) FROM mock_fundamentals) as fundamentals,
  (SELECT COUNT(*) FROM mock_prices) as prices,
  (SELECT COUNT(*) FROM mock_news) as news,
  (SELECT COUNT(*) FROM mock_technical_indicators) as technicals;
"
```

---

## 🎯 What's Next?

You've successfully:
- ✅ Installed the framework
- ✅ Set up the database with test data
- ✅ Started the API server
- ✅ Run your first analysis

### Continue Learning

1. **[Architecture Guide](architecture.md)** - Understand how the system works
2. **[Creating Agents Guide](creating-agents.md)** - Build your own agents
3. **[API Reference](api-reference.md)** - Complete API documentation
4. **[Example Agents](../examples/)** - Study 61 professional agents

### Build Something

- Create a custom agent for your strategy
- Build an agent portfolio for a specific goal
- Integrate with a frontend dashboard
- Deploy to production with real data

---

## 📚 Quick Reference

### Common Commands

```bash
# Database
docker-compose -f docker-compose.test.yml up -d      # Start
docker-compose -f docker-compose.test.yml down       # Stop
docker-compose -f docker-compose.test.yml down -v    # Reset
docker-compose -f docker-compose.test.yml logs -f    # View logs

# API
python -m agent_builder.api.main                     # Start
curl http://localhost:8000/health                    # Health check
curl http://localhost:8000/agents                    # List agents

# Setup
python setup_test_database.py                        # Setup database
python verify_installation.py                        # Verify install

# Development
uvicorn agent_builder.api.main:app --reload          # Hot reload
```

### File Locations

```
agent_builder/          # Core framework
examples/               # Example agents
sql/                    # Database schema
docs/                   # Documentation (you are here)
```

### Environment Variables

```bash
DATABASE_URL            # PostgreSQL connection string
API_HOST                # API bind address (0.0.0.0)
API_PORT                # API port (8000)
DEBUG                   # Enable debug mode (true/false)
LLM_PROVIDER            # ollama or groq
SENTIMENT_ANALYZER      # vader or finbert
```

---

## 🆘 Getting Help

### Documentation

- **This Guide** - Getting started
- **[Architecture](architecture.md)** - System design
- **[Creating Agents](creating-agents.md)** - Build agents
- **[API Reference](api-reference.md)** - API docs

### Troubleshooting

- Run `python verify_installation.py` for diagnostics
- Check `docker-compose logs` for database issues
- Check API console output for agent errors
- See [QUICKSTART.md](../QUICKSTART.md) troubleshooting section

### Community

- GitHub Issues - Bug reports
- GitHub Discussions - Questions and ideas
- Documentation - Comprehensive guides

---

**Ready to build your first agent?** → [Creating Agents Guide](creating-agents.md)

**Want to understand the architecture?** → [Architecture Guide](architecture.md)

**Need API details?** → [API Reference](api-reference.md)