# API Reference

REST API documentation for AI-Agent-Builder FastAPI server.

---

## Overview

The framework includes a production-ready REST API built with FastAPI. The API provides endpoints for:
- Health checks and monitoring
- Data access (tickers, fundamentals, prices, news)
- Agent registration and execution
- Analysis requests

**Base URL:** `http://localhost:8000` (configurable via `.env`)

---

## Starting the API Server

```bash
# From project directory
uvicorn agent_framework.api:app --reload

# Or with custom host/port
uvicorn agent_framework.api:app --host 0.0.0.0 --port 8000
```

**Configuration:**
```bash
# .env file
API_HOST=0.0.0.0      # Listen on all interfaces
API_PORT=8000         # Default port
DEBUG=True            # Show detailed errors (dev only)
CORS_ORIGINS=*        # Allowed origins (or comma-separated list)
```

---

## Authentication

Currently no authentication is implemented. This is suitable for:
- Local development
- Internal networks
- Learning environments

**For production:** Implement JWT, API keys, or OAuth2 before deployment.

---

## Endpoints

### Health & Status

#### `GET /`

Root endpoint for basic health check.

**Response:**
```json
{
  "status": "online",
  "framework": "AI Agent Framework",
  "version": "2.0.0",
  "database": "PostgreSQL with asyncpg"
}
```

**Example:**
```bash
curl http://localhost:8000/
```

---

#### `GET /health`

Detailed health check including database status.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "agents": 3,
  "tickers": 4
}
```

**Status values:**
- `healthy` - All systems operational
- `degraded` - Some issues (e.g., database slow)

**Example:**
```bash
curl http://localhost:8000/health
```

---

### Data Access

#### `GET /tickers`

List all available ticker symbols.

**Response:**
```json
[
  "AAPL",
  "MSFT",
  "TSLA",
  "JPM"
]
```

**Example:**
```bash
curl http://localhost:8000/tickers
```

---

#### `GET /tickers/{ticker}`

Get complete data for a specific ticker.

**Parameters:**
- `ticker` (path) - Stock ticker symbol (e.g., AAPL)
- `days` (query, optional) - Days of price history (default: 30)

**Response:**
```json
{
  "ticker": "AAPL",
  "fundamentals": {
    "ticker": "AAPL",
    "name": "Apple Inc.",
    "sector": "Technology",
    "market_cap": 2800000000000,
    "pe_ratio": 28.5,
    "pb_ratio": 45.2,
    "roe": 147.4,
    "profit_margin": 25.3,
    "revenue_growth": 8.6,
    "debt_to_equity": 1.73,
    "current_ratio": 0.93,
    "dividend_yield": 0.5,
    "updated_at": "2025-01-14T10:30:00Z"
  },
  "prices": [
    {
      "date": "2025-01-13",
      "open": 180.50,
      "high": 182.30,
      "low": 179.80,
      "close": 181.90,
      "volume": 52000000
    },
    // ... more price records
  ],
  "news": [
    {
      "date": "2025-01-13",
      "headline": "Apple announces new product",
      "sentiment": "positive",
      "source": "Reuters"
    },
    // ... more news items
  ]
}
```

**Example:**
```bash
# Get AAPL with 30 days of prices (default)
curl http://localhost:8000/tickers/AAPL

# Get AAPL with 90 days of prices
curl "http://localhost:8000/tickers/AAPL?days=90"
```

**Errors:**
- `404` - Ticker not found
- `500` - Database error

---

### Agent Management

#### `GET /agents`

List all registered agents.

**Response:**
```json
[
  "ValueAgent",
  "GrowthAgent",
  "QualityAgent"
]
```

**Example:**
```bash
curl http://localhost:8000/agents
```

**Note:** Agents must be registered via `register_agent_instance()` in Python code.

---

#### `POST /analyze`

Run agent analysis on a ticker.

**Request Body:**
```json
{
  "agent_name": "ValueAgent",
  "ticker": "AAPL",
  "parameters": {}
}
```

**Fields:**
- `agent_name` (string, required) - Name of registered agent
- `ticker` (string, required) - Stock ticker symbol
- `parameters` (object, optional) - Additional parameters for agent

**Response:**
```json
{
  "direction": "bullish",
  "confidence": 0.8,
  "reasoning": "PE ratio 28.5 is fairly valued between 15-30",
  "timestamp": "2025-01-14T10:30:00Z",
  "metadata": {}
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "ValueAgent",
    "ticker": "AAPL"
  }'
