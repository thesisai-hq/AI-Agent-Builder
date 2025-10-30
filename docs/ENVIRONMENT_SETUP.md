# Python Environment Setup - Complete Guide

Choose between **conda, venv, or system Python**. All work equally well!

## Which Should You Choose?

### Quick Decision Guide

**Choose Conda if you:**
- Work on multiple Python projects
- Do data science or machine learning
- Want the easiest package management
- Like having everything managed in one place

**Choose venv if you:**
- Want to use Python's built-in tools
- Prefer lightweight solutions
- Only work on this one project
- Want minimal setup

**Choose System Python if you:**
- Just want to test things quickly
- Don't work on many Python projects
- Want the absolute simplest setup
- Are okay with global package installation

**Still not sure?** Start with **venv** - it's a good middle ground.

---

## Option 1: Conda (Miniconda)

### Install Miniconda

**What is Miniconda?** Lightweight version of Anaconda (popular in data science). Manages Python versions, packages, and environments.

**WSL2/Linux x86_64:**
```bash
# Download installer
cd ~
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Install (takes 2-3 minutes)
bash Miniconda3-latest-Linux-x86_64.sh

# Follow the prompts:
# 1. Press Enter to read license
# 2. Type 'yes' to accept license
# 3. Press Enter to use default location (~miniconda3)
# 4. Type 'yes' to initialize conda

# Clean up installer
rm Miniconda3-latest-Linux-x86_64.sh

# Activate conda
source ~/.bashrc

# Verify
conda --version
```

**macOS (Intel Chip):**
```bash
cd ~
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
bash Miniconda3-latest-MacOSX-x86_64.sh
# Follow prompts
rm Miniconda3-latest-MacOSX-x86_64.sh
source ~/.zshrc
conda --version
```

**macOS (Apple Silicon - M1/M2/M3):**
```bash
cd ~
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
bash Miniconda3-latest-MacOSX-arm64.sh
# Follow prompts
rm Miniconda3-latest-MacOSX-arm64.sh
source ~/.zshrc
conda --version
```

### Create Project Environment

```bash
# Create environment named 'agent-framework' with Python 3.11
conda create -n agent-framework python=3.11 -y

# This takes 1-2 minutes
```

**What just happened?**
- Created isolated environment called "agent-framework"
- Installed Python 3.11 in it
- This environment is separate from your system Python

### Activate Environment

```bash
# Activate
conda activate agent-framework

# Your terminal prompt should now show: (agent-framework)
```

### Install Project

```bash
# Clone and navigate (if not done already)
cd ~
git clone <repo-url>
cd AI-Agent-Builder

# Install framework with all dependencies
pip install -e ".[all]"

# Or install only what you need:
# pip install -e .            # Core only
# pip install -e ".[llm]"     # Core + LLM support
# pip install -e ".[rag]"     # Core + RAG support
# pip install -e ".[dev]"     # Core + dev tools

# Done!
```

### Daily Usage

```bash
# Every time you work on this project:

# 1. Activate environment
conda activate agent-framework

# 2. Navigate to project
cd ~/AI-Agent-Builder

# 3. Start database
docker compose up -d postgres

# 4. Work on your agents
python my_agent.py

# 5. When done (optional)
docker compose down
conda deactivate
```

### Conda Cheat Sheet

```bash
# Environments
conda env list                              # List all environments
conda activate agent-framework              # Activate
conda deactivate                            # Deactivate
conda create -n myenv python=3.11           # Create new
conda env remove -n myenv                   # Delete environment

# Packages
conda install numpy pandas                  # Install packages
conda install -c conda-forge package-name   # From conda-forge
pip install package-name                    # Use pip in conda (works!)
pip install -e ".[llm]"                     # Install optional deps
conda list                                  # List installed packages
conda update --all                          # Update all packages

# Export/Import
conda env export > environment.yml          # Export
conda env export --no-builds > env.yml      # Cross-platform export
conda env create -f environment.yml         # Create from file

# Maintenance
conda clean --all                           # Clean cache
conda update conda                          # Update conda itself
```

---

## Option 2: venv (Virtual Environment)

### Install Prerequisites

