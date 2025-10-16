# API Reference

Complete reference for the AI Investment Advisor REST API.

---

## 📍 Base URL

```
http://localhost:8000
```

For production, replace with your domain:
```
https://api.yourdomain.com
```

---

## 🔐 Authentication

**Current:** No authentication (testing/development)

**Production:** Add one of:
- API Keys (header: `X-API-Key`)
- JWT Bearer tokens
- OAuth 2.0

---

## 📡 Endpoints

### Root

Get API information and status.

```http
GET /
```

**Response 200:**
```json
{
  "name": "AI Agent Builder API",
  "version": "0.6.0",
  "architecture": "optimized with connection pooling",
  "storage": {
    "agents": "registry (in-memory)",
    "analyses": "postgresql with connection pool"
  },
  "performance": {
    "connection_pooling": true,
    "pool_size": "2-10 connections"
  },
  "agents": {
    "total_agents": 61,
    "enabled_agents": 61,
    "disabled_agents": 0,
    "agent_ids": ["value_investor", "rsi_momentum", ...]
  },
  "docs": "/docs"
}
```

---

### Health Check

Check API and database health.

```http
GET /health
```

**Response 200:**
```json
{
  "status": "healthy",
  "timestamp": "2024-10-16T10:30:00Z",
  "database": "connected (pooled)",
  "agents": {
    "total_agents": 61,
    "enabled_agents": 61,
    "disabled_agents": 0
  }
}
```

**Use for:** 
- Kubernetes liveness probes
- Load balancer health checks
- Monitoring systems

---

### List Agents

Get all registered agents.

```http
GET /agents
GET /agents?enabled=true
GET /agents?enabled=false
```

**Query Parameters:**

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `enabled` | boolean | Filter by enabled status | null (all) |

**Response 200:**
```json
{
  "agents": [
    {
      "id": "value_investor",
      "name": "Value Investor",
      "weight": 0.15,
      "enabled": true,
      "tags": ["fundamental", "value"],
      "type": "SimpleAgent"
    },
    {
      "id": "rsi_momentum",
      "name": "RSI Momentum",
      "weight": 0.11,
      "enabled": true,
      "tags": ["technical", "momentum"],
      "type": "SimpleAgent"
    }
  ],
  "total": 61
}
```

**Examples:**
```bash
# List all agents
curl http://localhost:8000/agents

# List only enabled agents
curl http://localhost:8000/agents?enabled=true

# List disabled agents
curl http://localhost:8000/agents?enabled=false
```

---

### Get Agent Details

Get metadata for a specific agent.

```http
GET /agents/{agent_id}
```

**Path Parameters:**

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `agent_id` | string | Agent identifier | Yes |

**Response 200:**
```json
{
  "id": "value_investor",
  "name": "Value Investor",
  "weight": 0.15,
  "enabled": true,
  "tags": ["fundamental", "value"],
  "type": "SimpleAgent"
}
```

**Response 404:**
```json
{
  "detail": "Agent not found"
}
```

**Example:**
```bash
curl http://localhost:8000/agents/value_investor
```

---

### Enable Agent

Enable a previously disabled agent.

```http
POST /agents/{agent_id}/enable
```

**Path Parameters:**

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `agent_id` | string | Agent identifier | Yes |

**Response 200:**
```json
{
  "status": "enabled",
  "agent_id": "value_investor"
}
```

**Response 404:**
```json
{
  "detail": "Agent not found"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/agents/value_investor/enable
```

---

### Disable Agent

