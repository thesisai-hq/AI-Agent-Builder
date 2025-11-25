# Multi-Agent Systems Guide

**Build orchestrated investment strategies with multiple agents working together.**

**Audience:** Advanced users, thesis-ai integration developers

**Related Documentation:**
- [Data Flow](DATA_FLOW.md) - Understand multi-agent data flow and transparency
- [Choosing Agent Type](CHOOSING_AGENT_TYPE.md) - Mix different agent types
- [API Reference](API_REFERENCE.md) - Multi-agent API endpoints

---

## What is a Multi-Agent System?

A multi-agent system runs **multiple agents** that analyze the same stock from different perspectives, then combines their insights for better decisions.

### Why Use Multiple Agents?

**Single Agent:**
```
ValueAgent analyzes AAPL
→ Bullish (based only on value metrics)
```

**Multi-Agent System:**
```
ValueAgent analyzes AAPL   → Bullish (undervalued)
GrowthAgent analyzes AAPL  → Bearish (slowing growth)
QualityAgent analyzes AAPL → Bullish (strong margins)

Orchestrator combines signals → Consensus: Neutral
```

**Benefits:**
- ✅ **Diverse perspectives** - Value, growth, quality, etc.
- ✅ **Risk reduction** - Avoid single-strategy bias
- ✅ **Consensus building** - Majority vote or weighted average
- ✅ **Specialized analysis** - Each agent focuses on what it does best

---

## Three Ways to Build Multi-Agent Systems

### 1. Sequential Analysis (Simple)

**Pattern:** Run agents one after another

```python
from agent_framework import Database, Config
import asyncio

async def sequential_analysis(ticker: str):
    """Analyze with multiple agents sequentially."""
    
    db = Database(Config.get_database_url())
    await db.connect()
    
    data = await db.get_fundamentals(ticker)
    
    # Create agents
    value_agent = ValueAgent()
    growth_agent = GrowthAgent()
    quality_agent = QualityAgent()
    
    # Run one at a time
    value_signal = await value_agent.analyze(ticker, data)
    growth_signal = await growth_agent.analyze(ticker, data)
    quality_signal = await quality_agent.analyze(ticker, data)
    
    # Combine results
    signals = [value_signal, growth_signal, quality_signal]
    
    # Simple consensus: majority vote
    bullish = sum(1 for s in signals if s.direction == 'bullish')
    bearish = sum(1 for s in signals if s.direction == 'bearish')
    
    if bullish > bearish:
        consensus = 'bullish'
    elif bearish > bullish:
        consensus = 'bearish'
    else:
        consensus = 'neutral'
    
    await db.disconnect()
    
    return consensus, signals

# Run
consensus, details = asyncio.run(sequential_analysis('AAPL'))
print(f"Consensus: {consensus}")
for i, signal in enumerate(details, 1):
    print(f"  Agent {i}: {signal.direction} ({signal.confidence:.0%})")
```

**Pros:** Simple to understand  
**Cons:** Slower (waits for each agent)

---

### 2. Parallel Analysis (Fast)

**Pattern:** Run all agents simultaneously

```python
import asyncio
from agent_framework import Database, Config

async def parallel_analysis(ticker: str):
    """Analyze with multiple agents in parallel (FAST!)."""
    
    db = Database(Config.get_database_url())
    await db.connect()
    
    data = await db.get_fundamentals(ticker)
    
    # Create agents
    agents = {
        'value': ValueAgent(),
        'growth': GrowthAgent(),
        'quality': QualityAgent(),
        'momentum': MomentumAgent(),
        'sentiment': SentimentAgent()
    }
    
    # Run ALL agents in parallel
    signals = await asyncio.gather(*[
        agent.analyze(ticker, data)
        for agent in agents.values()
    ])
    
    # Map results to agent names
    results = dict(zip(agents.keys(), signals))
    
    await db.disconnect()
    
    return results

# Run
results = asyncio.run(parallel_analysis('AAPL'))

for agent_name, signal in results.items():
    print(f"{agent_name:12s}: {signal.direction:8s} ({signal.confidence:.0%})")
```

