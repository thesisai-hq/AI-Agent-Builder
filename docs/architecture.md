# Architecture Guide

This document explains the system architecture, design patterns, and technical decisions behind the AI Investment Advisor framework.

---

## 🏗️ System Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  (HTTP Clients, Frontend Apps, Scripts, API Consumers)          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   FastAPI       │
                    │  REST API       │
                    │  (Port 8000)    │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌────▼─────┐      ┌─────▼──────┐     ┌─────▼──────┐
    │ Endpoint │      │ Background │     │  Registry  │
    │ Handlers │      │   Tasks    │     │  (Agents)  │
    └────┬─────┘      └─────┬──────┘     └─────┬──────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                    ┌────────▼────────┐
                    │ Agent Execution │
                    │   Orchestrator  │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
         ┌────▼────┐   ┌─────▼─────┐  ┌───▼────┐
         │Fundamental│ │ Technical │  │  Macro │
         │  Agents   │ │  Agents   │  │ Agents │
         │   (12)    │ │   (13)    │  │  (13)  │
         └────┬──────┘ └─────┬─────┘  └───┬────┘
              │              │            │
         ┌────▼────┐   ┌─────▼─────┐
         │Sentiment│   │   Risk    │
         │ Agents  │   │  Agents   │
         │  (11)   │   │   (12)    │
         └────┬────┘   └─────┬─────┘
              │              │
              └──────┬───────┘
                     │
            ┌────────▼─────────┐
            │  Agent Context   │
            │ (Data Access)    │
            └────────┬─────────┘
                     │
            ┌────────▼─────────┐
            │ Connection Pool  │
            │  (2-10 conns)    │
            └────────┬─────────┘
                     │
            ┌────────▼─────────┐
            │   PostgreSQL     │
            │   (13 Tables)    │
            └──────────────────┘
```

---

## 🧩 Core Components

### 1. API Layer (`agent_builder/api/`)

**Purpose:** RESTful interface for client applications

**Key Files:**
- `main.py` - FastAPI application, endpoints, lifecycle management

**Features:**
- Async request handling
- Background task processing
- CORS support
- Global error handling
- Health checks
- Request validation (Pydantic)

**Design Pattern:** REST API with async/await

**Endpoints:**
```
GET  /                  # Root info
GET  /health            # Health check
GET  /agents            # List agents
POST /analyze           # Start analysis
GET  /analyze/{id}      # Get results
POST /agents/{id}/enable   # Enable agent
POST /agents/{id}/disable  # Disable agent
```

### 2. Agent System (`agent_builder/agents/`)

**Purpose:** Core agent abstraction and registry

**Key Files:**
- `base_agent.py` - Abstract base class, AgentSignal
- `builder.py` - @simple_agent decorator, SimpleAgent wrapper
- `context.py` - AgentContext for data access
- `registry.py` - AgentRegistry for managing agents
- `personas.py` - LLM system prompts

**Design Patterns:**
- **Abstract Factory:** BaseAgent interface
- **Decorator:** @simple_agent for easy agent creation
- **Registry:** Centralized agent management
- **Context Object:** Unified data access

**Agent Lifecycle:**
```
1. Define: @simple_agent decorator
2. Register: registry.register()
3. Enable/Disable: registry.enable/disable()
4. Execute: agent.analyze(ticker)
5. Return: AgentSignal(signal, confidence)
```

### 3. Data Layer (`agent_builder/data/`)

**Purpose:** Mock data generation for testing

**Key Files:**
- `generator.py` - MockDataGenerator class
- `setup.py` - Database setup utilities

**Features:**
- Realistic financial data generation
- 8 pre-configured stock profiles
- Correlated data (news matches trends)
- Calculated technical indicators
- Calculated risk metrics

**Design Pattern:** Factory + Builder

### 4. Repository Layer (`agent_builder/repositories/`)

**Purpose:** Database abstraction and connection management

**Key Files:**
- `connection.py` - Connection pooling
- `repository.py` - CRUD operations

**Features:**
- Connection pooling (2-10 connections)
- Context manager for auto-cleanup
- Dual backend support (PostgreSQL + in-memory)
- Transaction management

**Design Pattern:** Repository + Singleton (ConnectionPool)

**Connection Pool Architecture:**
```
Request 1 ──┐
Request 2 ──┼──► Connection Pool ──┐
Request 3 ──┘     (2-10 conns)     ├──► PostgreSQL
                                    │