Disable an agent (won't be used in analyses).

```http
POST /agents/{agent_id}/disable
```

**Path Parameters:**

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `agent_id` | string | Agent identifier | Yes |

**Response 200:**
```json
{
  "status": "disabled",
  "agent_id": "value_investor"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/agents/value_investor/disable
```

---

### Run Analysis

Start a stock analysis with agents.

```http
POST /analyze
Content-Type: application/json
```

**Request Body:**
```json
{
  "ticker": "AAPL",
  "agent_ids": ["value_investor", "rsi_momentum"]  // optional
}
```

**Request Schema:**

| Field | Type | Description | Required | Validation |
|-------|------|-------------|----------|------------|
| `ticker` | string | Stock ticker | Yes | 1-5 uppercase letters |
| `agent_ids` | array[string] | Specific agents to use | No | Valid agent IDs |

**Response 202 Accepted:**
```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending"
}
```

**Response 400 Bad Request:**
```json
{
  "detail": [
    {
      "loc": ["body", "ticker"],
      "msg": "Invalid ticker format: ticker123",
      "type": "value_error"
    }
  ]
}
```

**Response 500 Internal Server Error:**
```json
{
  "error": "Internal server error",
  "message": "Failed to create analysis"
}
```

**Examples:**

```bash
# Analyze with all agents
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'

# Analyze with specific agents
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "MSFT",
    "agent_ids": ["value_investor", "growth_investor", "rsi_momentum"]
  }'

# Multiple tickers (run separately)
for ticker in AAPL MSFT GOOGL; do
  curl -X POST http://localhost:8000/analyze \
    -H "Content-Type: application/json" \
    -d "{\"ticker\": \"$ticker\"}"
done
```

**Notes:**
- Analysis runs asynchronously (background task)
- Response is immediate (<100ms)
- Use `analysis_id` to retrieve results
- Results available in 1-3 seconds

---

### Get Analysis Results

Retrieve completed analysis results.

```http
GET /analyze/{analysis_id}
```

**Path Parameters:**

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `analysis_id` | string | UUID from POST /analyze | Yes |

**Response 200 (Pending):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "ticker": "AAPL",
  "status": "pending",
  "signals": [],
  "consensus": null,
  "error": null,
  "started_at": "2024-10-16T10:30:00Z",
  "completed_at": null
}
```

**Response 200 (Completed):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "ticker": "AAPL",
  "status": "completed",
  "signals": [
    {
      "agent_name": "Value Investor",
      "signal_type": "bullish",
      "confidence": 0.85,
      "reasoning": "Value Investor analysis",
      "timestamp": "2024-10-16T10:30:01Z"
    },
    {
      "agent_name": "RSI Momentum",
      "signal_type": "bullish",
      "confidence": 0.75,
      "reasoning": "RSI Momentum analysis",
      "timestamp": "2024-10-16T10:30:01Z"
    }
  ],
  "consensus": {
    "signal": "bullish",
    "confidence": 0.75,
    "agreement": 0.82,
    "distribution": {
      "bullish": 50,
      "bearish": 8,
      "neutral": 3
    }
  },
  "error": null,
  "started_at": "2024-10-16T10:30:00Z",
  "completed_at": "2024-10-16T10:30:02Z"
}
```

**Response 200 (Failed):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "ticker": "INVALID",
  "status": "failed",
  "signals": [],
  "consensus": null,
  "error": "No agents available",
  "started_at": "2024-10-16T10:30:00Z",
  "completed_at": "2024-10-16T10:30:01Z"
}
```

**Response 404:**
```json
{
  "detail": "Analysis not found"
}
```

**Examples:**

```bash
# Get results
curl http://localhost:8000/analyze/550e8400-e29b-41d4-a716-446655440000

# Pretty print with jq
curl http://localhost:8000/analyze/550e8400-e29b-41d4-a716-446655440000 | jq

# Extract consensus only
curl http://localhost:8000/analyze/550e8400-e29b-41d4-a716-446655440000 | jq '.consensus'