**Pros:** Fast (5 agents in ~2-3 seconds instead of 10-15 seconds)  
**Cons:** Slightly more complex

---

### 3. API-Based Multi-Agent (Scalable)

**Pattern:** Agents as microservices

```python
# server.py (deploy this)
from agent_framework import api_app, register_agent_instance
from my_agents import ValueAgent, GrowthAgent, QualityAgent
import uvicorn

# Register all your agents
register_agent_instance("value", ValueAgent())
register_agent_instance("growth", GrowthAgent())
register_agent_instance("quality", QualityAgent())

# Run API server
uvicorn.run(api_app, host="0.0.0.0", port=8000)
```

```python
# orchestrator.py (your main system)
import httpx
import asyncio

async def api_multi_agent_analysis(ticker: str):
    """Query multiple agents via API."""
    
    agent_names = ['value', 'growth', 'quality']
    
    async with httpx.AsyncClient() as client:
        # Call all agents in parallel
        tasks = [
            client.post(
                'http://localhost:8000/analyze',
                json={'agent_name': name, 'ticker': ticker}
            )
            for name in agent_names
        ]
        
        responses = await asyncio.gather(*tasks)
        
        # Parse results
        signals = {}
        for name, resp in zip(agent_names, responses):
            data = resp.json()
            signals[name] = data
        
        return signals

# Run
results = asyncio.run(api_multi_agent_analysis('AAPL'))

for name, signal in results.items():
    print(f"{name}: {signal['direction']} ({signal['confidence']:.0%})")
```

**Pros:**
- ✅ Scalable (each agent can be separate service)
- ✅ Language-agnostic (call from any language)
- ✅ Distributed (agents on different servers)
- ✅ Production-ready

**Cons:**
- More infrastructure (API server)
- Network overhead

---

## Consensus Strategies

### Strategy 1: Majority Vote

```python
def majority_vote(signals: list) -> str:
    """Simple majority consensus."""
    
    bullish = sum(1 for s in signals if s.direction == 'bullish')
    bearish = sum(1 for s in signals if s.direction == 'bearish')
    
    if bullish > len(signals) / 2:
        return 'bullish'
    elif bearish > len(signals) / 2:
        return 'bearish'
    else:
        return 'neutral'
```

**Use when:** All agents equally important

---

### Strategy 2: Weighted Consensus

```python
def weighted_consensus(signals: dict) -> tuple:
    """Weighted by agent expertise."""
    
    # Define weights based on agent specialty
    weights = {
        'value': 0.3,      # 30% weight
        'growth': 0.25,    # 25% weight
        'quality': 0.25,   # 25% weight
        'momentum': 0.2    # 20% weight
    }
    
    # Calculate weighted score
    score = 0
    for name, signal in signals.items():
        if signal.direction == 'bullish':
            score += weights[name] * signal.confidence
        elif signal.direction == 'bearish':
            score -= weights[name] * signal.confidence
    
    # Determine consensus
    if score > 0.3:
        consensus = 'bullish'
    elif score < -0.3:
        consensus = 'bearish'
    else:
        consensus = 'neutral'
    
    return consensus, abs(score)
```

**Use when:** Some agents are more reliable than others

---

### Strategy 3: Confidence-Weighted

```python
def confidence_weighted(signals: list) -> tuple:
    """Weight by each agent's confidence."""
    
    bullish_conf = sum(s.confidence for s in signals if s.direction == 'bullish')
    bearish_conf = sum(s.confidence for s in signals if s.direction == 'bearish')
    neutral_conf = sum(s.confidence for s in signals if s.direction == 'neutral')
    
    total = bullish_conf + bearish_conf + neutral_conf
    
    if total == 0:
        return 'neutral', 0.5
    
    # Highest total confidence wins
    if bullish_conf > max(bearish_conf, neutral_conf):
        return 'bullish', bullish_conf / total
    elif bearish_conf > max(bullish_conf, neutral_conf):
        return 'bearish', bearish_conf / total
    else:
        return 'neutral', neutral_conf / total
```