```

**Errors:**
- `404` - Agent not found or ticker not found
- `500` - Analysis error

---

## Response Schemas

### Signal Response

```typescript
{
  direction: "bullish" | "bearish" | "neutral",
  confidence: number,  // 0.0 to 1.0
  reasoning: string,
  timestamp: string,   // ISO 8601 format
  metadata: object     // Optional additional data
}
```

---

### Error Response

```typescript
{
  detail: string,      // Error message
  error_type: string   // Error category
}
```

**Common error types:**
- `database_error` - Database query failed
- `connection_error` - Database connection failed
- `validation_error` - Invalid request parameters

---

## Using the API

### Python Example

```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Get ticker data
response = requests.get("http://localhost:8000/tickers/AAPL")
data = response.json()
print(f"PE Ratio: {data['fundamentals']['pe_ratio']}")

# Run analysis
response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "agent_name": "ValueAgent",
        "ticker": "AAPL"
    }
)
signal = response.json()
print(f"{signal['direction']}: {signal['reasoning']}")
```

---

### JavaScript Example

```javascript
// Health check
const health = await fetch('http://localhost:8000/health')
  .then(r => r.json());
console.log(health);

// Get ticker data
const data = await fetch('http://localhost:8000/tickers/AAPL')
  .then(r => r.json());
console.log(`PE Ratio: ${data.fundamentals.pe_ratio}`);

// Run analysis
const signal = await fetch('http://localhost:8000/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    agent_name: 'ValueAgent',
    ticker: 'AAPL'
  })
}).then(r => r.json());
console.log(`${signal.direction}: ${signal.reasoning}`);
```

---

### curl Examples

```bash
# Health check
curl http://localhost:8000/health

# List tickers
curl http://localhost:8000/tickers

# Get ticker data
curl http://localhost:8000/tickers/AAPL

# List agents
curl http://localhost:8000/agents

# Run analysis
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"agent_name":"ValueAgent","ticker":"AAPL"}'
```

---

## Registering Agents

Agents must be registered before they can be used via the API:

```python
from agent_framework import register_agent_instance
from examples.basic import ValueAgent

# Create and register agent
agent = ValueAgent()
register_agent_instance("ValueAgent", agent)

# Now available at /agents and /analyze endpoints
```

**Complete example:**

```python
# my_server.py
from agent_framework import api_app, register_agent_instance
from examples.basic import ValueAgent

# Register agents
value_agent = ValueAgent()
register_agent_instance("ValueAgent", value_agent)

# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api_app, host="0.0.0.0", port=8000)
```

---

## CORS Configuration

Cross-Origin Resource Sharing (CORS) is configured via `.env`:

```bash
# Allow all origins (development only)
CORS_ORIGINS=*

# Allow specific origins (production)
CORS_ORIGINS=https://myapp.com,https://api.myapp.com

# Allow localhost for development
CORS_ORIGINS=http://localhost:3000,http://localhost:8501
```

**Restart server after changes.**

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Common Causes |
|------|---------|---------------|
| `200` | Success | Request completed |
| `404` | Not Found | Ticker or agent doesn't exist |
| `422` | Validation Error | Invalid request parameters |
| `500` | Internal Error | Database error, analysis error |
| `503` | Service Unavailable | Database not connected |

### Error Response Format

```json
{
  "detail": "Ticker INVALID not found",
  "error_type": "database_error"
}
```

---

## OpenAPI Documentation

FastAPI automatically generates interactive API documentation:

**Swagger UI:** `http://localhost:8000/docs`
- Interactive API explorer
- Try endpoints directly in browser
- See request/response schemas

**ReDoc:** `http://localhost:8000/redoc`
- Alternative documentation format
- Better for reading
- Good for sharing with team

---

## Performance

### Response Times

Typical response times (local development):

| Endpoint | Average | Notes |
|----------|---------|-------|
| `GET /` | < 10ms | No database query |
| `GET /health` | 10-20ms | Database health check |
| `GET /tickers` | 10-30ms | Single query |
| `GET /tickers/{ticker}` | 20-50ms | Multiple queries |
| `POST /analyze` | 50-200ms | Rule-based agent |
| `POST /analyze` | 2-5s | LLM-powered agent |

