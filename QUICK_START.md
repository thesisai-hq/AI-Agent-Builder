# Quick Start - 5 Minutes

Get the framework running in 5 minutes with copy-paste commands.

## Prerequisites

- Python 3.10+ installed
- Docker installed and running
- Terminal (WSL2, macOS, or Linux)

## Installation

### Option 1: Conda (Recommended for data science)

```bash
# Create environment
conda create -n agent-framework python=3.11 -y
conda activate agent-framework

# Install framework
git clone https://github.com/thesisai-hq/AI-Agent-Builder.git
cd AI-Agent-Builder
pip install -e ".[all]"
```

### Option 2: venv (Built-in Python)

```bash
# Clone and create environment
git clone https://github.com/thesisai-hq/AI-Agent-Builder.git
cd AI-Agent-Builder
python3 -m venv venv
source venv/bin/activate  # Linux/macOS

# Install framework
pip install -e ".[all]"
```

### Option 3: System Python (Simplest)

```bash
# Clone and install
git clone https://github.com/thesisai-hq/AI-Agent-Builder.git
cd AI-Agent-Builder
pip install -e ".[all]"
```

### Install Options Explained

```bash
# Core dependencies only (FastAPI, Database, no LLM)
pip install -e .

# Core + LLM support (OpenAI, Anthropic, Ollama)
pip install -e ".[llm]"

# Core + RAG support (Document analysis)
pip install -e ".[rag]"

# Core + Development tools (pytest, black, etc.)
pip install -e ".[dev]"

# Everything (recommended for getting started)
pip install -e ".[all]"
```

## Setup Database

```bash
# Copy configuration
cp .env.example .env

# Start PostgreSQL
docker compose up -d postgres

# Wait 10 seconds for startup
sleep 10

# Add sample data (AAPL, MSFT, TSLA, JPM)
python seed_data.py
```

**Expected output:**
```
📊 Seeding fundamentals...
  ✓ Added AAPL
  ✓ Added MSFT
  ✓ Added TSLA
  ✓ Added JPM
✅ Database seeding completed successfully!
```

## Run Your First Agent

```bash
# Start with the basic rule-based agent (no AI needed!)
python examples/01_basic.py
```

**Expected output:**
```
Example 1: Basic Rule-Based Agent
====================================

📊 Analyzing AAPL - Apple Inc.
   PE Ratio: 28.5

🟡 NEUTRAL (60%)
   PE ratio 28.5 is fairly valued (between 15-30)
```

## What's Next?

**Follow the learning path:**
```bash
# 1. Rule-based (you just ran this!)
python examples/01_basic.py    # ⭐ Rules only, fast

# 2. LLM-powered (AI analysis)
python examples/02_llm_agent.py  # ⭐⭐ Requires: ollama + llama3.2

# 3. Hybrid (rules + AI)
python examples/03_hybrid.py     # ⭐⭐⭐ Best of both worlds

# 4. RAG document analysis
python examples/04_rag_agent.py  # ⭐⭐⭐⭐ Analyze PDFs, filings

# 5. Famous investor strategies
python examples/05_buffett_quality.py  # Warren Buffett
python examples/06_lynch_garp.py       # Peter Lynch  
python examples/07_graham_value.py     # Benjamin Graham
```

**For LLM examples (02-04), install dependencies:**
```bash
# Install Ollama package
pip install ollama

# Download llama3.2 model
ollama pull llama3.2

# Start Ollama service
ollama serve
```

**Or use the visual GUI (no coding!):**
```bash
./gui/launch.sh
```

**Read detailed guides:**
- [Getting Started](docs/GETTING_STARTED.md) - Complete installation with all environments
- [Configuration](docs/CONFIGURATION.md) - Customize settings
- [Database Guide](docs/DATABASE_SETUP.md) - PostgreSQL details
- [LLM Customization](docs/LLM_CUSTOMIZATION.md) - AI setup
- [Hybrid Agents](docs/HYBRID_AGENTS.md) - Advanced patterns

## Daily Workflow

### Starting Work

**Conda:**
```bash
conda activate agent-framework
cd ~/AI-Agent-Builder
docker compose up -d postgres
```

**venv:**
```bash
cd ~/AI-Agent-Builder
source venv/bin/activate
docker compose up -d postgres
```

**System Python:**
```bash
cd ~/AI-Agent-Builder
docker compose up -d postgres
```

### Stopping Work

```bash
docker compose down
conda deactivate          # If using conda
deactivate                # If using venv
```

## Troubleshooting

### Can't connect to database
```bash
# Check if Docker is running
docker ps

# Restart database
docker compose restart postgres
sleep 10
```

### Module not found
```bash
# Make sure environment is activated
conda activate agent-framework  # If conda
source venv/bin/activate        # If venv

# Reinstall with all dependencies
pip install -e ".[all]"
```

### Missing optional dependencies
```bash
# If you see "No module named 'openai'" or similar:

# Install LLM dependencies
pip install -e ".[llm]"

# Or install everything
pip install -e ".[all]"
```

### Port already in use
```bash
# Edit .env
nano .env
# Change: DB_PORT=5434

# Restart
docker compose down
docker compose up -d postgres
```

See [Database Guide](docs/DATABASE_SETUP.md) for more troubleshooting.

## Optional: Ultra-Fast Installation with uv

Want 10-100x faster installations?

```bash
# Install uv (one-time)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Use uv instead of pip (same commands work!)
cd AI-Agent-Builder
uv pip install -e ".[all]"

# That's it - uv is a drop-in replacement for pip
```

## Quick Commands Reference

```bash
# Environment
conda activate agent-framework        # Activate (conda)
source venv/bin/activate              # Activate (venv)
conda deactivate                      # Deactivate (conda)
deactivate                            # Deactivate (venv)

# Database
docker compose up -d postgres         # Start
docker compose down                   # Stop
docker compose logs postgres          # View logs
docker ps                             # Check status

# Development
python my_agent.py                    # Run agent
pytest tests/                         # Run tests
pip install -e ".[dev]"              # Install dev tools
```

## Need Help?

- **Full documentation:** [docs/](docs/)
- **Issues:** [GitHub Issues](https://github.com/thesisai-hq/AI-Agent-Builder/issues)
- **Examples:** [examples/](examples/)

---

**Done!** You're now ready to build AI agents. 🚀