**Use when:** Higher confidence signals should matter more

---

### Strategy 4: Veto System

```python
def veto_system(signals: dict) -> str:
    """Any strong bearish signal vetoes bullish consensus."""
    
    # Check for strong bearish signals (veto)
    strong_bearish = any(
        s.direction == 'bearish' and s.confidence > 0.8
        for s in signals.values()
    )
    
    if strong_bearish:
        return 'bearish'  # Veto!
    
    # Otherwise, majority vote
    return majority_vote(list(signals.values()))
```

**Use when:** Risk management is critical (avoid bad investments)

---

## Complete Multi-Agent Example

### orchestrator.py

```python
"""Multi-agent orchestrator - Combines signals from multiple agents."""

import asyncio
from typing import Dict, List
from agent_framework import Agent, Signal, Database, Config

# Import your agents
from examples.01_basic import ValueAgent
from examples.05_buffett_quality import BuffettQualityAgent
from examples.06_lynch_garp import LynchGARPAgent


class MultiAgentOrchestrator:
    """Orchestrates multiple agents and combines their signals."""
    
    def __init__(self, agents: Dict[str, Agent], strategy: str = 'weighted'):
        """Initialize orchestrator.
        
        Args:
            agents: Dict of agent_name -> Agent instance
            strategy: 'majority', 'weighted', 'confidence', or 'veto'
        """
        self.agents = agents
        self.strategy = strategy
        self.weights = {
            'value': 0.35,      # Value investing gets highest weight
            'quality': 0.35,    # Quality equally important
            'growth': 0.30      # Growth lower weight (more volatile)
        }
    
    async def analyze(self, ticker: str, data: dict) -> Dict:
        """Run all agents and combine signals.
        
        Args:
            ticker: Stock ticker
            data: Financial data
            
        Returns:
            Dict with consensus signal and individual agent signals
        """
        # Run all agents in parallel (FAST!)
        agent_signals = await asyncio.gather(*[
            agent.analyze(ticker, data)
            for agent in self.agents.values()
        ])
        
        # Map to agent names
        signals = dict(zip(self.agents.keys(), agent_signals))
        
        # Calculate consensus
        consensus, confidence = self._calculate_consensus(signals)
        
        return {
            'ticker': ticker,
            'consensus': {
                'direction': consensus,
                'confidence': confidence,
                'strategy': self.strategy
            },
            'individual_signals': {
                name: {
                    'direction': sig.direction,
                    'confidence': sig.confidence,
                    'reasoning': sig.reasoning
                }
                for name, sig in signals.items()
            },
            'agreement_level': self._calculate_agreement(signals)
        }
    
    def _calculate_consensus(self, signals: Dict[str, Signal]) -> tuple:
        """Calculate consensus based on strategy."""
        
        if self.strategy == 'majority':
            return self._majority_vote(signals)
        elif self.strategy == 'weighted':
            return self._weighted_consensus(signals)
        elif self.strategy == 'confidence':
            return self._confidence_weighted(signals)
        elif self.strategy == 'veto':
            return self._veto_system(signals)
        else:
            return 'neutral', 0.5
    
    def _majority_vote(self, signals: Dict[str, Signal]) -> tuple:
        """Simple majority vote."""
        bullish = sum(1 for s in signals.values() if s.direction == 'bullish')
        bearish = sum(1 for s in signals.values() if s.direction == 'bearish')
        total = len(signals)
        
        if bullish > total / 2:
            return 'bullish', bullish / total
        elif bearish > total / 2:
            return 'bearish', bearish / total
        else:
            return 'neutral', 0.5
    
    def _weighted_consensus(self, signals: Dict[str, Signal]) -> tuple:
        """Weighted by agent expertise."""
        score = 0
        
        for name, signal in signals.items():
            weight = self.weights.get(name, 1.0 / len(signals))
            
            if signal.direction == 'bullish':
                score += weight * signal.confidence
            elif signal.direction == 'bearish':
                score -= weight * signal.confidence
        
        if score > 0.3:
            return 'bullish', min(score, 1.0)
        elif score < -0.3:
            return 'bearish', min(abs(score), 1.0)
        else:
            return 'neutral', 0.5
    
    def _confidence_weighted(self, signals: Dict[str, Signal]) -> tuple:
        """Weight by confidence levels."""
        bullish_conf = sum(s.confidence for s in signals.values() if s.direction == 'bullish')
        bearish_conf = sum(s.confidence for s in signals.values() if s.direction == 'bearish')
        neutral_conf = sum(s.confidence for s in signals.values() if s.direction == 'neutral')
        
        total = bullish_conf + bearish_conf + neutral_conf
        
        if total == 0:
            return 'neutral', 0.5
        
        if bullish_conf > max(bearish_conf, neutral_conf):
            return 'bullish', bullish_conf / total
        elif bearish_conf > max(bullish_conf, neutral_conf):
            return 'bearish', bearish_conf / total
        else:
            return 'neutral', neutral_conf / total
    
    def _veto_system(self, signals: Dict[str, Signal]) -> tuple:
        """Any strong bearish vetoes bullish."""
        # Check for strong bearish (>80% confidence)
        strong_bearish = any(
            s.direction == 'bearish' and s.confidence > 0.8
            for s in signals.values()
        )
        
        if strong_bearish:
            return 'bearish', 0.9  # Veto!
        
        # Otherwise majority
        return self._majority_vote(signals)
    
    def _calculate_agreement(self, signals: Dict[str, Signal]) -> float:
        """Calculate how much agents agree (0-1)."""
        if not signals:
            return 0.0
        
        # Count each direction
        directions = [s.direction for s in signals.values()]
        
        # Most common direction
        from collections import Counter
        counts = Counter(directions)
        most_common_count = counts.most_common(1)[0][1]
        
        # Agreement = % of agents with most common signal
        return most_common_count / len(signals)


async def main():
    """Example usage of multi-agent orchestrator."""
    
    db = Database(Config.get_database_url())
    await db.connect()
    
    # Create agents
    agents = {
        'value': ValueAgent(),
        'quality': BuffettQualityAgent(),
        'growth': LynchGARPAgent()
    }
    
    # Create orchestrator
    orchestrator = MultiAgentOrchestrator(agents, strategy='weighted')
    
    # Analyze stocks
    for ticker in ['AAPL', 'MSFT', 'TSLA']:
        data = await db.get_fundamentals(ticker)
        result = await orchestrator.analyze(ticker, data)
        
        print(f"\n{ticker}:")
        print(f"  Consensus: {result['consensus']['direction'].upper()} "
              f"({result['consensus']['confidence']:.0%})")
        print(f"  Agreement: {result['agreement_level']:.0%}")
        print(f"  Individual signals:")
        
        for name, sig in result['individual_signals'].items():
            print(f"    {name:10s}: {sig['direction']:8s} ({sig['confidence']:.0%}) - {sig['reasoning'][:50]}...")
    
    await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
```