### Connection Pooling

The API uses PostgreSQL connection pooling (default: 2-10 connections):

```python
# Configured in .env
DB_MIN_POOL_SIZE=2
DB_MAX_POOL_SIZE=10
```

**Benefits:**
- 9x faster queries
- Handles concurrent requests efficiently
- Automatic connection reuse

---

## Rate Limiting

**Not currently implemented.** For production:

1. Use middleware (e.g., `slowapi`)
2. Implement per-IP or per-user limits
3. Add rate limit headers to responses

**Example configuration (not included):**
```python
# Rate limit: 100 requests per minute
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
```

---

## Security Considerations

### For Development ✅
- Local access (localhost)
- No authentication
- Debug mode enabled
- CORS allows all origins

### For Production ⚠️

**Required:**
1. **Authentication:** Implement JWT or API keys
2. **HTTPS:** Use SSL/TLS certificates
3. **CORS:** Restrict to specific origins
4. **Rate Limiting:** Prevent abuse
5. **Input Validation:** Already handled by Pydantic
6. **Error Messages:** Disable DEBUG mode (hides stack traces)

**Configuration:**
```bash
# .env (production)
DEBUG=False
CORS_ORIGINS=https://yourdomain.com
API_HOST=0.0.0.0
API_PORT=443
```

---

## Deployment

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -e ".[all]"