Conn1 (available) ◄─────────────────┤
Conn2 (in use)                      │
Conn3 (in use)                      │
Conn4 (available) ◄─────────────────┘
```

**Performance:** ~50x faster than creating new connections

### 5. LLM Providers (`agent_builder/llm/`)

**Purpose:** Large Language Model integration

**Key Files:**
- `base.py` - LLMProvider interface
- `ollama.py` - Local Ollama integration
- `groq.py` - Groq cloud API integration
- `factory.py` - Provider selection

**Design Pattern:** Strategy + Factory

**Supported Providers:**
- **Ollama** - Local, free, private
- **Groq** - Cloud, fast, API key required

**Usage:**
```python
llm = get_llm_provider()
response = llm.generate(
    prompt="Analyze AAPL",
    system_prompt="You are a value investor...",
    temperature=0.7
)
```

### 6. Sentiment Analysis (`agent_builder/sentiment/`)

**Purpose:** Text sentiment analysis

**Key Files:**
- `base.py` - SentimentAnalyzer interface
- `vader.py` - VADER (fast, rule-based)
- `finbert.py` - FinBERT (accurate, ML-based)
- `factory.py` - Analyzer selection

**Design Pattern:** Strategy + Factory

**Comparison:**

| Feature | VADER | FinBERT |
|---------|-------|---------|
| **Speed** | <1ms | 100-200ms |
| **Accuracy** | Good | Excellent |
| **Setup** | None | Model download |
| **Size** | 1MB | 500MB |
| **Best For** | Testing | Production |

---

## 🔄 Request Flow

### Analysis Request Lifecycle

```
1. Client sends POST /analyze
   ↓
2. API validates request (Pydantic)
   ↓
3. Generate analysis_id (UUID)
   ↓
4. Create analysis record (status: pending)
   ↓
5. Save to database (repository)
   ↓
6. Return 202 Accepted with analysis_id
   ↓
7. Schedule background task
   ↓
8. Background task executes:
   ├─ Get enabled agents from registry
   ├─ For each agent:
   │  ├─ Create AgentContext(ticker)
   │  ├─ Agent accesses data via context
   │  ├─ Agent returns (signal, confidence)
   │  └─ Collect AgentSignal
   ├─ Calculate consensus from all signals
   └─ Update analysis record (status: completed)
   ↓
9. Client polls GET /analyze/{id}
   ↓
10. Return completed analysis with consensus
```

**Timeline:**
- Steps 1-6: <100ms (immediate response)
- Steps 7-8: 1-3 seconds (background)
- Step 9: <10ms (cached result)

---

## 💾 Data Architecture

### Database Schema Design

```
mock_fundamentals (1:N)
    │
    ├──► mock_balance_sheet
    ├──► mock_cash_flow
    ├──► mock_earnings
    ├──► mock_sec_filings
    ├──► mock_prices (1:N)
    │       └──► mock_technical_indicators (1:1)
    ├──► mock_news
    ├──► mock_analyst_ratings
    ├──► mock_insider_trades
    ├──► mock_risk_metrics
    └──► mock_options_data

mock_macro_indicators (shared, no FK)
```

**Design Decisions:**

1. **Foreign Keys:** All tables reference `mock_fundamentals(ticker)`
2. **Cascade Deletes:** Remove stock → removes all related data
3. **Unique Constraints:** Prevent duplicate records
4. **Indexes:** Optimized for common queries (ticker, date)
5. **Views:** Pre-aggregated data for performance

### Normalized Design

**Normalization Level:** 3NF (Third Normal Form)

**Benefits:**
- No data duplication
- Easy to update
- Referential integrity
- Efficient storage

**Trade-offs:**
- Requires JOINs for complex queries
- Views help mitigate this

### Denormalization Strategy

Views provide denormalized access:

```sql
-- Instead of JOINing 3 tables:
SELECT * FROM mock_latest_prices;