```bash
# Check Python version (need 3.10+)
python3 --version

# If Python not found or too old:
# WSL2/Ubuntu/Debian:
sudo apt update
sudo apt install python3 python3-pip python3-venv

# macOS (with Homebrew):
brew install python3

# Fedora/RHEL:
sudo dnf install python3 python3-pip
```

### Create Virtual Environment

```bash
# Clone repository first
cd ~
git clone <repo-url>
cd AI-Agent-Builder

# Create virtual environment in 'venv' folder
python3 -m venv venv

# Takes 10-20 seconds
```

**What just happened?**
- Created a folder called `venv/` in your project
- Installed a copy of Python and pip in it
- This is your isolated environment

### Activate Environment

```bash
# Activate (from project directory)
source venv/bin/activate

# Your prompt should now show: (venv)
```

### Install Project

```bash
# Make sure venv is activated (you should see (venv) in prompt)

# Install framework with all dependencies
pip install -e ".[all]"

# Or install only what you need:
# pip install -e .            # Core only
# pip install -e ".[llm]"     # Core + LLM support
# pip install -e ".[rag]"     # Core + RAG support
# pip install -e ".[dev]"     # Core + dev tools

# Done!
```

### Daily Usage

```bash
# Every time you work on this project:

# 1. Navigate to project and activate
cd ~/AI-Agent-Builder
source venv/bin/activate

# 2. Start database
docker compose up -d postgres

# 3. Work on your agents
python my_agent.py

# 4. When done (optional)
docker compose down
deactivate
```

### venv Cheat Sheet

```bash
# Create environment
python3 -m venv venv                    # In current directory
python3 -m venv ~/envs/myproject        # In specific location
python3.11 -m venv venv                 # With specific Python version

# Activate
source venv/bin/activate                # Linux/WSL2/macOS

# Deactivate
deactivate

# Check you're in venv
which python                            # Should show venv path
echo $VIRTUAL_ENV                       # Should show venv directory

# Packages
pip install package-name                # Install package
pip install -e ".[llm]"                 # Install optional dependencies
pip list                                # List installed
pip show package-name                   # Show details

# Upgrade
pip install --upgrade pip               # Upgrade pip itself
pip install --upgrade package-name      # Upgrade package

# Remove environment
deactivate                              # Deactivate first
rm -rf venv                             # Delete folder

# Recreate
python3 -m venv venv
source venv/bin/activate
pip install -e ".[all]"
```

---

## Option 3: System Python

### Install Python

```bash
# Check current version
python3 --version

# Need Python 3.10 or newer
```

**If Python not installed or too old:**

**WSL2/Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version
```

**macOS (with Homebrew):**
```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3
python3 --version
```

**Fedora/RHEL:**
```bash
sudo dnf install python3 python3-pip
python3 --version
```

### Install Project

```bash
# Clone repository
cd ~
git clone <repo-url>
cd AI-Agent-Builder

# Install framework with all dependencies
pip install -e ".[all]"

# Or install only what you need:
# pip install -e .            # Core only
# pip install -e ".[llm]"     # Core + LLM support
# pip install -e ".[rag]"     # Core + RAG support
# pip install -e ".[dev]"     # Core + dev tools

# Or install for user only (safer)
pip install --user -e ".[all]"
```

### Daily Usage

```bash
# Navigate to project
cd ~/AI-Agent-Builder

# Start database
docker compose up -d postgres

# Work on your agents (no activation needed!)
python my_agent.py

# When done
docker compose down
```

### System Python Cheat Sheet

```bash
# Install packages
pip install package-name                # May need sudo
pip install --user package-name         # User install (safer)
pip install -e ".[llm]"                 # Install optional dependencies
sudo pip install package-name           # System install (not recommended)

# List packages
pip list                                # All packages
pip list --user                         # User packages only

# Check installation
pip show ai-agent-framework

# Upgrade
pip install --upgrade package-name

# Uninstall
pip uninstall package-name

# Check Python
which python3
python3 --version

