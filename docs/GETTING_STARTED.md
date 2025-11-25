# Getting Started - Complete Setup Guide

This guide covers installation with **conda, venv, or system Python** on WSL2, macOS, and Linux.

## What You'll Need

- **Terminal access**: WSL2 (Windows), macOS Terminal, or Linux terminal
- **30 minutes** of your time
- **Internet connection**

## Step 1: Choose Your Python Environment

**You have three options. Pick ONE that suits your workflow:**

### Option A: Conda/Miniconda (Recommended for Data Science)

**What is Conda?** A package and environment manager that makes it easy to switch between projects and manage dependencies.

**Why choose Conda?**
- ✅ Easy environment management
- ✅ Great for data science workflows
- ✅ Handles non-Python dependencies
- ✅ Popular in ML/AI community

<details>
<summary><b>Install Miniconda</b></summary>

**Linux/WSL2:**
```bash
# Download installer
cd ~
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Run installer
bash Miniconda3-latest-Linux-x86_64.sh

# Follow prompts:
# - Press Enter to review license
# - Type 'yes' to accept
# - Press Enter to confirm location
# - Type 'yes' to initialize conda

# Remove installer
rm Miniconda3-latest-Linux-x86_64.sh

# Restart terminal or activate:
source ~/.bashrc
```

**macOS (Intel):**
```bash
# Download installer
cd ~
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh

# Run installer
bash Miniconda3-latest-MacOSX-x86_64.sh

# Follow prompts (same as Linux)
rm Miniconda3-latest-MacOSX-x86_64.sh

# Restart terminal or:
source ~/.zshrc  # or ~/.bash_profile
```

**macOS (Apple Silicon/M1/M2/M3):**
```bash
# Download ARM installer
cd ~
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh

# Run installer
bash Miniconda3-latest-MacOSX-arm64.sh

# Follow prompts
rm Miniconda3-latest-MacOSX-arm64.sh
source ~/.zshrc
```

**Verify installation:**
```bash
conda --version
# Should show: conda 23.x.x or newer
```

</details>

**Create project environment:**

```bash
# Create new environment with Python 3.11
conda create -n agent-framework python=3.11 -y

# Activate environment
conda activate agent-framework

# Your prompt should now show: (agent-framework)
```

**Useful conda commands:**

```bash
# List environments
conda env list

# Activate environment
conda activate agent-framework

# Deactivate environment
conda deactivate

# Install package with conda
conda install numpy pandas

# Install package with pip
pip install package-name

# Update conda
conda update conda

# Remove environment (if needed)
conda env remove -n agent-framework

# Export environment
conda env export > environment.yml
```

**Continue to Step 2** →

---

### Option B: venv (Python Built-in, Lightweight)

**What is venv?** Python's built-in tool for creating isolated environments.

**Why choose venv?**
- ✅ Built into Python (no extra installation)
- ✅ Lightweight and fast
- ✅ Simple to understand
- ✅ Standard Python tool

**Prerequisites:**

```bash
# Make sure Python 3.10+ is installed
python3 --version

# If not, install Python first:
# WSL2/Ubuntu/Debian:
sudo apt update
sudo apt install python3 python3-pip python3-venv

# macOS (with Homebrew):
brew install python3

# Fedora/RHEL:
sudo dnf install python3 python3-pip
```

**Create virtual environment:**

```bash
# Navigate to project directory
cd ~
git clone https://github.com/thesisai-hq/AI-Agent-Builder.git
cd AI-Agent-Builder

# Create virtual environment
python3 -m venv venv

# Activate environment
# Linux/WSL2/macOS:
source venv/bin/activate

# Your prompt should now show: (venv)
```

**Useful venv commands:**

```bash
# Activate (from project directory)
cd ~/AI-Agent-Builder
source venv/bin/activate

# Check you're in virtual environment
which python
# Should show: ~/AI-Agent-Builder/venv/bin/python

# Deactivate
deactivate

# Remove environment
rm -rf venv

# Recreate
python3 -m venv venv
```

**Continue to Step 2** →

