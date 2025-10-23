# AI Agent Framework

> **Simple, maintainable framework for building AI financial analysis agents**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 What Is This?

A lightweight, production-ready framework for building AI agents that analyze financial data. Designed to be:

- **Simple**: Core framework is ~800 lines
- **Self-contained**: Works immediately with built-in mock data
- **Flexible**: Optional LLM and RAG capabilities
- **Maintainable**: Clean architecture, minimal dependencies
- **Production-ready**: FastAPI backend, type-safe

## ⚡ Quick Start

```bash
# Install
git clone git@github.com:thesisai-hq/AI-Agent-Builder.git
cd AI-Agent-Builder
pip install -e .

# Run examples (work immediately!)
python examples/01_basic.py
python examples/02_llm_agent.py  # Requires Ollama/OpenAI/Anthropic
python examples/03_rag_agent.py  # Requires sentence-transformers
```

## 🏗️ Architecture

```
agent_framework/
├── models.py      # Data structures (Signal, Config)
├── agent.py       # Agent base class
├── llm.py         # LLM client with system prompts
├── rag.py         # RAG system for documents
├── database.py    # Mock database with realistic data
└── api.py         # FastAPI REST endpoints
```

## 📊 Built-in Mock Data

Framework includes realistic data for **4 tickers** (AAPL, MSFT, TSLA, JPM):
- Fundamentals (PE, ROE, margins, growth)
- 90 days price history
- News headlines
- SEC filing excerpts (2000+ words for RAG testing)

**No external data needed for development!**

## 🚀 Usage

### Simple Agent (No LLM)

```python
from agent_framework import Agent, Signal, MockDatabase

class ValueAgent(Agent):
    def analyze(self, ticker: str, data: dict) -> Signal:
        pe = data.get('pe_ratio', 0)
        if pe < 15:
            return Signal('bullish', 0.8, f"PE {pe:.1f} undervalued")
        return Signal('neutral', 0.5, "Fair value")

# Use immediately!
db = MockDatabase()
agent = ValueAgent()
signal = agent.analyze('AAPL', db.get_fundamentals('AAPL'))
print(f"{signal.direction} ({signal.confidence:.0%}): {signal.reasoning}")
```

### LLM Agent with Persona

```python
from agent_framework import Agent, Signal, AgentConfig, LLMConfig

class ConservativeInvestor(Agent):
    def __init__(self):
        config = AgentConfig(
            name="Conservative Investor",
            llm=LLMConfig(
                provider='ollama',
                model='llama3',
                system_prompt="""You are a conservative value investor.
                Focus on: low PE ratios, high dividends, stable businesses.
                Be skeptical of high-growth narratives."""
            )
        )
        super().__init__(config)
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        prompt = f"Analyze {ticker}: PE={data['pe_ratio']}, Growth={data['revenue_growth']}%"
        response = self.llm.chat(prompt)  # Uses system prompt automatically
        # Parse and return signal...
```

### RAG for SEC Filings

```python
from agent_framework import Agent, AgentConfig, RAGConfig

class SECAnalyst(Agent):
    def __init__(self):
        config = AgentConfig(
            name="SEC Analyst",
            rag=RAGConfig(chunk_size=300, top_k=3)
        )
        super().__init__(config)
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        # Add SEC filing to RAG
        self.rag.add_document(filing_text)
        
        # Query specific sections
        context = self.rag.query("What are the key risk factors?")
        
        # Analyze context...
```

## 🎨 Design Principles

### 1. **Dataclasses with Slots**
```python
@dataclass(frozen=True, slots=True)
class Signal:
    direction: str
    confidence: float
    reasoning: str
```
- 76% memory reduction vs regular classes
- Immutable by default (frozen=True)
- Built-in `__repr__`, `__eq__`

### 2. **Lazy Initialization**
```python
class Agent:
    @property
    def llm(self):
        if self._llm is None and self.config.llm:
            self._llm = LLMClient(self.config.llm)
        return self._llm
```
- LLM/RAG only created when accessed
- Simple agents stay simple
- No overhead for unused features