# Create alias
echo 'alias python=python3' >> ~/.bashrc
source ~/.bashrc
```

---

## Comparison Table

| Feature | Conda | venv | System Python |
|---------|-------|------|---------------|
| **Installation** | Download Miniconda | Built into Python | Already installed |
| **Setup Time** | 5 minutes | 30 seconds | 0 seconds |
| **Disk Space** | ~500MB base + envs | ~50MB per env | None |
| **Activation** | `conda activate` | `source venv/bin/activate` | None needed |
| **Isolation** | ✅ Excellent | ✅ Good | ❌ None |
| **Package Sources** | conda + pip | pip only | pip only |
| **Multiple Projects** | ✅ Very easy | ✅ Easy | ❌ May conflict |
| **Optional Deps** | ✅ `pip install -e ".[llm]"` | ✅ `pip install -e ".[llm]"` | ✅ `pip install -e ".[llm]"` |
| **Non-Python Packages** | ✅ Yes | ❌ No | ❌ No |
| **Speed** | Medium | Fast | Fastest |
| **Data Science** | ✅ Optimized | ⚠️ Manual install | ⚠️ Manual install |
| **Best For** | ML/Data Science/Multi-project | Standard development | Quick testing/single project |

## Understanding Optional Dependencies

The framework uses modern Python packaging (PEP 621) with optional dependency groups:

```bash
# Install core only (FastAPI, Database, no AI)
pip install -e .

# Install with LLM support (OpenAI, Anthropic, Ollama)
pip install -e ".[llm]"

# Install with RAG support (document analysis)
pip install -e ".[rag]"

# Install with dev tools (pytest, black, ruff)
pip install -e ".[dev]"

# Install everything
pip install -e ".[all]"

# Combine multiple groups
pip install -e ".[llm,rag]"
```

**What's in each group?**

| Group | Packages |
|-------|----------|
| Core | fastapi, uvicorn, pydantic, asyncpg, numpy, python-dotenv |
| `llm` | openai, anthropic, ollama |
| `rag` | sentence-transformers |
| `dev` | pytest, pytest-asyncio, pytest-cov, black, ruff |
| `all` | Everything above |

## Troubleshooting Guide

### Conda Issues

**"conda: command not found"**
```bash
# Restart terminal or:
source ~/miniconda3/bin/activate

# Initialize in current shell
conda init bash  # or zsh

# Restart terminal
```

**"CondaError: Run 'conda init' first"**
```bash
conda init bash  # or zsh
source ~/.bashrc  # or ~/.zshrc
```

**Wrong environment active**
```bash
conda deactivate
conda activate agent-framework
conda env list  # Verify (should have * next to agent-framework)
```

**Package conflicts**
```bash
# Remove and recreate environment
conda deactivate
conda env remove -n agent-framework
conda create -n agent-framework python=3.11 -y
conda activate agent-framework
pip install -e ".[all]"
```

### venv Issues

**"No module named venv"**
```bash
# Install venv module
# Ubuntu/Debian:
sudo apt install python3-venv

# Fedora:
sudo dnf install python3-venv
```

**Can't activate venv**
```bash
# Make sure you're in project directory
cd ~/AI-Agent-Builder
pwd  # Should show .../AI-Agent-Builder

# Then activate
source venv/bin/activate
```

**Wrong Python in venv**
```bash
# Check Python version
which python

# If wrong, recreate with specific version
deactivate
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
python --version  # Verify
```

**ModuleNotFoundError in venv**
```bash
# Ensure venv is activated
source venv/bin/activate
echo $VIRTUAL_ENV  # Should show path

# Reinstall with all dependencies
pip install -e ".[all]"
```

**Missing optional dependencies**
```bash
# If you see "No module named 'openai'" or similar:

# Check what's installed
pip list | grep -E "(openai|anthropic|ollama)"

# Install the missing group
pip install -e ".[llm]"

# Or install everything
pip install -e ".[all]"
```

### System Python Issues

**"Permission denied" when installing**
```bash
# Use --user flag
pip install --user -e ".[all]"

# Or use sudo (not recommended)
sudo pip install -e ".[all]"
```

**Multiple Python versions**
```bash
# Check all installed
ls -la /usr/bin/python*

# Use specific version
python3.11 --version

