# Installation Guide

## Prerequisites

- Python 3.10, 3.11, or 3.12
- pip (Python package manager)
- Git (for cloning repository)

## Quick Install

```bash
# Clone repository
git clone https://github.com/yourusername/ai-agent-framework.git
cd AI-Agent-Builder

# Install in development mode
pip install -e .

# Verify installation
python quickstart.py
```

That's it! The framework works immediately with built-in mock data.

## Optional Dependencies

### For LLM Agents

**Option 1: Ollama (Local, Free)**
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Start Ollama if not automatically started
ollama serve

# Pull a model
ollama pull llama3.2

# Install Python client
pip install ollama
```

**Option 2: OpenAI**
```bash
pip install openai

# Add to .env
echo "OPENAI_API_KEY=sk-..." >> .env
```

**Option 3: Anthropic**
```bash
pip install anthropic

# Add to .env
echo "ANTHROPIC_API_KEY=sk-ant-..." >> .env
```

### For RAG (Document Analysis)

```bash
pip install sentence-transformers
```

This will download ~100MB of embedding models on first use.

### All Optional Dependencies

```bash
# Install everything
pip install -e .[all]
```

## Installation Options

### 1. Basic (Core Only)
```bash
pip install -e .
```
- Works immediately with mock data
- No LLM or RAG capabilities
- Perfect for learning the framework

### 2. With LLM Support
```bash
pip install -e .[llm]
```
- Adds OpenAI, Anthropic, Ollama clients
- Enables LLM-powered agents

### 3. With RAG Support
```bash
pip install -e .[rag]
```
- Adds sentence-transformers
- Enables document analysis

### 4. Complete Installation
```bash
pip install -e .[all]
```
- All features enabled
- Includes development tools (pytest, black)

## Verify Installation

Run the quickstart script:

```bash
python quickstart.py
```

Expected output:
```
🔍 Checking imports...
✅ Core imports successful

🗄️  Testing mock database...
✅ Loaded 4 tickers: AAPL, MSFT, TSLA, JPM
✅ AAPL PE Ratio: 28.5
✅ Retrieved 5 days of price data

🤖 Testing simple agent...
✅ Agent analysis: BULLISH (70%)
   Reasoning: PE ratio: 28.5

📚 Testing RAG system...
✅ RAG query successful

🌐 Testing API...
✅ FastAPI app loaded

🎉 Framework is ready to use!
```

## Run Examples

All examples work immediately:

```bash
# Simple agents (no dependencies)
python examples/01_basic.py

# LLM agents (requires Ollama/OpenAI/Anthropic)
python examples/02_llm_agent.py

# RAG analysis (requires sentence-transformers)
python examples/03_rag_agent.py
```

## Start API Server

```bash
uvicorn agent_framework.api:app --reload
```

Visit: http://localhost:8000/docs for API documentation

## Run Tests

```bash
pytest tests/ -v
```

## Troubleshooting

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'agent_framework'`

**Solution:** Install in editable mode:
```bash
pip install -e .
```

### LLM Not Working

**Problem:** LLM agents fail with authentication errors

**Solution:** Set API keys in `.env` file:
```bash
cp .env.example .env
# Edit .env with your API keys
```

For Ollama:
```bash
# Check Ollama is running
ollama list

# Pull a model if needed
ollama pull llama3.2
```

### RAG Slow on First Use

**Problem:** First RAG query takes ~30 seconds

**Solution:** This is normal! Sentence-transformers downloads models on first use. Subsequent queries are fast.

### Tests Failing

**Problem:** Some tests fail with `ModuleNotFoundError`

**Solution:** Install optional dependencies:
```bash
pip install -e .[all]
```

## Uninstall

```bash
pip uninstall ai-agent-framework
```

## Development Setup

For contributing:

```bash
# Clone repo
git clone https://github.com/yourusername/ai-agent-framework.git
cd ai-agent-framework

# Install with dev dependencies
pip install -e .[dev]

# Run tests
pytest tests/ -v

# Format code
black agent_framework/ examples/ tests/

# Run examples
python examples/01_basic.py
```

## Docker Setup (Optional)

```bash
# Build image
docker build -t ai-agent-framework .

# Run container
docker run -p 8000:8000 ai-agent-framework

# With environment variables
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=sk-... \
  ai-agent-framework
```

## Next Steps

1. ✅ Verify installation: `python quickstart.py`
2. 📖 Read the [README.md](README.md)
3. 🎯 Run examples: `python examples/01_basic.py`
4. 🧪 Run tests: `pytest tests/`
5. 🚀 Build your first agent!

## Need Help?

- Check [README.md](README.md) for usage examples
- Review examples in `examples/` directory
- Run `python quickstart.py` to diagnose issues
- Open an issue on GitHub