# Poll until complete
while true; do
  status=$(curl -s http://localhost:8000/analyze/abc-123 | jq -r '.status')
  echo "Status: $status"
  [ "$status" = "completed" ] && break
  sleep 1
done
```

---

## 📊 Response Schemas

### AgentSignal Schema

```typescript
{
  agent_name: string,        // "Value Investor"
  signal_type: string,       // "bullish" | "bearish" | "neutral"
  confidence: number,        // 0.0 to 1.0
  reasoning: string,         // Explanation
  timestamp: string          // ISO 8601 datetime
}
```

### Consensus Schema

```typescript
{
  signal: string,            // "bullish" | "bearish" | "neutral"
  confidence: number,        // Average confidence (0.0 to 1.0)
  agreement: number,         // Agreement percentage (0.0 to 1.0)
  distribution: {
    bullish: number,         // Count of bullish signals
    bearish: number,         // Count of bearish signals
    neutral: number          // Count of neutral signals
  }
}
```

### Analysis Schema

```typescript
{
  id: string,                // UUID
  ticker: string,            // Stock ticker (uppercase)
  status: string,            // "pending" | "completed" | "failed"
  signals: AgentSignal[],    // Array of agent signals
  consensus: Consensus,      // Aggregate consensus
  error: string | null,      // Error message if failed
  started_at: string,        // ISO 8601 datetime
  completed_at: string | null // ISO 8601 datetime
}
```

---

## 🔧 Request/Response Examples

### Example 1: Full Analysis Workflow

```bash
# 1. Start analysis
RESPONSE=$(curl -s -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}')

# 2. Extract analysis ID
ANALYSIS_ID=$(echo $RESPONSE | jq -r '.analysis_id')
echo "Analysis ID: $ANALYSIS_ID"

# 3. Wait for completion
sleep 3

# 4. Get results
curl http://localhost:8000/analyze/$ANALYSIS_ID | jq
```

### Example 2: Compare Multiple Stocks

```bash
# Analyze multiple stocks
for TICKER in AAPL MSFT GOOGL TSLA; do
  echo "Analyzing $TICKER..."
  
  RESPONSE=$(curl -s -X POST http://localhost:8000/analyze \
    -H "Content-Type: application/json" \
    -d "{\"ticker\": \"$TICKER\"}")
  
  ANALYSIS_ID=$(echo $RESPONSE | jq -r '.analysis_id')
  
  sleep 3
  
  CONSENSUS=$(curl -s http://localhost:8000/analyze/$ANALYSIS_ID | jq '.consensus')
  
  echo "$TICKER: $CONSENSUS"
  echo "---"
done
```

### Example 3: Python Client

```python
import requests
import time

class InvestmentAdvisorClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def analyze(self, ticker, agent_ids=None, wait=True):
        """Run analysis and optionally wait for results"""
        # Start analysis
        payload = {"ticker": ticker}
        if agent_ids:
            payload["agent_ids"] = agent_ids
        
        response = requests.post(
            f"{self.base_url}/analyze",
            json=payload
        )
        response.raise_for_status()
        
        analysis_id = response.json()['analysis_id']
        
        if not wait:
            return analysis_id
        
        # Poll for results
        max_attempts = 30
        for attempt in range(max_attempts):
            time.sleep(1)
            
            result = requests.get(
                f"{self.base_url}/analyze/{analysis_id}"
            ).json()
            
            if result['status'] == 'completed':
                return result
            elif result['status'] == 'failed':
                raise Exception(f"Analysis failed: {result['error']}")
        
        raise TimeoutError("Analysis timeout")
    
    def list_agents(self, enabled_only=False):
        """List all agents"""
        url = f"{self.base_url}/agents"
        if enabled_only:
            url += "?enabled=true"
        
        return requests.get(url).json()
    
    def get_agent(self, agent_id):
        """Get specific agent"""
        return requests.get(
            f"{self.base_url}/agents/{agent_id}"
        ).json()
    
    def enable_agent(self, agent_id):
        """Enable an agent"""
        return requests.post(
            f"{self.base_url}/agents/{agent_id}/enable"
        ).json()
    
    def disable_agent(self, agent_id):
        """Disable an agent"""
        return requests.post(
            f"{self.base_url}/agents/{agent_id}/disable"
        ).json()

# Usage
client = InvestmentAdvisorClient()

# Run analysis
result = client.analyze("AAPL")
print(f"Consensus: {result['consensus']['signal']}")
print(f"Confidence: {result['consensus']['confidence']}")

# List agents
agents = client.list_agents(enabled_only=True)
print(f"Enabled agents: {agents['total']}")
```

---

## ⚠️ Error Responses

### 400 Bad Request

Invalid input parameters.

```json
{
  "detail": [
    {
      "loc": ["body", "ticker"],
      "msg": "Invalid ticker format: aapl123",
      "type": "value_error"
    }
  ]
}
```

**Common causes:**
- Invalid ticker format (must be 1-5 uppercase letters)
- Invalid agent_id format
- Missing required fields

### 404 Not Found

Resource doesn't exist.

```json
{
  "detail": "Analysis not found"
}
```

**Common causes:**
- Invalid analysis_id
- Invalid agent_id
- Analysis expired/deleted

### 500 Internal Server Error

Server error during processing.

```json
{
  "error": "Internal server error",
  "message": "Failed to create analysis",
  "path": "/analyze"
}
```

**Common causes:**
- Database connection lost
- Agent execution error
- Unexpected exception

**Debug mode** (DEBUG=true in .env):
```json
{
  "error": "Internal server error",
  "message": "division by zero in agent XYZ",
  "path": "/analyze"
}
```

---

## 🎯 Usage Patterns

### Pattern 1: Simple Analysis

```bash
# Single analysis
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'
```

### Pattern 2: Batch Analysis

```bash
#!/bin/bash
# analyze_portfolio.sh

TICKERS="AAPL MSFT GOOGL TSLA AMZN"

for ticker in $TICKERS; do
  echo "Analyzing $ticker..."
  
  ANALYSIS_ID=$(curl -s -X POST http://localhost:8000/analyze \
    -H "Content-Type: application/json" \
    -d "{\"ticker\": \"$ticker\"}" | jq -r '.analysis_id')
  
  echo "$ticker: $ANALYSIS_ID"
done

echo "All analyses started. Waiting 5 seconds..."
sleep 5

# Retrieve all results
for ticker in $TICKERS; do
  # Get most recent analysis for ticker
  # (You'd need to store analysis_ids from above)
  echo "Results for $ticker:"
  # curl http://localhost:8000/analyze/$ANALYSIS_ID | jq '.consensus'
done
```

### Pattern 3: Filtered Agents

```bash
# Use only fundamental agents
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "agent_ids": [
      "value_investor",
      "growth_investor",
      "quality_screener",
      "cash_flow_quality"
    ]
  }'

# Use only technical agents
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "agent_ids": [
      "moving_average_crossover",
      "rsi_momentum",
      "macd_signal"
    ]
  }'