**Save as:** `orchestrator.py`

**Run:**
```bash
python orchestrator.py
```

**Output:**
```
AAPL:
  Consensus: NEUTRAL (65%)
  Agreement: 67%
  Individual signals:
    value     : NEUTRAL  (60%) - Fair value: PE=28.5
    quality   : BULLISH  (75%) - Strong margins and ROE
    growth    : BEARISH  (70%) - Growth slowing from peak
```

---

## REST API Multi-Agent System

### Deploy Agents as API

**Step 1: Create server.py**

```python
# server.py
from agent_framework import api_app, register_agent_instance
from examples.01_basic import ValueAgent
from examples.05_buffett_quality import BuffettQualityAgent
from examples.06_lynch_garp import LynchGARPAgent
import uvicorn

# Register agents (they're now available via API)
register_agent_instance("value", ValueAgent())
register_agent_instance("quality", BuffettQualityAgent())
register_agent_instance("growth", LynchGARPAgent())

print("✅ Registered 3 agents: value, quality, growth")
print("🚀 API available at: http://localhost:8000")
print("📖 API docs: http://localhost:8000/docs")

# Start server
uvicorn.run(api_app, host="0.0.0.0", port=8000, reload=True)
```

**Step 2: Run server**

```bash
python server.py
```

**Step 3: Query from any client**