### 3. **System Prompts for Personas**
```python
LLMConfig(
    provider='anthropic',
    model='claude-3-sonnet',
    system_prompt="You are a conservative investor..."  # Agent persona!
)
```
- Each agent can have unique personality
- Consistent behavior across queries
- Works with OpenAI, Anthropic, Ollama

### 4. **Self-Contained Testing**
```python
db = MockDatabase()  # Pre-loaded with 4 tickers
data = db.get_fundamentals('AAPL')  # Works immediately!
```
- No external APIs needed
- Realistic test data
- Fast development cycle

## 📡 REST API

Start the API server:

```bash
python -m uvicorn agent_framework.api:app --reload
```

Endpoints:

```bash
GET  /                      # Health check
GET  /tickers               # List available tickers
GET  /tickers/{ticker}      # Get ticker data
POST /analyze               # Run agent analysis
```

Example:

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "value_agent",
    "ticker": "AAPL"
  }'
```

Alternative:
* Open your browser and type: http://localhost:8000/docs
* You can click tabs for each endpoints and click **Try it out** to try them instead of using CURL in CLI.

## 🧪 Testing

```python
import pytest
from agent_framework import Agent, Signal, MockDatabase

def test_value_agent():
    db = MockDatabase()
    agent = ValueAgent()
    signal = agent.analyze('AAPL', db.get_fundamentals('AAPL'))
    
    assert signal.direction in ('bullish', 'bearish', 'neutral')
    assert 0 <= signal.confidence <= 1
    assert len(signal.reasoning) > 0
```

Run tests:

```bash
pytest tests/
```

## 🔌 LLM Provider Setup

### Ollama (Local)
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull model
ollama pull llama3.2
```

### OpenAI
```python
LLMConfig(
    provider='openai',
    model='gpt-4',
    api_key='sk-...',
    system_prompt="Your agent persona"
)
```

### Anthropic
```python
LLMConfig(
    provider='anthropic',
    model='claude-3-sonnet-20240229',
    api_key='sk-ant-...',
    system_prompt="Your agent persona"
)
```

## 🎯 Use Cases

### 1. **Open Source Framework** (This Repo)
- Core framework code
- Examples with mock data
- Documentation
- Anyone can clone and run

### 2. **Your Investment Backend**
- Use framework as foundation
- Add proprietary agents
- Connect real data sources
- Deploy with your frontend

## 📦 Project Structure

```
AI-Agent-Builder/
├── agent_framework/         # Core package
│   ├── __init__.py         # Public API
│   ├── models.py           # Data structures
│   ├── agent.py            # Agent base
│   ├── llm.py              # LLM client
│   ├── rag.py              # RAG system
│   ├── database.py         # Mock database
│   └── api.py              # FastAPI backend
│
├── examples/               # Working examples
│   ├── 01_basic.py        # Simple agents
│   ├── 02_llm_agent.py    # LLM + personas
│   └── 03_rag_agent.py    # RAG analysis
│
├── tests/
│   └── test_framework.py
│
├── requirements.txt
├── setup.py
└── README.md
```

## 🤝 Contributing

Contributions welcome! This is an open-source framework designed to be simple and maintainable.

## 📄 License

MIT License - see LICENSE file

## 🚀 Roadmap

- [ ] PostgreSQL integration
- [ ] Real-time data connectors
- [ ] Agent composition (ensemble agents)
- [ ] Backtesting framework
- [ ] Web dashboard

## 💡 Philosophy

**Keep It Simple**
- Framework core: ~800 lines
- No unnecessary abstractions
- Clear, readable code
- Minimal dependencies

**Make It Work**
- Self-contained examples
- Built-in mock data
- Works in 30 seconds
- Production-ready patterns

**Stay Maintainable**
- Type hints everywhere
- Dataclasses for data
- Lazy initialization
- Clean separation of concerns

---

**Built with ❤️ for simplicity and maintainability**