---

### Option C: System Python (Simplest)

**What is System Python?** Use Python installed directly on your system.

**Why choose System Python?**
- ✅ Simplest setup
- ✅ No environment management needed
- ✅ Good for learning/testing
- ✅ Works everywhere

**Prerequisites:**

```bash
# Check Python version (need 3.10+)
python3 --version

# If not installed or too old:
# WSL2/Ubuntu/Debian:
sudo apt update
sudo apt install python3 python3-pip

# macOS (with Homebrew):
brew install python3

# Fedora/RHEL:
sudo dnf install python3 python3-pip
```

**That's it!** No environment to create. Continue to Step 2 →

---

## Step 2: Install Git and Clone Repository

```bash
# Check if git is installed
git --version
```

**If git not found:**

```bash
# WSL2/Ubuntu/Debian:
sudo apt install git

# macOS:
brew install git

# Fedora/RHEL:
sudo dnf install git
```

**Clone the repository:**

```bash
# Navigate home
cd ~

# Clone repository
git clone https://github.com/thesisai-hq/AI-Agent-Builder.git

# Navigate into project
cd AI-Agent-Builder

# Verify location
pwd

# List files
ls -la
```

## Step 3: Install Framework

**Activate your environment first:**

```bash
# If using conda:
conda activate agent-framework

# If using venv:
cd ~/AI-Agent-Builder
source venv/bin/activate

# If using system Python: (nothing to activate)
```

**Install with dependencies:**

```bash
# From project directory
cd ~/AI-Agent-Builder

# Option 1: Install everything (recommended for beginners)
pip install -e ".[all]"

# Option 2: Core only (no LLM, no RAG)
pip install -e .

# Option 3: Core + LLM support (OpenAI, Anthropic, Ollama)
pip install -e ".[llm]"

# Option 4: Core + RAG support (Document analysis)
pip install -e ".[rag]"

# Option 5: Core + Dev tools (pytest, black, etc.)
pip install -e ".[dev]"

# Takes 2-3 minutes
```

**What do the brackets mean?**
- `.` - Install the current package (agent_framework)
- `[all]` - Also install optional dependencies (llm + rag + dev)
- `-e` - Editable mode (changes to code take effect immediately)

**Verify:**

```bash
# Check installation
pip show ai-agent-framework

# Test import
python -c "from agent_framework import Agent, Database; print('✅ Success!')"
```

## Step 4: Install Docker

Follow platform-specific instructions:

**WSL2:** Install Docker Desktop for Windows  
**macOS:** Install Docker Desktop or use Homebrew  
**Linux:** Use get-docker.sh script

See detailed instructions in collapsible sections in README.md

## Step 5: Start Database

```bash
# Copy environment file
cp .env.example .env

# Start PostgreSQL
docker compose up -d postgres

# Wait for startup
sleep 10

# Verify
docker ps
```

## Step 6: Load Sample Data

```bash
# Environment should be activated
# conda activate agent-framework  # if conda
# source venv/bin/activate        # if venv

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

## Step 7: Run Examples

```bash
# Simple rule-based agents (no LLM required)
python examples/01_basic.py

# AI-powered agents (requires: pip install -e ".[llm]")
python examples/02_llm_agent.py

# Document analysis (requires: pip install -e ".[rag]")
python examples/03_rag_agent.py
```

## Environment Comparison

| Feature | Conda | venv | System Python |
|---------|-------|------|---------------|
| Setup | Install Miniconda | Built-in | Already there |
| Commands | `conda activate` | `source venv/bin/activate` | None |
| Isolation | ✅ Excellent | ✅ Good | ❌ None |
| Package Mgmt | conda + pip | pip only | pip only |
| Multiple Projects | ✅ Very easy | ✅ Easy | ❌ May conflict |
| Disk Space | ~500MB | ~50MB per env | Minimal |
| **Best For** | Data science | Standard dev | Quick testing |

## Dependency Groups Explained

The framework uses modern Python packaging (PEP 621) with optional dependency groups:

**Core dependencies** (always installed):
```
fastapi, uvicorn, pydantic, asyncpg, numpy, python-dotenv
```

**Optional dependencies:**

| Group | Description | Install Command |
|-------|-------------|-----------------|
| `llm` | OpenAI, Anthropic, Ollama support | `pip install -e ".[llm]"` |
| `rag` | Document analysis with sentence-transformers | `pip install -e ".[rag]"` |
| `dev` | Testing and linting tools | `pip install -e ".[dev]"` |
| `all` | Everything above | `pip install -e ".[all]"` |

**Combine multiple groups:**
```bash
# LLM + RAG, but not dev tools
pip install -e ".[llm,rag]"
```

## Troubleshooting

### Conda Issues

```bash
# Command not found after install
source ~/miniconda3/bin/activate
conda init bash  # or zsh