```bash
# Python client
import httpx
import asyncio

async def query_agents(ticker: str):
    async with httpx.AsyncClient() as client:
        # Get all available agents
        agents_resp = await client.get('http://localhost:8000/agents')
        agent_names = agents_resp.json()
        
        # Query each agent
        results = {}
        for name in agent_names:
            resp = await client.post(
                'http://localhost:8000/analyze',
                json={'agent_name': name, 'ticker': ticker}
            )
            results[name] = resp.json()
        
        return results

# Run
results = asyncio.run(query_agents('AAPL'))
```

```bash
# JavaScript/TypeScript client
async function queryAgents(ticker) {
    // Get agents
    const agents = await fetch('http://localhost:8000/agents').then(r => r.json());
    
    // Query each
    const results = {};
    for (const name of agents) {
        const response = await fetch('http://localhost:8000/analyze', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({agent_name: name, ticker: ticker})
        });
        results[name] = await response.json();
    }
    
    return results;
}
```

```bash
# cURL (any language)
curl http://localhost:8000/agents
# ["value", "quality", "growth"]

curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"agent_name":"value","ticker":"AAPL"}'
```

**Benefits:**
- ✅ Language-agnostic (call from any language)
- ✅ Scalable (microservices)
- ✅ Distributed (different servers)
- ✅ Cacheable (HTTP caching)

---

## Performance Considerations

### Parallel vs Sequential

```python
import time

# Sequential (SLOW)
start = time.time()
for agent in agents:
    signal = await agent.analyze(ticker, data)  # 2s each
# Total: 10 seconds for 5 agents

# Parallel (FAST)
start = time.time()
signals = await asyncio.gather(*[
    agent.analyze(ticker, data) for agent in agents
])
# Total: 2 seconds (all run simultaneously!)
```

**Always use parallel for multiple agents!**

---

### Connection Pooling

```python
# ❌ BAD: Creates new connection for each agent
async def bad_pattern(tickers):
    for ticker in tickers:
        db = Database(...)  # New connection every time!
        await db.connect()
        # ... analyze
        await db.disconnect()

# ✅ GOOD: Reuse single connection
async def good_pattern(tickers):
    db = Database(...)
    await db.connect()  # Connect once
    
    for ticker in tickers:
        # Reuse connection
        data = await db.get_fundamentals(ticker)
        # ... analyze
    
    await db.disconnect()  # Disconnect once
```

---

## Testing Multi-Agent Systems

```python
# test_orchestrator.py
import pytest

@pytest.mark.asyncio
async def test_consensus_majority():
    """Test majority vote consensus."""
    
    # Mock signals
    signals = [
        Signal('bullish', 0.8, 'Strong'),
        Signal('bullish', 0.7, 'Good'),
        Signal('bearish', 0.6, 'Weak'),
    ]
    
    consensus = majority_vote(signals)
    assert consensus == 'bullish'  # 2 out of 3

@pytest.mark.asyncio
async def test_parallel_execution():
    """Test parallel agent execution."""
    import time
    
    start = time.time()
    
    # Run 5 agents in parallel
    agents = [ValueAgent() for _ in range(5)]
    data = {'pe_ratio': 20}
    
    signals = await asyncio.gather(*[
        agent.analyze('TEST', data) for agent in agents
    ])
    
    elapsed = time.time() - start
    
    # Should be fast (parallel, not sequential)
    assert elapsed < 1.0  # All 5 in under 1 second
    assert len(signals) == 5
```

---

## Best Practices

### ✅ DO:

1. **Use parallel execution**
   ```python
   # Parallel (fast)
   signals = await asyncio.gather(*[agent.analyze(...) for agent in agents])
   ```

2. **Reuse database connections**
   ```python
   # Connect once, use many times
   await db.connect()
   for ticker in tickers:
       data = await db.get_fundamentals(ticker)
   await db.disconnect()
   ```