-- Instead of complex aggregation:
SELECT * FROM mock_analyst_consensus;
```

---

## 🔐 Security Architecture

### Input Validation Layers

```
1. Pydantic Models (API Layer)
   ↓ Validates: ticker format, agent_ids format
   
2. Security Module (Application Layer)
   ↓ Validates: table names, ticker regex, agent IDs
   
3. Parameterized Queries (Database Layer)
   ↓ Prevents: SQL injection via parameters
   
4. Column Whitelisting (Context Layer)
   ↓ Validates: metric_name in ALLOWED_METRICS
```

### SQL Injection Prevention

**Multi-layered approach:**

1. **Table Whitelist:**
```python
ALLOWED_TABLES = frozenset([
    "mock_fundamentals",
    "mock_prices",
    # ... only these tables allowed
])

def validate_table_name(table: str) -> str:
    if table not in ALLOWED_TABLES:
        raise ValueError("Invalid table")
    return table
```

2. **Column Whitelist:**
```python
ALLOWED_METRICS = frozenset([
    'pe_ratio', 'roe', 'market_cap',
    # ... only these columns allowed
])
```

3. **Parameterized Queries:**
```python
# SAFE (parameterized)
cursor.execute(
    "SELECT * FROM mock_prices WHERE ticker = %s",
    (ticker,)
)

# UNSAFE (never do this)
cursor.execute(
    f"SELECT * FROM mock_prices WHERE ticker = '{ticker}'"
)
```

4. **Input Sanitization:**
```python
def sanitize_ticker(ticker: str) -> str:
    # Only allow A-Z, 1-5 characters
    if not re.match(r"^[A-Z]{1,5}$", ticker.upper()):
        raise ValueError("Invalid ticker")
    return ticker.upper()
```

---

## ⚡ Performance Optimization

### Connection Pooling

**Problem:** Creating new database connections is slow (50ms+)

**Solution:** Connection pool maintains reusable connections

```python
class ConnectionPool:
    _pool = SimpleConnectionPool(
        minconn=2,    # Always keep 2 open
        maxconn=10,   # Maximum 10 concurrent
        **db_params
    )
    
    @classmethod
    def get_connection(cls):
        return cls._pool.getconn()  # Fast! (~1ms)
    
    @classmethod
    def return_connection(cls, conn):
        cls._pool.putconn(conn)  # Return to pool
```

**Performance Impact:**
- Without pool: 50ms per query
- With pool: 1-5ms per query
- **~50x faster!**

### Context Caching

**Problem:** Agents may request same data multiple times

**Solution:** Cache results in AgentContext

```python
class AgentContext:
    def __init__(self, ticker):
        self._cache = {}  # Per-analysis cache
    
    def get_metric(self, metric_name):
        cache_key = f"metric_{metric_name}"
        if cache_key in self._cache:
            return self._cache[cache_key]  # Cached!
        
        # Fetch from database
        value = self._fetch_from_db(metric_name)
        self._cache[cache_key] = value
        return value
```

**Cache Scope:** Per-analysis (fresh for each request)

### Background Task Processing

**Problem:** Analysis takes 1-3 seconds (blocks HTTP request)

**Solution:** Async processing with immediate response

```python
@app.post("/analyze", status_code=202)
async def analyze(request, background_tasks):
    # Create analysis record (fast)
    analysis_id = create_analysis(request.ticker)
    
    # Schedule background execution
    background_tasks.add_task(
        execute_analysis,
        analysis_id,
        request.ticker
    )
    
    # Return immediately
    return {"analysis_id": analysis_id, "status": "pending"}
```

**User Experience:**
- Request: <100ms response
- Poll for results: <10ms (database lookup)
- No blocking!

### Database Indexes

**Strategically placed indexes:**

```sql
-- Prices: ticker + date queries
CREATE INDEX idx_prices_ticker_date 
ON mock_prices(ticker, date DESC);