# Set default (Ubuntu)
sudo update-alternatives --config python3
```

**Conflicts between projects**
```bash
# Solution: Switch to venv or conda!
# With system Python, projects share packages

# Or use --user and careful package management
pip install --user -e ".[all]"
```

## Migration Guide

### From System Python to venv

```bash
# Create venv
cd ~/AI-Agent-Builder
python3 -m venv venv
source venv/bin/activate

# Install in venv
pip install -e ".[all]"
```

### From venv to Conda

```bash
# Create conda environment
conda create -n agent-framework python=3.11 -y
conda activate agent-framework

# Install
cd ~/AI-Agent-Builder
pip install -e ".[all]"

# Optional: Delete old venv
rm -rf venv
```

### From Conda to venv

```bash
# Create venv
cd ~/AI-Agent-Builder
conda deactivate
python3 -m venv venv
source venv/bin/activate

# Install
pip install -e ".[all]"

# Remove conda environment (optional)
conda env remove -n agent-framework
```

## Best Practices

### For Conda Users

```bash
# Install data science packages with conda
conda install numpy pandas matplotlib scikit-learn

# Use pip for the framework and other packages
pip install -e ".[all]"

# Update regularly
conda update --all
```

### For venv Users

```bash
# Create venv in project directory (standard location)
python3 -m venv venv

# Add venv/ to .gitignore (don't commit it)
echo "venv/" >> .gitignore

# Always activate before working
source venv/bin/activate

# Install all dependencies at once
pip install -e ".[all]"
```

### For System Python Users

```bash
# Use --user flag to avoid conflicts
pip install --user -e ".[all]"

# Consider switching to venv if:
# - You work on multiple projects
# - You get package conflicts
# - You want to share exact dependencies
```

## Optional: Ultra-Fast Installation with uv

Want 10-100x faster installations? Use [uv](https://github.com/astral-sh/uv):

```bash
# Install uv (one-time)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create venv with uv (10x faster)
uv venv
source .venv/bin/activate

# Install with uv (100x faster than pip)
uv pip install -e ".[all]"

# Add new packages
uv pip install requests

# uv is a drop-in replacement for pip
# All pip commands work with uv
```

**Why use uv?**
- ✅ 10-100x faster than pip
- ✅ Drop-in replacement (same commands)
- ✅ Works with existing pyproject.toml
- ✅ No configuration changes needed
- ✅ Made by Astral (creators of Ruff)

## Complete Setup Commands

### Conda Setup (Copy entire block)

```bash
# Install Miniconda
cd ~
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc
rm Miniconda3-latest-Linux-x86_64.sh

# Create environment
conda create -n agent-framework python=3.11 -y
conda activate agent-framework

# Install project
git clone <repo-url>
cd AI-Agent-Builder
pip install -e ".[all]"

# Setup
cp .env.example .env
docker compose up -d postgres
sleep 10
python seed_data.py

# Verify
python examples/01_basic.py
```

### venv Setup (Copy entire block)

```bash
# Clone project
cd ~
git clone <repo-url>
cd AI-Agent-Builder

# Create and activate venv
python3 -m venv venv
source venv/bin/activate

# Install
pip install -e ".[all]"

# Setup
cp .env.example .env
docker compose up -d postgres
sleep 10
python seed_data.py

# Verify
python examples/01_basic.py
```

### System Python Setup (Copy entire block)

```bash
# Clone project
cd ~
git clone <repo-url>
cd AI-Agent-Builder

# Install
pip install -e ".[all]"

# Setup
cp .env.example .env
docker compose up -d postgres
sleep 10
python seed_data.py

# Verify
python examples/01_basic.py
```

### uv Setup (Ultra-Fast)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone project
cd ~
git clone <repo-url>
cd AI-Agent-Builder

# Create venv and install (10x faster!)
uv venv
source .venv/bin/activate
uv pip install -e ".[all]"

# Setup
cp .env.example .env
docker compose up -d postgres
sleep 10
python seed_data.py

# Verify
python examples/01_basic.py
```

---

**Chosen your environment? Great! Continue with the rest of the setup in [GETTING_STARTED.md](GETTING_STARTED.md)** 🚀
