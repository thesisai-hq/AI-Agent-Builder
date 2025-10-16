# AI Investment Advisor - Agent Framework

A comprehensive, production-ready framework for building AI-powered investment analysis agents. Create sophisticated multi-agent systems that analyze stocks from multiple perspectives: fundamental, technical, macro, sentiment, and risk analysis.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Overview

This framework enables you to:
- **Build custom AI agents** using a simple decorator pattern
- **Combine multiple analysis strategies** (value investing, technical analysis, sentiment, etc.)
- **Generate consensus signals** from agent votes
- **Scale from testing to production** with PostgreSQL backend
- **Integrate LLMs** (Ollama, Groq) for intelligent analysis
- **Test with realistic data** using comprehensive mock database

**Perfect for:** Quantitative analysts, algorithmic traders, portfolio managers, fintech developers, and anyone building systematic investment strategies.

---

## ⚡ Quick Start (3 Minutes)

### 1. Clone & Install

```bash
git clone <repository-url>
cd ai-investment-advisor
pip install -r requirements.txt
```

### 2. Start Database

```bash
docker-compose -f docker-compose.test.yml up -d
```

### 3. Setup Test Data

```bash
python setup_test_database.py
```

Expected output:
```
✅ Schema created (13 tables)
✅ Generated 8 companies, 5,000+ records
✅ Ready for all agent types!
```

### 4. Start API

```bash
python -m agent_builder.api.main
```

### 5. Test Analysis

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'
```
### 6. Check Analysis REsult
- Swap {"analysis_id"} with your analysis_id given from previous command.
```bash
curl http://localhost:8000/analyze/{"analysis_id"}
```

**🎉 Done!** API docs at http://localhost:8000/docs

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI REST API                         │
│                  (Async, Background Tasks)                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────┐
│                   Agent Registry                             │
│              (Manages 61+ Agents)                            │
└──────────┬──────────┬──────────┬──────────┬─────────────────┘
           │          │          │          │
    ┌──────▼───┐ ┌───▼────┐ ┌──▼─────┐ ┌──▼──────┐
    │Fundamental│ │Technical│ │ Macro  │ │Sentiment│
    │  Agents   │ │ Agents  │ │ Agents │ │ Agents  │
    │  (12)     │ │  (13)   │ │  (13)  │ │  (11)   │
    └──────┬────┘ └───┬─────┘ └──┬─────┘ └──┬──────┘
           │          │          │          │
           └──────────┴──────────┴──────────┘
                       │
           ┌───────────▼────────────┐
           │   Agent Context        │
           │  (Data Access Layer)   │
           └───────────┬────────────┘
                       │
           ┌───────────▼────────────┐
           │  Connection Pool       │
           │   (2-10 connections)   │
           └───────────┬────────────┘
                       │
           ┌───────────▼────────────┐
           │  PostgreSQL Database   │
           │    (13 Tables)         │
           │  - Fundamentals        │
           │  - Prices              │
           │  - Technical Indicators│
           │  - News & Sentiment    │
           │  - Risk Metrics        │
           │  - Macro Data          │
           └────────────────────────┘
```

---

## 🤖 Agent Types (61 Total)

### 1. Fundamental Agents (12)

Analyze company financials and business quality:

- **Value Investing**: Warren Buffett style (P/E, ROE, debt)
- **Growth Investing**: High-growth stocks (PEG, revenue growth)
- **Quality Screening**: Business moats (margins, ROIC)
- **Cash Flow Analysis**: Free cash flow quality
- **Earnings Analysis**: Beats, misses, guidance
- **Balance Sheet**: Financial health, debt sustainability

**Example:**
```python
@simple_agent("Value Investor", weight=0.15)
def value_agent(ticker, context):
    pe = context.get_metric('pe_ratio')
    roe = context.get_metric('roe')
    
    if pe < 20 and roe > 15:
        return "bullish", 0.85
    return "neutral", 0.5
```

