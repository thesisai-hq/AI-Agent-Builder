# System Architecture

## Overview

AI Agent Builder uses a clean, layered architecture for maintainability and extensibility.

## Architecture Diagram

```
┌─────────────────────────────────────┐
│         API Layer (FastAPI)         │
│  - REST endpoints                   │
│  - Request validation               │
│  - Background tasks                 │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Agent Registry Layer           │
│  - Agent discovery                  │
│  - Agent management                 │
│  - Enable/disable control           │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Agent Execution Layer          │
│  - Multiple agent types             │
│  - Parallel execution               │
│  - Result aggregation               │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│       Data Access Layer             │
│  - AgentContext (with caching)      │
│  - Repository pattern               │
│  - Connection pooling               │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│        Storage Layer                │
│  - PostgreSQL (analyses, data)      │
│  - In-memory (registry cache)       │
└─────────────────────────────────────┘
```

## Key Components

### 1. Agent System
- **BaseAgent** - Abstract base class
- **@simple_agent** - Decorator for quick creation
- **AgentContext** - Data access helper
- **Agent Registry** - Central management

### 2. Repository Pattern
- **Repository** - Generic CRUD operations
- **Connection Pool** - Optimized database access
- **Dual Storage** - PostgreSQL or in-memory

### 3. API Gateway
- **FastAPI** - Modern async framework
- **Background Tasks** - Non-blocking execution
- **Lifespan Events** - Startup/shutdown management

### 4. Performance Optimizations
- **Connection Pooling** - 50x faster DB access
- **Caching** - AgentContext caches queries
- **Background Processing** - Non-blocking API

## Data Flow

```
1. User Request
   POST /analyze {"ticker": "AAPL"}
   
2. API Creates Analysis Record
   Saves to database (status: pending)
   
3. Background Task Scheduled
   Returns analysis_id immediately (~12ms)
   
4. Agents Execute (Background)
   ├─ Get enabled agents from registry
   ├─ Each agent analyzes ticker
   ├─ AgentContext fetches data (cached)
   └─ Signals collected
   
5. Consensus Calculated
   Aggregate all agent signals
   
6. Results Saved
   Update analysis (status: completed)
   
7. User Polls for Results
   GET /analyze/{id}
   
Total: ~124ms for 10 agents
```

## Design Patterns

- **Repository Pattern** - Data access abstraction
- **Factory Pattern** - LLM provider selection
- **Decorator Pattern** - Agent creation
- **Registry Pattern** - Agent discovery
- **Context Manager** - Resource cleanup

## Scalability

- **Horizontal** - Stateless design allows multiple instances
- **Vertical** - Connection pooling handles load
- **Async** - Background tasks prevent blocking
- **Caching** - Reduces database load

**Can handle 100+ analyses/minute on single instance**