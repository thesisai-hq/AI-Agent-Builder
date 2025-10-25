# Quick Reference - Copy-Paste Commands

All commands work on **WSL2, macOS, and Linux** with **conda, venv, or system Python**.

## Environment Activation

**Always activate your environment first!**

```bash
# If using conda:
conda activate agent-framework

# If using venv:
cd ~/AI-Agent-Builder && source venv/bin/activate

# If using system Python:
# (nothing to activate)
```

## Essential Daily Commands

### Start Work Session

**Conda:**
```bash
cd ~/AI-Agent-Builder
conda activate agent-framework
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

### Run Examples

```bash
# Simple agents (no AI)
python examples/01_basic.py

# AI-powered agents
python examples/02_llm_agent.py

# Document analysis
python examples/03_rag_agent.py

# Custom LLM settings
python examples/04_custom_llm_config.py
```

### End Work Session

**Conda:**
```bash
docker compose down
conda deactivate
```

**venv:**
```bash
docker compose down
deactivate
```

**System Python:**
```bash
docker compose down
```

## Environment Management

### Conda Commands

```bash
# Create environment
conda create -n agent-framework python=3.11 -y

# Activate
conda activate agent-framework

# Deactivate
conda deactivate

# List environments (shows active with *)
conda env list

# Install package with conda
conda install numpy pandas

# Install package with pip
pip install package-name

# Update all packages
conda update --all

# Export environment
conda env export > environment.yml
conda env export --no-builds > environment.yml  # Cross-platform

# Create from export
conda env create -f environment.yml

# Clone environment
conda create --name newenv --clone agent-framework

# Remove environment
conda deactivate
conda env remove -n agent-framework

# Clean cache
conda clean --all
```

### venv Commands

```bash
# Create environment
cd ~/AI-Agent-Builder
python3 -m venv venv

# Activate
source venv/bin/activate

# Deactivate
deactivate

# Check active environment
which python
# Should show: ~/AI-Agent-Builder/venv/bin/python

# Install package
pip install package-name

# Save dependencies
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt

# Upgrade pip
pip install --upgrade pip

# Remove environment
rm -rf venv

# Recreate
python3 -m venv venv
```

### System Python Commands

```bash
# Install package
pip install package-name

# Install for user only (safer)
pip install --user package-name

# List installed packages
pip list

# Show package info
pip show package-name

# Upgrade pip
pip install --upgrade pip
```

## Database Commands

### Start/Stop

```bash
# Start database
docker compose up -d postgres

# Stop database
docker compose down

# Restart
docker compose restart postgres

# View status
docker compose ps
docker ps

# Stop and delete all data (WARNING!)
docker compose down -v
```

### View Logs

```bash
# Last 50 lines
docker compose logs --tail=50 postgres

# Follow in real-time
docker compose logs -f postgres

# All logs
docker compose logs postgres
```

### Query Database

```bash
# Open psql shell
docker exec -it agent_framework_db psql -U postgres -d agent_framework

# Inside psql:
\dt                           # List tables
\d fundamentals               # Describe table
SELECT * FROM fundamentals;   # Query data
\q                            # Exit

# One-line queries
docker exec -it agent_framework_db psql -U postgres -d agent_framework -c "SELECT ticker, name FROM fundamentals;"

# Count records
docker exec -it agent_framework_db psql -U postgres -d agent_framework -c "SELECT COUNT(*) FROM prices;"
```

### Backup & Restore

```bash
# Create backup
docker exec agent_framework_db pg_dump -U postgres agent_framework > backup_$(date +%Y%m%d).sql

# List backups
ls -lh backup_*.sql

# Restore from backup
docker exec -i agent_framework_db psql -U postgres agent_framework < backup_20250124.sql

# Reset database completely
docker compose down -v
docker compose up -d postgres
sleep 10
python seed_data.py
```

## Python Commands

### Run Scripts

```bash
# Make sure environment is activated first!
# conda activate agent-framework  # if conda
# source venv/bin/activate        # if venv

# Run script
python my_agent.py

# Run with output saved to file
python my_agent.py > output.log 2>&1

# Run in background
python my_agent.py &

# Run and see output + save
python my_agent.py 2>&1 | tee output.log
```

### Package Management

**All Environments:**
```bash
# List installed packages
pip list

# Show package info
pip show agent_framework

# Install package
pip install package-name

# Uninstall package
pip uninstall package-name

# Upgrade package
pip install --upgrade package-name
```

**Conda-Specific:**
```bash
# Install with conda (preferred)
conda install numpy pandas matplotlib

# Search for package
conda search package-name

# Update package
conda update package-name

# List conda packages
conda list
```

**venv-Specific:**
```bash
# Save current packages
pip freeze > requirements.txt

# Install from file
pip install -r requirements.txt