3. **Weight agents appropriately**
   ```python
   # Value agents might be more reliable than momentum
   weights = {'value': 0.4, 'momentum': 0.2}
   ```

4. **Log individual signals**
   ```python
   # Keep audit trail
   for name, signal in signals.items():
       logger.info(f"{name}: {signal.direction} ({signal.confidence})")
   ```

---

### ❌ DON'T:

1. **Don't run sequentially (unless required)**
   ```python
   # Slow (avoid this)
   for agent in agents:
       signal = await agent.analyze(...)
   ```

2. **Don't create connections per agent**
   ```python
   # Wasteful (avoid this)
   class MyAgent(Agent):
       async def analyze(self, ticker, data):
           db = Database(...)  # New connection each time!
   ```

3. **Don't ignore disagreement**
   ```python
   # Check agreement level
   if agreement < 0.5:
       logger.warning(f"Low agreement on {ticker}: {agreement:.0%}")
   ```

4. **Don't treat all agents equally**
   ```python
   # Consider expertise
   # Value agents for value stocks
   # Growth agents for growth stocks
   ```

---

## Consensus Strategy Recommendations

### For Conservative Investors

**Use:** Veto system
```python
strategy='veto'
```

**Why:** Any strong bearish signal prevents bullish recommendation

---

### For Balanced Approach

**Use:** Weighted consensus
```python
strategy='weighted'
weights={'value': 0.4, 'quality': 0.35, 'growth': 0.25}
```

**Why:** Balances different perspectives with expertise weighting

---

### For Equal Treatment

**Use:** Majority vote
```python
strategy='majority'
```

**Why:** Democratic - each agent gets equal say

---

### For High-Conviction Signals

**Use:** Confidence-weighted
```python
strategy='confidence'
```

**Why:** Agents with higher confidence matter more

---

## Example Use Cases

### Use Case 1: Portfolio Screening

```python
"""Screen 100 stocks, keep top 10."""

async def screen_portfolio(tickers: List[str], top_n: int = 10):
    orchestrator = MultiAgentOrchestrator(agents, strategy='weighted')
    
    results = []
    for ticker in tickers:
        data = await db.get_fundamentals(ticker)
        analysis = await orchestrator.analyze(ticker, data)
        results.append((ticker, analysis))
    
    # Sort by consensus confidence
    results.sort(key=lambda x: x[1]['consensus']['confidence'], reverse=True)
    
    # Return top N
    return results[:top_n]
```

---

### Use Case 2: Conflicting Signals Alert

```python
"""Alert when agents disagree."""

def check_for_conflicts(analysis: dict):
    """Alert if agents strongly disagree."""
    
    agreement = analysis['agreement_level']
    
    if agreement < 0.4:
        print(f"⚠️  LOW AGREEMENT on {analysis['ticker']}: {agreement:.0%}")
        print("Individual signals:")
        for name, sig in analysis['individual_signals'].items():
            print(f"  {name}: {sig['direction']} ({sig['confidence']:.0%})")
        print("→ Manual review recommended")
        return True
    
    return False
```

---

### Use Case 3: Sector Rotation

```python
"""Use different agent combinations per sector."""

sector_agents = {
    'Technology': ['growth', 'quality'],      # Tech: Focus on growth + quality
    'Financials': ['value', 'quality'],       # Banks: Value + quality
    'Healthcare': ['quality', 'growth'],      # Healthcare: Quality + growth
    'Utilities': ['value', 'dividend']        # Utilities: Value + income
}

async def sector_aware_analysis(ticker: str, sector: str):
    """Use sector-appropriate agents."""
    
    # Select agents for this sector
    agent_names = sector_agents.get(sector, ['value', 'quality'])
    selected_agents = {name: all_agents[name] for name in agent_names}
    
    # Analyze with sector-specific agents
    orchestrator = MultiAgentOrchestrator(selected_agents)
    return await orchestrator.analyze(ticker, data)
```

---

## API Endpoints Reference

**When you run `python server.py`:**