-- News: recent news queries
CREATE INDEX idx_news_ticker_date 
ON mock_news(ticker, published_at DESC);

-- Technicals: latest indicators
CREATE INDEX idx_technical_ticker_date 
ON mock_technical_indicators(ticker, date DESC);
```

**Query Performance:**
- Without index: 50-100ms (table scan)
- With index: 1-5ms (index scan)

---

## 🎯 Design Patterns

### 1. Registry Pattern

**Purpose:** Centralized agent management

```python
class AgentRegistry:
    def __init__(self):
        self._agents = {}       # Store instances
        self._metadata = {}     # Store metadata
    
    def register(self, agent, weight=0.1, tags=[]):
        agent_id = generate_id(agent.name)
        self._agents[agent_id] = agent
        self._metadata[agent_id] = {...}
    
    def get_enabled_agents(self):
        return [agent for id, agent in self._agents.items()
                if self._metadata[id]['enabled']]
```

**Benefits:**
- Single source of truth for agents
- Easy enable/disable
- Metadata management
- Discovery mechanism

### 2. Decorator Pattern

**Purpose:** Simplify agent creation

```python
def simple_agent(name, weight=0.1):
    def decorator(func):
        agent = SimpleAgent(name, func, weight)
        func.agent = agent
        return func
    return decorator

# Usage:
@simple_agent("My Agent", weight=0.15)
def my_agent(ticker, context):
    return "bullish", 0.8
```

**Benefits:**
- Clean syntax
- Minimal boilerplate
- Familiar Python idiom
- Easy to understand

### 3. Context Object Pattern

**Purpose:** Encapsulate data access

```python
class AgentContext:
    def __init__(self, ticker):
        self.ticker = ticker
        self._cache = {}
    
    def get_metric(self, name):
        # Handle caching, errors, fallbacks
        pass
```

**Benefits:**
- Hides database complexity
- Consistent interface
- Automatic caching
- Error handling
- Easy to mock for testing

### 4. Factory Pattern

**Purpose:** Create instances based on configuration

```python
def get_llm_provider(provider_name=None):
    provider = provider_name or Config.LLM_PROVIDER
    
    if provider == 'ollama':
        return OllamaProvider(...)
    elif provider == 'groq':
        return GroqProvider(...)
```

**Benefits:**
- Configuration-driven
- Easy to add providers
- Decouples creation from usage

### 5. Repository Pattern

**Purpose:** Abstract data persistence

```python
class Repository:
    def save(self, table, data):
        # Abstract database operations
        pass
    
    def find_by_id(self, table, id):
        pass
```

**Benefits:**
- Swappable backends (PostgreSQL, in-memory)
- Testable (mock repository)
- Business logic separated from persistence

---

## 🔀 Agent Execution Flow

### Sequential Execution (Current)

```python
def execute_analysis(ticker, agents):
    signals = []
    
    for agent in agents:  # Sequential
        signal = agent.analyze(ticker)
        signals.append(signal)
    
    return calculate_consensus(signals)
```

**Pros:**
- Simple
- Predictable order
- Easy to debug

**Cons:**
- Slower (agents run one-by-one)
- One slow agent blocks others

**Performance:** 61 agents × 30ms = ~2 seconds

### Parallel Execution (Future Enhancement)

```python
from concurrent.futures import ThreadPoolExecutor

def execute_analysis(ticker, agents):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(agent.analyze, ticker)
            for agent in agents
        ]
        
        signals = [f.result() for f in futures]
    
    return calculate_consensus(signals)
```

**Potential Performance:** 61 agents in parallel = ~200ms

---

## 🎲 Consensus Algorithm

### Current Implementation (Simple Majority)

```python
def calculate_consensus(signals):
    # Count votes
    signal_counts = {}
    total_confidence = 0
    
    for signal in signals:
        signal_type = signal['signal_type']
        confidence = signal['confidence']
        
        signal_counts[signal_type] = signal_counts.get(signal_type, 0) + 1
        total_confidence += confidence
    
    # Majority wins
    majority_signal = max(signal_counts.items(), key=lambda x: x[1])
    
    # Calculate metrics
    agreement = majority_signal[1] / len(signals)
    avg_confidence = total_confidence / len(signals)
    
    return {
        'signal': majority_signal[0],
        'confidence': avg_confidence,
        'agreement': agreement
    }