# Wrong environment active
conda deactivate
conda activate agent-framework

# Package conflicts
conda env remove -n agent-framework
conda create -n agent-framework python=3.11 -y
conda activate agent-framework
pip install -e ".[all]"
```

### venv Issues

```bash
# Can't activate venv
cd ~/AI-Agent-Builder
source venv/bin/activate

# Wrong Python in venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -e ".[all]"

# ModuleNotFoundError
source venv/bin/activate  # Make sure activated!
pip install -e ".[all]"
```

### System Python Issues

```bash
# Use python3 not python
python3 --version
alias python=python3

# Permission denied
pip install --user -e ".[all]"

# Multiple Python versions
python3.11 --version
update-alternatives --config python3
```

### Missing Dependencies

```bash
# If you see "No module named 'openai'" or similar:

# Install the missing group
pip install -e ".[llm]"     # For OpenAI, Anthropic, Ollama
pip install -e ".[rag]"     # For document analysis
pip install -e ".[all]"     # For everything

# Check what's installed
pip list | grep -E "(openai|anthropic|ollama|sentence)"
```

## Complete Setup Scripts

### For Conda Users

```bash
# Save as setup_conda.sh
cd ~
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc
conda create -n agent-framework python=3.11 -y
conda activate agent-framework
git clone https://github.com/thesisai-hq/AI-Agent-Builder.git
cd AI-Agent-Builder
pip install -e ".[all]"
cp .env.example .env
docker compose up -d postgres
sleep 10
python seed_data.py
python examples/01_basic.py
```

### For venv Users

```bash
# Save as setup_venv.sh
cd ~
git clone <repo-url>
cd AI-Agent-Builder
python3 -m venv venv
source venv/bin/activate
pip install -e ".[all]"
cp .env.example .env
docker compose up -d postgres
sleep 10
python seed_data.py
python examples/01_basic.py
```

### For System Python Users

```bash
# Save as setup_system.sh
cd ~
git clone <repo-url>
cd AI-Agent-Builder
pip install -e ".[all]"
cp .env.example .env
docker compose up -d postgres
sleep 10
python seed_data.py
python examples/01_basic.py
```

## Optional: Ultra-Fast Installation with uv

Want 10-100x faster installations? Use [uv](https://github.com/astral-sh/uv):

```bash
# Install uv (one-time)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Use uv instead of pip (same syntax!)
uv pip install -e ".[all]"

# Create virtual environment with uv (even faster)
uv venv
source .venv/bin/activate
uv pip install -e ".[all]"

# uv is 10-100x faster than pip and fully compatible
```

## Next Steps

- Read [DATA_FLOW.md](DATA_FLOW.md) - Understand how data flows through agents ⭐
- Read [MULTI_AGENT_SYSTEMS.md](MULTI_AGENT_SYSTEMS.md) - Learn orchestration patterns ⭐
- Read [CONFIGURATION.md](CONFIGURATION.md) for settings
- Read [LLM_CUSTOMIZATION.md](LLM_CUSTOMIZATION.md) for AI options
- See [FRAMEWORK_QUICKSTART.md](FRAMEWORK_QUICKSTART.md) for framework guide

---

**Remember:** Any environment works! Choose what you're comfortable with. 🚀