### 2. Technical Agents (13)

Price patterns and chart analysis:

- **Moving Averages**: Golden/Death Cross
- **Momentum**: RSI, MACD, ADX
- **Volatility**: Bollinger Bands, ATR
- **Volume**: OBV, volume confirmation
- **Price Action**: Support/resistance, trends
- **Multi-Timeframe**: Confluence analysis

### 3. Macro Agents (13)

Economic conditions and cycles:

- **Economic Cycle**: GDP, unemployment, inflation
- **Interest Rates**: Fed policy, yield curve
- **Market Sentiment**: VIX, S&P 500 momentum
- **Commodities**: Oil, gold prices
- **Currency**: Dollar strength (DXY)
- **Recession Indicators**: Leading indicators

### 4. Sentiment Agents (11)

Market psychology and opinions:

- **News Sentiment**: Aggregate media sentiment
- **Analyst Ratings**: Buy/hold/sell consensus
- **Insider Trading**: Follow the smart money
- **Price Targets**: Upside potential
- **Sentiment Divergence**: Cross-source validation

### 5. Risk Agents (12)

Risk management and capital preservation:

- **Volatility**: Current levels and regime shifts
- **Downside Protection**: Max drawdown, VaR
- **Risk-Adjusted Returns**: Sharpe, Sortino ratios
- **Correlation**: Portfolio diversification
- **Tail Risk**: Extreme event monitoring
- **Options Signals**: Put/call ratio, IV premium

---

## 📊 Mock Database

Comprehensive test data for **8 major stocks**:
- **AAPL** (Apple) - Technology
- **MSFT** (Microsoft) - Technology
- **GOOGL** (Alphabet) - Technology
- **TSLA** (Tesla) - Automotive
- **AMZN** (Amazon) - E-commerce
- **JPM** (JPMorgan) - Banking
- **XOM** (Exxon) - Energy
- **WMT** (Walmart) - Retail

### Data Included (5,000+ records):

| Table | Records | Description |
|-------|---------|-------------|
| **Fundamentals** | 8 | P/E, ROE, margins, debt ratios (30+ metrics) |
| **Prices** | 1,440+ | 90 days OHLCV data |
| **Technical Indicators** | 1,200+ | RSI, MACD, Bollinger Bands, etc. |
| **Risk Metrics** | 1,200+ | Volatility, VaR, Sharpe ratio |
| **Balance Sheet** | 32 | Quarterly financial statements |
| **Cash Flow** | 32 | Operating, investing, financing flows |
| **Earnings** | 32 | EPS beats/misses, guidance |
| **SEC Filings** | 32 | 10-K, 10-Q, 8-K documents |
| **News** | 160+ | Headlines with sentiment analysis |
| **Analyst Ratings** | 80+ | Buy/hold/sell recommendations |
| **Insider Trades** | 100+ | Executive transactions |
| **Options Data** | 100+ | Put/call ratios, implied volatility |
| **Macro Indicators** | 13 | Fed rates, GDP, VIX, oil, gold |

**Total: ~5,000 realistic test records!**

---

## 🚀 Usage Examples

### Create a Custom Agent

```python
from agent_builder.agents import simple_agent

@simple_agent("PE Ratio Agent", weight=0.15)
def pe_ratio_agent(ticker, context):
    """Buy low P/E stocks"""
    pe = context.get_metric('pe_ratio')
    
    if pe < 15:
        return "bullish", 0.8
    elif pe > 30:
        return "bearish", 0.7
    return "neutral", 0.5
```

### Register Agent

```python
from agent_builder.agents.registry import get_registry

registry = get_registry()
registry.register(pe_ratio_agent.agent, tags=['fundamental', 'value'])
```

### Run Analysis via API