```

### Alternative Algorithms (Future)

**1. Weighted Voting:**
```python
# Weight by agent weight and confidence
weighted_votes = {}
for signal in signals:
    weight = signal['agent_weight'] * signal['confidence']
    weighted_votes[signal['signal_type']] += weight
```

**2. Confidence Threshold:**
```python
# Only count high-confidence signals
high_conf_signals = [s for s in signals if s['confidence'] > 0.7]
```

**3. Category-Based:**
```python
# Separate consensus for each category
fundamental_consensus = consensus([s for s in signals if 'fundamental' in s['tags']])
technical_consensus = consensus([s for s in signals if 'technical' in s['tags']])
```

---

## 🗂️ Data Flow

### Read Path (Query)

```
Agent calls context.get_metric('pe_ratio')
    ↓
Check cache (in-memory dict)
    ↓ (if not cached)
Get connection from pool
    ↓
Execute parameterized query
    ↓
Fetch result
    ↓
Cache result
    ↓
Return to agent
    ↓
Return connection to pool
```

**Performance:** 
- Cached: <1ms
- Uncached: 1-5ms
- No connection overhead (pooled)

### Write Path (Analysis Storage)

```
Analysis completed
    ↓
Prepare data (signals, consensus)
    ↓
Get connection from pool
    ↓
Serialize to JSON (JSONB)
    ↓
Execute INSERT/UPDATE
    ↓
Commit transaction
    ↓
Return connection to pool
```

---

## 🏛️ System Design Principles

### 1. Separation of Concerns

Each layer has a single responsibility:
- **API:** HTTP handling
- **Agents:** Analysis logic
- **Context:** Data access
- **Repository:** Persistence
- **Connection:** Database connectivity

### 2. Dependency Inversion

High-level modules don't depend on low-level modules:

```python
# High-level (Agent)
def analyze(ticker, context):
    pe = context.get_metric('pe_ratio')  # Abstract interface
    
# Low-level (Context implementation)
class AgentContext:
    def get_metric(self, name):
        # Actual database query
```

### 3. Open/Closed Principle

Open for extension, closed for modification:

```python
# Add new agent: Just create and register (no core changes)
@simple_agent("New Agent")
def new_agent(ticker, context):
    return "bullish", 0.8

registry.register(new_agent.agent)
```

### 4. Single Responsibility

Each agent does one thing:
- Value Investor: Only P/E + ROE + Debt analysis
- RSI Momentum: Only RSI indicator
- News Sentiment: Only news aggregation

### 5. DRY (Don't Repeat Yourself)

Shared utilities:
- `@safe_execute` decorator for error handling
- `get_db_cursor()` context manager
- `AgentContext` for data access

---

## 🔧 Configuration Management

### Centralized Configuration

```python
class Config:
    # Single source of truth
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    DATABASE_URL = os.getenv("DATABASE_URL", "memory")
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
```

**Benefits:**
- Environment-based
- Type conversion
- Default values
- Easy to test

### Configuration Hierarchy

```
1. Environment variables (.env file)
   ↓
2. Config class (with defaults)
   ↓
3. Runtime (can override in code)
```

---

## 📊 Scalability Considerations

### Current Limits

- **Concurrent analyses:** ~10 (connection pool limit)
- **Agents per analysis:** Unlimited (sequential execution)
- **Database size:** Limited by PostgreSQL
- **API throughput:** ~100 req/sec (single instance)

### Scaling Strategies

**Horizontal Scaling:**
```
Load Balancer
    ├──► API Instance 1
    ├──► API Instance 2
    └──► API Instance 3
            ↓
    Shared PostgreSQL