# Upgrade all packages (careful!)
pip list --outdated
pip install --upgrade package1 package2
```

### Framework Installation

```bash
# Install framework
pip install -e .

# Reinstall after changes
pip install -e . --force-reinstall

# Install with extras
pip install -e ".[llm]"      # LLM support only
pip install -e ".[rag]"      # RAG support only
pip install -e ".[dev]"      # Development tools
pip install -e ".[all]"      # Everything

# Uninstall
pip uninstall agent_framework
```

## File Management

```bash
# Create file
touch my_agent.py
nano my_agent.py

# View file
cat my_agent.py
less my_agent.py  # Page through (press 'q' to quit)

# Copy file
cp examples/01_basic.py my_agent.py

# Move/rename
mv my_agent.py my_new_agent.py

# Delete
rm my_agent.py

# Search for files
find . -name "*.py"
find . -name "my_agent.py"

# Search in files
grep -r "def analyze" .
grep -r "Agent" --include="*.py" .
```

## Configuration

```bash
# Create .env from example
cp .env.example .env

# View settings
cat .env

# Edit settings
nano .env
# or
code .env  # VS Code
# or  
vim .env

# Check specific setting
grep DB_PORT .env
```

## Testing

### Setup Test Database

```bash
# One-time setup (environment should be activated)
python setup_test_db.py
```

### Run Tests

```bash
# Environment must be activated!
# conda activate agent-framework  # if conda
# source venv/bin/activate        # if venv

# All tests
pytest tests/ -v

# Specific test
pytest tests/test_framework.py::test_database -v

# With coverage
pytest tests/ --cov=agent_framework

# Generate HTML report
pytest tests/ --cov=agent_framework --cov-report=html
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux

# Install pytest if needed
pip install pytest pytest-asyncio pytest-cov
```

## Ollama (Free Local AI)

```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Download models
ollama pull llama3.2      # 4GB
ollama pull mistral       # 4GB
ollama pull phi           # 2GB

# List models
ollama list

# Test model
ollama run llama3.2 "Hello world"

# Remove model
ollama rm phi

# Check Ollama status
curl http://localhost:11434
```

## API Server

### Start API

```bash
# Activate environment first!
# conda activate agent-framework  # if conda
# source venv/bin/activate        # if venv

# Start server
uvicorn agent_framework.api:app --reload

# Start on specific port
uvicorn agent_framework.api:app --host 0.0.0.0 --port 8000

# Start in background
nohup uvicorn agent_framework.api:app > api.log 2>&1 &

# View log
tail -f api.log
```

### Stop API

```bash
# If running in terminal: Ctrl+C

# If running in background:
pkill -f uvicorn
```

### Test API

```bash
# Health check
curl http://localhost:8000/health

# Pretty print JSON
curl http://localhost:8000/health | python -m json.tool

# List tickers
curl http://localhost:8000/tickers

# Get ticker data
curl http://localhost:8000/tickers/AAPL
```

## Git Commands

```bash
# Check status
git status

# View changes
git diff

# Add files
git add .
git add my_agent.py

# Commit
git commit -m "Add my custom agent"

# Push
git push origin main

# Pull latest
git pull origin main

# Create branch
git checkout -b new-feature

# Switch branch
git checkout main
```

## Platform-Specific

### WSL2 (Windows)

```bash
# Access Windows files
cd /mnt/c/Users/YourName/Documents

# Open Windows Explorer
explorer.exe .

# Edit with Windows apps
notepad.exe my_agent.py
code my_agent.py

# Copy from Windows
cp /mnt/c/Users/YourName/file.txt .

# Check WSL version
wsl --version
```

### macOS

```bash
# Open Finder
open .

# Copy to clipboard
cat my_agent.py | pbcopy

# Paste from clipboard
pbpaste > new_file.py

# Open with default app
open my_agent.py
```

### Linux

```bash
# Open file manager
xdg-open .

# Copy to clipboard (requires xclip)
sudo apt install xclip
cat my_agent.py | xclip -selection clipboard
```

## Complete Workflows

### One-Time Setup

**Conda:**
```bash
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
```

**venv:**
```bash
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
```

**System Python:**
```bash
cd ~
git clone <repo-url>
cd AI-Agent-Builder
pip install -e .
cp .env.example .env
docker compose up -d postgres
sleep 10
python seed_data.py
```

### Daily Work

**Conda:**
```bash
cd ~/AI-Agent-Builder
conda activate agent-framework
docker compose up -d postgres
python my_agent.py
# ... work ...
docker compose down
conda deactivate
```

**venv:**
```bash
cd ~/AI-Agent-Builder
source venv/bin/activate
docker compose up -d postgres
python my_agent.py
# ... work ...
docker compose down
deactivate
```

**System Python:**
```bash
cd ~/AI-Agent-Builder
docker compose up -d postgres
python my_agent.py
# ... work ...
docker compose down
```

## Troubleshooting

### Environment Issues

```bash
# Check which Python you're using
which python
python --version