### GET /health
**Health check**
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "database": "connected",
  "agents": 3,
  "tickers": 4
}
```

---

### GET /agents
**List registered agents**
```bash
curl http://localhost:8000/agents
```

Response:
```json
["value", "quality", "growth"]
```

---

### POST /analyze
**Run agent analysis**
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "value",
    "ticker": "AAPL"
  }'
```

Response:
```json
{
  "direction": "neutral",
  "confidence": 0.6,
  "reasoning": "Fair value: PE=28.5",
  "timestamp": "2025-11-20T10:30:00",
  "metadata": {}
}
```

---

### POST /analyze/batch
**Analyze multiple tickers**
```bash
curl -X POST http://localhost:8000/analyze/batch \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "value",
    "tickers": ["AAPL", "MSFT", "TSLA"]
  }'
```

Response:
```json
{
  "AAPL": {"direction": "neutral", ...},
  "MSFT": {"direction": "bullish", ...},
  "TSLA": {"direction": "bearish", ...}
}
```

---

## Complete Example: Production Multi-Agent

```python
# production_orchestrator.py
"""Production-ready multi-agent system with error handling."""

import asyncio
import logging
from typing import Dict, List
from agent_framework import Agent, Signal, Database, Config

logger = logging.getLogger(__name__)


class ProductionOrchestrator:
    """Production multi-agent orchestrator with error handling."""
    
    def __init__(self, agents: Dict[str, Agent]):
        self.agents = agents
        self.db = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.db = Database(Config.get_database_url())
        await self.db.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.db:
            await self.db.disconnect()
    
    async def analyze_with_fallback(
        self,
        ticker: str,
        data: dict
    ) -> Dict:
        """Analyze with error handling and fallbacks."""
        
        results = {}
        errors = {}
        
        # Run all agents, catch individual errors
        for name, agent in self.agents.items():
            try:
                signal = await asyncio.wait_for(
                    agent.analyze(ticker, data),
                    timeout=30.0  # 30 second timeout per agent
                )
                results[name] = signal
                
            except asyncio.TimeoutError:
                logger.error(f"Agent {name} timed out on {ticker}")
                errors[name] = "timeout"
                
            except Exception as e:
                logger.error(f"Agent {name} failed on {ticker}: {e}")
                errors[name] = str(e)
        
        # Calculate consensus from successful agents only
        if results:
            consensus = self._calculate_consensus(results)
        else:
            # All agents failed
            consensus = {
                'direction': 'neutral',
                'confidence': 0.3,
                'reasoning': 'All agents failed'
            }
        
        return {
            'ticker': ticker,
            'consensus': consensus,
            'successful_agents': len(results),
            'failed_agents': len(errors),
            'signals': results,
            'errors': errors
        }
    
    def _calculate_consensus(self, signals: Dict[str, Signal]) -> dict:
        """Calculate weighted consensus."""
        # Implementation same as before
        pass


# Usage
async def main():
    agents = {
        'value': ValueAgent(),
        'growth': GrowthAgent(),
        'quality': QualityAgent()
    }
    
    async with ProductionOrchestrator(agents) as orchestrator:
        result = await orchestrator.analyze_with_fallback('AAPL', data)
        
        print(f"Consensus: {result['consensus']['direction']}")
        print(f"Successful: {result['successful_agents']}/{len(agents)}")
        
        if result['errors']:
            print(f"Errors: {result['errors']}")
```

---

## Summary

### Multi-Agent Patterns

1. **Sequential** - Simple, slow
2. **Parallel** - Fast, recommended
3. **API-Based** - Scalable, distributed

### Consensus Strategies

1. **Majority Vote** - Democratic
2. **Weighted** - Expertise-based
3. **Confidence-Weighted** - High-conviction focus
4. **Veto** - Risk management

### thesis-ai Integration

- ✅ Import AI-Agent-Builder agents
- ✅ Combine with custom agents
- ✅ Shared database
- ✅ Parallel execution
- ✅ Custom consensus logic

---

**Multi-agent systems enable sophisticated investment strategies!** 🚀
