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
git clone <repo-url>
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

# Save dependencies
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt
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

# Clone repository (replace with actual URL)
git clone <repo-url>

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

**Install:**

```bash
# From project directory
cd ~/AI-Agent-Builder

# Install framework
pip install -e .

# Takes 2-3 minutes
```

**Verify:**

```bash
pip show agent_framework
```

## Step 4: Install Docker

Follow platform-specific instructions:

**WSL2:** Install Docker Desktop for Windows  
**macOS:** Install Docker Desktop or use Homebrew  
**Linux:** Use get-docker.sh script

See detailed instructions in collapsible sections in README.md

## Step 5: Start Database

```bash
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

## Step 7: Run Examples

```bash
# Simple agents
python examples/01_basic.py

# AI-powered agents  
python examples/02_llm_agent.py

# Document analysis
python examples/03_rag_agent.py
```

## Environment Comparison

| Feature | Conda | venv | System Python |
|---------|-------|------|---------------|
| Setup | Install Miniconda | Built-in | Already there |
| Commands | `conda activate` | `source venv/bin/activate` | None |
| Isolation | ✅ Excellent | ✅ Good | ❌ None |
| Package Mgmt | conda + pip | pip only | pip only |
| Multiple Projects | ✅ Easy | ✅ Easy | ❌ Conflicts |
| Disk Space | ~500MB | ~50MB per env | Minimal |
| **Best For** | Data science | Standard dev | Quick testing |

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
pip install -e .
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
pip install -e .

# ModuleNotFoundError
source venv/bin/activate  # Make sure activated!
pip install -e .
```

### System Python Issues

```bash
# Use python3 not python
python3 --version
alias python=python3

# Permission denied
pip install --user package-name

# Multiple Python versions
python3.11 --version
update-alternatives --config python3
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
git clone <repo-url>
cd AI-Agent-Builder
pip install -e .
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
pip install -e .
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
pip install -e .
cp .env.example .env
docker compose up -d postgres
sleep 10
python seed_data.py
python examples/01_basic.py
```

## Next Steps

- Read [CONFIGURATION.md](CONFIGURATION.md) for settings
- Read [LLM_CUSTOMIZATION.md](LLM_CUSTOMIZATION.md) for AI options
- Check [QUICK_REFERENCE.md](../QUICK_REFERENCE.md) for commands

---

**Remember:** Any environment works! Choose what you're comfortable with. 🚀