```bash
# Start analysis
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'

# Response:
{
  "analysis_id": "abc-123",
  "status": "pending"
}

# Get results
curl http://localhost:8000/analyze/abc-123

# Response:
{
  "id": "abc-123",
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
      "reasoning": "Low P/E with high ROE"
    },
    // ... more agents
  ]
}
```

### Access Data in Agents

```python
@simple_agent("Comprehensive Analyzer", weight=0.20)
def comprehensive_agent(ticker, context):
    # Fundamentals
    fundamentals = context.get_fundamentals()
    pe = context.get_metric('pe_ratio')
    
    # Technical
    technicals = context.get_latest_technicals()
    rsi = technicals.get('rsi_14', 50)
    
    # Sentiment
    news = context.get_news(limit=20)
    ratings = context.get_analyst_ratings()
    
    # Risk
    risk = context.get_latest_risk_metrics()
    sharpe = risk.get('sharpe_ratio', 0)
    
    # Macro
    macro = context.get_macro_indicators()
    gdp = macro.get('gdp_growth', 0)
    
    # Combine all factors
    score = calculate_comprehensive_score(...)
    
    return "bullish" if score > 0.6 else "bearish", confidence
```

---

## 🎓 Example Agent Portfolios

### Conservative Portfolio
```python
# Focus on quality, risk management, dividends
- Value Investor (0.15)
- Quality Screener (0.15)
- Downside Protection (0.15)
- Balance Sheet Strength (0.12)
- Dividend Analysis (0.10)
- Risk-Adjusted Returns (0.12)
```

### Growth Portfolio
```python
# Focus on momentum, earnings growth
- Growth Investor (0.20)
- Earnings Surprise (0.15)
- Technical Momentum (0.15)
- Revenue Growth (0.12)
- Analyst Upgrades (0.10)
```

### Contrarian Portfolio
```python
# Buy fear, sell greed
- VIX Fear Gauge (0.15)
- RSI Oversold (0.15)
- Insider Buying (0.15)
- Deep Value (0.12)
- Sentiment Divergence (0.10)
```

---

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Database
DATABASE_URL=postgresql://agent_user:agent_password@localhost:5432/agent_test

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# LLM Provider (optional)
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Or use Groq
# LLM_PROVIDER=groq
# GROQ_API_KEY=your_api_key_here
# GROQ_MODEL=llama3-8b-8192

# Sentiment Analysis
SENTIMENT_ANALYZER=vader  # or finbert
```

### Agent Weights

Customize agent importance:

```python
registry.register(
    agent=value_investor_agent.agent,
    agent_id="value_investor",
    weight=0.20,  # Higher weight = more influence
    enabled=True,
    tags=['fundamental', 'value']
)
```

---

## 📁 Project Structure

```
ai-investment-advisor/
├── sql/
│   └── schema.sql                    # Database schema (13 tables)
│
├── agent_builder/
│   ├── agents/
│   │   ├── base_agent.py            # BaseAgent, AgentSignal
│   │   ├── builder.py               # @simple_agent decorator
│   │   ├── context.py               # AgentContext (data access)
│   │   ├── registry.py              # AgentRegistry
│   │   └── personas.py              # LLM agent personas
│   │
│   ├── api/
│   │   └── main.py                  # FastAPI application
│   │
│   ├── data/
│   │   ├── generator.py             # Mock data generator
│   │   └── setup.py                 # Database setup utilities
│   │
│   ├── llm/
│   │   ├── ollama.py                # Ollama provider
│   │   ├── groq.py                  # Groq provider
│   │   └── factory.py               # LLM factory
│   │
│   ├── repositories/
│   │   ├── connection.py            # Connection pooling
│   │   └── repository.py            # Data repository
│   │
│   ├── sentiment/
│   │   ├── vader.py                 # VADER analyzer (fast)
│   │   ├── finbert.py               # FinBERT analyzer (accurate)
│   │   └── factory.py               # Sentiment factory
│   │
│   ├── config.py                    # Configuration
│   ├── security.py                  # SQL injection prevention
│   └── utils.py                     # Utilities
│
├── examples/
│   ├── fundamental_agents.py        # 12 fundamental agents
│   ├── technical_agents.py          # 13 technical agents
│   ├── macro_agents.py              # 13 macro agents
│   ├── sentiment_agents.py          # 11 sentiment agents
│   ├── risk_agents.py               # 12 risk agents
│   └── register_agents.py           # Agent registration
│
├── docker-compose.test.yml          # PostgreSQL + services
├── setup_test_database.py           # Database setup script
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment template
├── README.md                        # This file
└── QUICKSTART.md                    # Quick start guide
```

---

## 🔌 API Reference

### Core Endpoints

#### Health Check
```bash
GET /health
```

#### List Agents
```bash
GET /agents
GET /agents?enabled=true
```

#### Get Agent Details
```bash
GET /agents/{agent_id}
```

#### Enable/Disable Agent
```bash
POST /agents/{agent_id}/enable
POST /agents/{agent_id}/disable
```

#### Run Analysis
```bash
POST /analyze
Content-Type: application/json