```

**Vertical Scaling:**
- Increase connection pool size
- Add more CPU cores
- Increase RAM for caching

**Database Scaling:**
- Read replicas for queries
- Write master for updates
- Connection pooling per instance

**Task Queue (Future):**
```
API → Redis Queue → Workers → Database
```

---

## 🔍 Error Handling Strategy

### Layers of Error Handling

**1. Decorator Level:**
```python
@safe_execute(default_return=0, log_error=True)
def get_metric(self, name):
    # If error, returns 0 and logs
```

**2. Context Manager Level:**
```python
@contextmanager
def get_db_cursor():
    try:
        cursor = conn.cursor()
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
```

**3. API Level:**
```python
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(status_code=500, ...)
```

**4. Agent Level:**
```python
try:
    signal = agent.analyze(ticker)
    signals.append(signal)
except Exception as e:
    logger.error(f"Agent {agent.name} failed: {e}")
    # Continue with other agents
```

### Graceful Degradation

System continues working even if:
- Some agents fail (use remaining agents)
- Database slow (use defaults/cache)
- LLM unavailable (fall back to rule-based)

---

## 🎯 Design Decisions & Trade-offs

### Decision: Sequential vs Parallel Agent Execution

**Current:** Sequential
- **Pro:** Simple, predictable, easier to debug
- **Con:** Slower for many agents

**Future:** Parallel (ThreadPoolExecutor)
- **Pro:** 10x+ faster
- **Con:** More complex, harder to debug

**Reason:** Simplicity for v0.4, parallel in v0.5

### Decision: Synchronous vs Async Agents

**Current:** Synchronous functions
```python
def analyze(ticker, context):
    return signal, confidence
```

**Alternative:** Async functions
```python
async def analyze(ticker, context):
    return signal, confidence
```

**Reason:** Most agents are CPU-bound, not I/O-bound. Async adds complexity without benefits.

### Decision: Background Tasks vs Real-time

**Current:** Background tasks (202 Accepted)
- **Pro:** Fast API response, no blocking
- **Con:** Client must poll for results

**Alternative:** Server-Sent Events / WebSockets
- **Pro:** Real-time results
- **Con:** More complex, stateful connections

**Reason:** Background tasks simpler for REST API pattern

### Decision: In-Memory Registry vs Database

**Current:** In-memory registry (agents stored in RAM)
- **Pro:** Fast, simple, no persistence needed
- **Con:** Lost on restart

**Alternative:** Database-backed registry
- **Pro:** Persists across restarts
- **Con:** Slower, more complex

**Reason:** Agents are code, not data. Should be in version control, not database.

---

## 🔮 Future Enhancements

### Short Term (v0.5)

1. **Parallel Agent Execution**
   - ThreadPoolExecutor for agents
   - 10x performance improvement

2. **Agent Performance Tracking**
   - Track accuracy per agent
   - Dynamic weight adjustment
   - Historical performance metrics

3. **WebSocket Support**
   - Real-time analysis updates
   - Streaming results

### Medium Term (v0.6)

1. **Real Data Integration**
   - Alpha Vantage, Finnhub, Yahoo Finance
   - Data refresh pipeline
   - Historical data backfill

2. **Backtesting Framework**
   - Test agent performance
   - Historical accuracy
   - Strategy optimization

3. **Advanced Consensus**
   - Weighted voting
   - Confidence thresholds
   - Category-based consensus

### Long Term (v1.0)

1. **Machine Learning Agents**
   - Predictive models
   - Reinforcement learning
   - Meta-learning

2. **Multi-Asset Support**
   - Stocks, ETFs, Crypto, Forex
   - Portfolio analysis
   - Correlation matrices

3. **Production Features**
   - Authentication & authorization
   - Rate limiting
   - Caching layer (Redis)
   - Monitoring & observability

---

## 📚 Additional Reading

- **[Creating Agents](creating-agents.md)** - Build custom agents
- **[API Reference](api-reference.md)** - Complete API docs
- **[Getting Started](getting-started.md)** - Installation guide

---

**Questions about architecture?** Open an issue on GitHub!