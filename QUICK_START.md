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
pip install -e .
```

### Option 2: venv (Built-in Python)

```bash
# Clone and create environment
git clone https://github.com/yourusername/AI-Agent-Builder.git
cd AI-Agent-Builder
python3 -m venv venv
source venv/bin/activate  # Linux/macOS

# Install framework
pip install -e .
```

### Option 3: System Python (Simplest)

```bash
# Clone and install
git clone https://github.com/yourusername/AI-Agent-Builder.git
cd AI-Agent-Builder
pip install -e .
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
python examples/01_basic.py
```

**Expected output:**
```
AI Agent Framework - Basic Example
====================================

📊 Analyzing AAPL - Apple Inc.
PE Ratio: 28.5
Revenue Growth: 8.5%

💡 Value Agent:
   Direction: NEUTRAL
   Confidence: 60%
   Reasoning: PE ratio 28.5 is fairly valued
```

## What's Next?

**Run more examples:**
```bash
python examples/02_llm_agent.py    # AI-powered analysis
python examples/03_rag_agent.py    # Document analysis
```

**Create your own agent:**
```bash
# Copy an example
cp examples/01_basic.py my_agent.py

# Edit and customize
nano my_agent.py

# Run it
python my_agent.py
```

**Read detailed guides:**
- [Getting Started](docs/GETTING_STARTED.md) - Complete installation details
- [Environment Setup](docs/ENVIRONMENT_SETUP.md) - Conda/venv/system Python
- [Configuration](docs/CONFIGURATION.md) - Customize settings
- [Database Guide](docs/DATABASE_SETUP.md) - Database details
- [LLM Customization](docs/LLM_CUSTOMIZATION.md) - AI agent setup

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

# Reinstall
pip install -e .
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
```

## Need Help?

- **Full documentation:** [docs/](docs/)
- **Issues:** [GitHub Issues](https://github.com/thesisai-hq/AI-Agent-Builder/issues)
- **Examples:** [examples/](examples/)

---

**Done!** You're now ready to build AI agents. 🚀