{
  "ticker": "AAPL",
  "agent_ids": ["value_investor", "rsi_momentum"]  # optional
}

Response:
{
  "analysis_id": "uuid",
  "status": "pending"
}
```

#### Get Analysis Results
```bash
GET /analyze/{analysis_id}

Response:
{
  "id": "uuid",
  "ticker": "AAPL",
  "status": "completed",
  "signals": [...],
  "consensus": {
    "signal": "bullish",
    "confidence": 0.75,
    "agreement": 0.82,
    "distribution": {
      "bullish": 45,
      "bearish": 10,
      "neutral": 6
    }
  }
}
```

**Interactive API Docs:** http://localhost:8000/docs

---

## 🎯 Key Features

### ✅ Security
- SQL injection prevention (whitelist + parameterization)
- Input validation (Pydantic models)
- Ticker sanitization
- Table name validation

### ✅ Performance
- Connection pooling (2-10 connections)
- Query result caching
- Background task processing
- Optimized database indexes
- ~50x faster than creating connections

### ✅ Scalability
- Async FastAPI
- Stateless design
- Easy horizontal scaling
- Supports distributed architectures

### ✅ Developer Experience
- Simple decorator pattern
- Clear agent structure
- Comprehensive examples
- Auto-generated API docs
- Hot-reload in development

### ✅ Production Ready
- Error handling
- Logging
- Health checks
- CORS support
- Environment-based config

---

## 🧪 Testing

### Run Test Analysis

```bash
# Start API
python -m agent_builder.api.main

# Test single stock
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'

# Test with specific agents
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "MSFT",
    "agent_ids": ["value_investor", "growth_investor"]
  }'
```

### Test Individual Agent

```python
from agent_builder.agents.context import AgentContext
from examples.fundamental_agents import value_investor_agent

context = AgentContext("AAPL")
signal, confidence = value_investor_agent("AAPL", context)

print(f"Signal: {signal}, Confidence: {confidence}")
# Output: Signal: bullish, Confidence: 0.75
```

### Database Queries

```bash
# Connect to database
docker exec -it agent-test-db psql -U agent_user -d agent_test

# Sample queries
SELECT * FROM mock_fundamentals WHERE ticker = 'AAPL';
SELECT * FROM mock_latest_prices ORDER BY ticker;
SELECT * FROM mock_analyst_consensus;
```

---

## 🚢 Production Deployment

### 1. Database Migration

Replace mock data with real data sources:

```python
# Instead of mock_generator
from your_data_pipeline import RealDataFetcher

fetcher = RealDataFetcher(
    alpha_vantage_key=os.getenv('ALPHA_VANTAGE_KEY'),
    finnhub_key=os.getenv('FINNHUB_KEY')
)