# Conda: Check active environment
conda env list
# Active environment has * next to it

# venv: Check activation
echo $VIRTUAL_ENV
# Should show: /home/.../AI-Agent-Builder/venv

# System: Check Python location
which python3
whereis python3
```

### Database Issues

```bash
# Check Docker is running
docker ps

# Database not found
docker exec -it agent_framework_db createdb -U postgres agent_framework
docker exec -i agent_framework_db psql -U postgres agent_framework < schema.sql

# No data
python seed_data.py

# Connection refused
docker compose restart postgres
sleep 10
```

### Module Issues

```bash
# Activate environment first!
# conda activate agent-framework
# source venv/bin/activate

# Then reinstall
pip install -e .

# Check installation
pip show agent_framework
```

### Port Issues

```bash
# Check what's using port
sudo lsof -i :5433

# Change port
nano .env
# Change: DB_PORT=5434

# Restart
docker compose down
docker compose up -d postgres
```

## Keyboard Shortcuts

### Terminal
```
Ctrl+C          Stop program
Ctrl+D          Exit shell
Ctrl+L          Clear screen
Ctrl+R          Search command history
Tab             Auto-complete
↑/↓             Previous/next command
```

### nano Editor
```
Ctrl+X          Exit
Ctrl+O          Save
Ctrl+K          Cut line
Ctrl+U          Paste
Ctrl+W          Search
```

## Environment-Specific Tips

### Conda Pro Tips

```bash
# Create environment with specific packages
conda create -n agent-framework python=3.11 numpy pandas -y

# Install from conda-forge (more packages)
conda install -c conda-forge package-name

# Update conda itself
conda update conda

# List what's installed
conda list

# Search for packages
conda search package-name
```

### venv Pro Tips

```bash
# Use specific Python version
python3.11 -m venv venv

# Upgrade pip in venv
source venv/bin/activate
pip install --upgrade pip

# Create multiple environments
python3 -m venv ~/envs/project1
python3 -m venv ~/envs/project2

# Activate different projects
source ~/envs/project1/bin/activate
source ~/envs/project2/bin/activate
```

### System Python Pro Tips

```bash
# Use --user flag to avoid permissions
pip install --user package-name

# Check user install location
python -m site --user-site

# Create alias for python3
echo 'alias python=python3' >> ~/.bashrc
source ~/.bashrc
```

## Quick Troubleshooting

```bash
# Environment not activated
# Conda:
conda activate agent-framework

# venv:
cd ~/AI-Agent-Builder && source venv/bin/activate

# Wrong environment
# Conda:
conda deactivate
conda activate agent-framework

# venv:
deactivate
source venv/bin/activate

# Module not found
pip install -e .

# Database not running
docker compose up -d postgres

# Port conflict
nano .env  # Change DB_PORT

# Check everything
python --version
pip show agent_framework
docker ps
```

## Advanced Commands

### Export/Share Environment

**Conda:**
```bash
# Export for same OS
conda env export > environment.yml

# Export cross-platform (no builds)
conda env export --no-builds > environment.yml

# Export minimal (only explicitly installed)
conda env export --from-history > environment.yml

# Share with others
git add environment.yml
git commit -m "Add conda environment"

# Others can recreate
conda env create -f environment.yml
```

**venv:**
```bash
# Export requirements
pip freeze > requirements.txt

# Share
git add requirements.txt
git commit -m "Add requirements"

# Others can install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Multiple Environments

**Conda:**
```bash
# Create multiple environments
conda create -n project1 python=3.11 -y
conda create -n project2 python=3.10 -y
conda create -n testing python=3.12 -y

# Switch between them
conda activate project1
conda activate project2
conda activate testing

# List all
conda env list
```

**venv:**
```bash
# Create in different locations
python3 -m venv ~/envs/project1
python3 -m venv ~/envs/project2

# Activate different projects
source ~/envs/project1/bin/activate
source ~/envs/project2/bin/activate
```

## System Information

```bash
# Python version
python --version

# Pip version
pip --version

# Environment info (conda)
conda info

# Environment info (venv)
which python
echo $VIRTUAL_ENV

# Docker version
docker --version
docker compose version

# System info
uname -a

# Disk space
df -h

# Memory
free -h
```

## Process Management

```bash
# List Python processes
ps aux | grep python

# Kill process by name
pkill -f "python my_agent.py"

# Kill by PID
kill 12345

# Background processes
jobs

# Bring to foreground
fg

# Send to background
bg
```

## Need More Help?

```bash
# Read docs
cat docs/GETTING_STARTED.md | less

# Search docs
grep -r "conda" docs/

# Command help
conda --help
python --help
docker --help
```

---

**Pro Tip:** Choose one environment method and stick with it. Don't mix them in the same project! 🎯
