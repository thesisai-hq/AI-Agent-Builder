# Getting Started with AI Agent Builder

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/ai-agent-builder.git
cd ai-agent-builder
```

### 2. Setup Python Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:
```bash
DATABASE_URL=postgresql://dev:dev@localhost:5433/ai_agents
API_PORT=8000
LLM_PROVIDER=ollama  # or groq
```

### 4. Start Database

```bash
docker-compose up -d
```

### 5. Generate Sample Data

```bash
python generate_mock_data.py --tickers 20
```

### 6. Start API Server

```bash
uvicorn agent_builder.api.main:app --reload
```

Visit: http://localhost:8000/docs

## Your First Agent

Create `my_first_agent.py`:

```python
from agent_builder.agents.builder import simple_agent

@simple_agent("My First Agent", weight=0.15)
def my_agent(ticker, context):
    # Get stock metrics
    pe_ratio = context.get_metric('pe_ratio')
    
    # Make decision
    if pe_ratio < 15:
        return "bullish", 0.8
    else:
        return "neutral", 0.6

# Test it
if __name__ == "__main__":
    signal = my_agent.analyze("AAPL")
    print(f"Signal: {signal.signal_type}")
    print(f"Confidence: {signal.confidence}")
```

Run: `python my_first_agent.py`

## Next Steps

- Read [Creating Agents](creating-agents.md)
- Explore [API Reference](http://localhost:8000/docs)
- Check [Architecture](architecture.md)
- See [Examples](../examples/)