fetcher.fetch_and_store('AAPL')
```

### 2. Environment Setup

```bash
# Production .env
DATABASE_URL=postgresql://user:pass@prod-db:5432/prod
DEBUG=false
API_HOST=0.0.0.0
API_PORT=8000
```

### 3. Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "agent_builder.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4. Add Production Features

- Authentication (JWT, API keys)
- Rate limiting
- Caching (Redis)
- Monitoring (Prometheus, Grafana)
- Logging aggregation
- Load balancing
- Auto-scaling

---

## 🛠️ Development

### Add New Agent Category

1. Create file: `examples/your_category_agents.py`
2. Define agents using `@simple_agent` decorator
3. Create `register_your_category_agents()` function
4. Register in `examples/register_agents.py`

### Add New Data Source

1. Add table to `sql/schema.sql`
2. Update `agent_builder/data/generator.py`
3. Add accessor method to `AgentContext`
4. Use in agents via `context.get_your_data()`

### Extend AgentContext

```python
# agent_builder/agents/context.py

@safe_execute(default_return=[])
def get_your_data(self, limit: int = 10) -> List[Dict]:
    """Get your custom data"""
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT * FROM your_table 
            WHERE ticker = %s 
            LIMIT %s
        """, (self.ticker, limit))
        # ... return results
```

---

## 📚 Documentation


   - **[getting-started](docs/gettig-started.md)**
   - **[api-reference](docs/api-reference.md)**
   - **[architecture](docs/architecture.md)**
   - **[creating-agents](docs/creating-agents.md)**

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

1. **More Agents**: Options strategies, pairs trading, arbitrage
2. **Data Sources**: Real-time APIs, alternative data
3. **ML Models**: Predictive models, reinforcement learning
4. **Risk Management**: Position sizing, portfolio optimization
5. **Backtesting**: Historical performance analysis

---

## 📊 Performance Benchmarks

| Metric | Value |
|--------|-------|
| **Agent Execution** | 10-50ms per agent |
| **Full Analysis (61 agents)** | 1-3 seconds |
| **API Response Time** | <100ms (cached) |
| **Database Query** | 1-5ms (with pooling) |
| **Concurrent Analyses** | 10+ simultaneous |

---

## 🎓 Learning Resources

### Investment Strategies
- **Value Investing**: Benjamin Graham, Warren Buffett
- **Technical Analysis**: John Murphy, Steve Nison
- **Risk Management**: Nassim Taleb, Ray Dalio
- **Quantitative**: Ernest Chan, Andreas Clenow

### Technical Skills
- **FastAPI**: https://fastapi.tiangolo.com/
- **PostgreSQL**: https://www.postgresql.org/docs/
- **Docker**: https://docs.docker.com/

---

## ⚠️ Disclaimer

**This software is for educational and research purposes only.**

- NOT financial advice
- NOT a recommendation to buy/sell securities
- Past performance does not guarantee future results
- Investing involves risk of loss
- Consult a licensed financial advisor before making investment decisions

The authors are not responsible for any financial losses incurred from using this software.

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

Built with:
- FastAPI - Modern web framework
- PostgreSQL - Robust database
- Ollama/Groq - LLM providers
- VADER/FinBERT - Sentiment analysis

Inspired by quantitative investment research and systematic trading strategies.

---

## 📬 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Documentation**: See `/docs` directory

---

## 🗺️ Roadmap

### v0.4 (Current)
- ✅ 61 agents across 5 categories
- ✅ Mock database with 5,000+ records
- ✅ Connection pooling
- ✅ FastAPI with async support

### v0.5 (Next)
- [ ] Real-time data integration
- [ ] WebSocket support
- [ ] Advanced backtesting
- [ ] Portfolio optimization

### v1.0 (Future)
- [ ] Machine learning models
- [ ] Multi-asset support (crypto, forex)
- [ ] React dashboard
- [ ] Cloud deployment templates

---

## 🌟 Star History

If you find this project useful, please ⭐ star it on GitHub!

---