```

### Pattern 4: Monitoring Loop

```python
import requests
import time

def monitor_stock(ticker, interval=300):
    """Monitor a stock every 5 minutes"""
    client = InvestmentAdvisorClient()
    
    while True:
        try:
            result = client.analyze(ticker, wait=True)
            
            consensus = result['consensus']
            print(f"[{time.strftime('%H:%M:%S')}] {ticker}: "
                  f"{consensus['signal']} ({consensus['confidence']:.2f})")
            
            # Alert on strong signals
            if consensus['confidence'] > 0.8:
                send_alert(ticker, consensus)
            
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(interval)

# Monitor AAPL every 5 minutes
monitor_stock("AAPL", interval=300)
```

---

## 🔍 Querying Results

### Filter Signals

```bash
# Get only bullish signals
curl http://localhost:8000/analyze/$ANALYSIS_ID | \
  jq '.signals[] | select(.signal_type == "bullish")'

# Get high-confidence signals (>0.8)
curl http://localhost:8000/analyze/$ANALYSIS_ID | \
  jq '.signals[] | select(.confidence > 0.8)'

# Count signals by type
curl http://localhost:8000/analyze/$ANALYSIS_ID | \
  jq '.signals | group_by(.signal_type) | map({type: .[0].signal_type, count: length})'