EXPOSE 8000
CMD ["uvicorn", "agent_framework.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build and run
docker build -t agent-framework-api .
docker run -p 8000:8000 agent-framework-api
```

### Cloud Deployment

**AWS (Elastic Beanstalk):**
```bash
eb init -p python-3.11 agent-framework
eb create agent-framework-env
eb deploy
```

**Heroku:**
```bash
# Create Procfile
echo "web: uvicorn agent_framework.api:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create agent-framework
git push heroku main
```

**Google Cloud Run:**
```bash
gcloud run deploy agent-framework \
  --source . \
  --platform managed \
  --region us-central1
```

---

## Monitoring

### Health Endpoint

Use `/health` for monitoring:

```bash
# Simple check
curl -f http://localhost:8000/health || echo "Service down"

# Full check with jq
curl -s http://localhost:8000/health | jq
```

### Logging

API uses Python logging (configured via LOG_LEVEL in `.env`):

```bash
# .env
LOG_LEVEL=INFO    # INFO, DEBUG, WARNING, ERROR
```

**View logs:**
```bash
# If running directly
python -m uvicorn agent_framework.api:app

# If using Docker
docker logs <container-id>
```

---

## Advanced Usage

### Custom Endpoints

Add custom endpoints by extending `agent_framework/api.py`:

```python
from agent_framework.api import app

@app.get("/custom")
async def custom_endpoint():
    return {"message": "Custom endpoint"}
```

### Dependency Injection

Use FastAPI dependency injection for database access:

```python
from agent_framework.api import get_db
from fastapi import Depends

@app.get("/custom")
async def custom_endpoint(db: Database = Depends(get_db)):
    tickers = await db.list_tickers()
    return {"tickers": tickers}
```

---

## Testing

### Manual Testing

```bash
# Start server
uvicorn agent_framework.api:app --reload

# Test in another terminal
curl http://localhost:8000/health
```

### Automated Testing

```python
from fastapi.testclient import TestClient
from agent_framework.api import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_tickers():
    response = client.get("/tickers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

---

## Troubleshooting

### API Won't Start

```bash
# Check port not in use
lsof -i :8000

# Try different port
uvicorn agent_framework.api:app --port 8001
```

### Database Connection Failed

```bash
# Check database is running
docker ps | grep postgres

# Check connection string
python -c "from agent_framework import Config; print(Config.get_database_url())"
```

### CORS Errors

```bash
# Add origin to .env
CORS_ORIGINS=http://localhost:3000

# Or allow all (development only)
CORS_ORIGINS=*

# Restart server
```

**See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more issues**

---

## Sentiment Analysis

### calculate_sentiment_score()

The framework includes built-in sentiment analysis using **VADER** (Valence Aware Dictionary and sEntiment Reasoner).

**What is VADER?**

VADER is an industry-standard sentiment analysis tool specifically designed for:
- Social media text
- Financial news and headlines
- Short informal text
- Business communications

**Key Features:**
- ✅ Handles negation ("not good" correctly identified as negative)
- ✅ Understands degree modifiers ("very good" > "good")
- ✅ Recognizes punctuation emphasis ("great!!!" > "great")
- ✅ Accounts for capitalization ("AMAZING" > "amazing")
- ✅ Optimized for financial text

**Usage:**

```python
from agent_framework import calculate_sentiment_score

# Analyze news headline
text = "Strong revenue growth drives stock higher"
direction, confidence = calculate_sentiment_score(text)

print(f"{direction}: {confidence:.1%}")
# Output: bullish: 68%
```

**Return Values:**

**Direction:**
- `"bullish"` - Positive sentiment (VADER compound >= 0.05)
- `"bearish"` - Negative sentiment (VADER compound <= -0.05)
- `"neutral"` - Neutral sentiment (VADER compound between -0.05 and 0.05)

**Confidence:**
- Bullish range: 0.55 to 0.85
- Bearish range: 0.55 to 0.80
- Neutral: 0.60 (fixed)

**VADER Compound Score Mapping:**

| VADER Compound | Direction | Confidence Range | Example |
|----------------|-----------|------------------|----------|
| 0.75 to 1.00 | Bullish | 77% - 85% | "Exceptional growth!!! 🚀" |
| 0.50 to 0.75 | Bullish | 70% - 77% | "Very strong performance" |
| 0.05 to 0.50 | Bullish | 57% - 70% | "Good results" |
| -0.05 to 0.05 | Neutral | 60% | "Company reported earnings" |
| -0.50 to -0.05 | Bearish | 57% - 68% | "Facing challenges" |
| -1.00 to -0.50 | Bearish | 68% - 80% | "Major risks and concerns" |

**Example Use Cases:**

```python
# Positive news
news = "Apple announces record earnings, beating expectations"
direction, conf = calculate_sentiment_score(news)
# Result: bullish, ~75%

# Negative news
text = "Major regulatory challenges and declining market share"
direction, conf = calculate_sentiment_score(text)
# Result: bearish, ~65%

# Neutral statement
text = "The company reported quarterly results"
direction, conf = calculate_sentiment_score(text)
# Result: neutral, 60%

# Negation handling (VADER strength)
text1 = "This is good"
text2 = "This is not good"
dir1, _ = calculate_sentiment_score(text1)  # bullish
dir2, _ = calculate_sentiment_score(text2)  # bearish ✅
# Simple keyword matching would fail on text2!
```

**Fallback Behavior:**

If vaderSentiment package is not installed, automatically falls back to simple keyword matching:

```python
# VADER not installed → uses fallback
direction, confidence = calculate_sentiment_score(text)
# Still works, just less sophisticated
```

**Installation:**

VADER is included in core dependencies:
```bash
pip install -e "."  # Includes vaderSentiment
pip install -e ".[all]"  # Also includes vaderSentiment
```

Or install separately:
```bash
pip install vaderSentiment
```

**Technical Details:**

VADER returns four scores:
- `positive`: Ratio of positive sentiment (0.0 to 1.0)
- `negative`: Ratio of negative sentiment (0.0 to 1.0)
- `neutral`: Ratio of neutral sentiment (0.0 to 1.0)
- `compound`: Normalized composite score (-1.0 to +1.0)

We use the **compound score** as it provides the best overall sentiment indicator.

**References:**
- VADER Paper: Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text.
- GitHub: https://github.com/cjhutto/vaderSentiment

---

## Next Steps

- **[Data Flow](DATA_FLOW.md)** - Understand how data flows through agents ⭐
- **[Multi-Agent Systems](MULTI_AGENT_SYSTEMS.md)** - Build orchestrated strategies ⭐
- **[Configuration Guide](CONFIGURATION.md)** - Environment variables
- **[Database Setup](DATABASE_SETUP.md)** - PostgreSQL details
- **[Project Structure](PROJECT_STRUCTURE.md)** - Code organization

---

**For production deployment, implement authentication and follow security best practices.**