```

### Extract Specific Data

```bash
# Just the consensus
curl http://localhost:8000/analyze/$ANALYSIS_ID | jq '.consensus'

# Signal and confidence only
curl http://localhost:8000/analyze/$ANALYSIS_ID | \
  jq '{signal: .consensus.signal, confidence: .consensus.confidence}'

# List all agent names
curl http://localhost:8000/analyze/$ANALYSIS_ID | \
  jq '.signals[].agent_name'
```

---

## 🚀 Advanced Usage

### Rate Limiting (Future)

When implemented:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1634400000
```

### Pagination (Future)

When implemented for listing endpoints:

```http
GET /analyses?page=1&per_page=20
```

### WebSocket (Future)

Real-time analysis updates:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/analyze');

ws.send(JSON.stringify({ticker: 'AAPL'}));

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Progress:', data);
};
```

---

## 📝 API Best Practices

### 1. Handle Async Nature

```python
# Good: Wait for completion
analysis_id = start_analysis("AAPL")
time.sleep(3)
results = get_analysis(analysis_id)

# Bad: Immediate fetch (will be pending)
analysis_id = start_analysis("AAPL")
results = get_analysis(analysis_id)  # status: "pending"
```

### 2. Check Status

```python
def wait_for_analysis(analysis_id, timeout=30):
    """Poll until complete or timeout"""
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        result = get_analysis(analysis_id)
        
        if result['status'] == 'completed':
            return result
        elif result['status'] == 'failed':
            raise Exception(f"Analysis failed: {result['error']}")
        
        time.sleep(1)
    
    raise TimeoutError("Analysis timeout")
```

### 3. Handle Errors Gracefully

```python
try:
    result = client.analyze("AAPL")
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 400:
        print("Invalid ticker or parameters")
    elif e.response.status_code == 500:
        print("Server error, try again later")
except requests.exceptions.ConnectionError:
    print("Cannot connect to API")
```

### 4. Use Appropriate Timeouts

```python
# Set reasonable timeout
response = requests.post(
    url,
    json=payload,
    timeout=10  # 10 seconds
)
```

### 5. Validate Responses

```python
result = client.analyze("AAPL")

# Check status
if result['status'] != 'completed':
    raise Exception("Analysis not complete")

# Check consensus exists
if not result['consensus']:
    raise Exception("No consensus generated")

# Validate signal type
valid_signals = ['bullish', 'bearish', 'neutral']
if result['consensus']['signal'] not in valid_signals:
    raise Exception("Invalid signal type")
```

---

## 🌐 CORS Configuration

### Allowed Origins

Configure in `.env`:
```bash
CORS_ORIGINS=http://localhost:3000,http://localhost:8080,https://yourdomain.com
```

### Preflight Requests

The API handles OPTIONS requests automatically:

```http
OPTIONS /analyze
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: POST, GET, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

---

## 📚 Interactive Documentation

### Swagger UI

**URL:** http://localhost:8000/docs

Features:
- Try-it-out functionality
- Request/response examples
- Schema documentation
- Authentication testing

### ReDoc

**URL:** http://localhost:8000/redoc

Features:
- Clean documentation layout
- Downloadable OpenAPI spec
- Code examples
- Search functionality

### OpenAPI Spec

**URL:** http://localhost:8000/openapi.json

Download the OpenAPI 3.0 specification for:
- Code generation
- API testing tools
- Documentation generators

---

## 🎓 Next Steps

- **[Getting Started](getting-started.md)** - Setup guide
- **[Creating Agents](creating-agents.md)** - Build custom agents
- **[Architecture](architecture.md)** - System design

---

**Questions?** Check the interactive docs at http://localhost:8000/docs