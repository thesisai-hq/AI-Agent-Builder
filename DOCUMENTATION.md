# Documentation Structure

Clean, user-focused documentation for AI-Agent-Builder GUI.

## User Documentation

### Main Directory (`~/AI-Agent-Builder/`)

**README.md** - Framework overview
- Installation options
- Quick examples
- GUI overview
- Project structure
- Common commands

**GUI_QUICK_START.md** - GUI quick start (5 min)
- Setup & launch
- Create first agent
- Test agent
- Integration guide

**QUICK_START.md** - Framework quick start (5 min)
- Installation
- Database setup
- Run examples

### GUI Directory (`~/AI-Agent-Builder/gui/`)

**README.md** - Complete GUI documentation
- Features
- Usage guide
- Agent types
- Testing
- Integration
- Troubleshooting
- Tips & best practices

### Docs Directory (`~/AI-Agent-Builder/docs/`)

Framework documentation:
- GETTING_STARTED.md
- CONFIGURATION.md
- DATABASE_SETUP.md
- LLM_CUSTOMIZATION.md
- PROJECT_STRUCTURE.md

### thesis-ai Integration

**thesis-ai/server/multi_agent_system/README.md**
- Multi-agent system overview
- Setup instructions
- Custom agent integration (NEW section)
- API reference

## Internal Files (To Remove)

Run cleanup to remove these internal development documents:

```bash
cd ~/AI-Agent-Builder/gui
./cleanup_docs.sh
```

**Files removed:**
- IMPLEMENTATION.md (technical implementation details)
- FIX_SUMMARY.md (bug fix notes)
- PROJECT_SUMMARY.md (project status)
- USAGE_GUIDE.md (redundant with README.md)
- TROUBLESHOOTING.md (merged into README.md)
- QUICK_REFERENCE.md (merged into README.md)
- CLEANUP.md (this file, after reading)

## Documentation Philosophy

**Keep:**
- User-facing guides
- Quick starts
- Essential references
- Integration examples

**Remove:**
- Internal development notes
- Detailed implementation docs
- Redundant information
- Status updates

## Quick Reference

### Setup & Launch
```bash
# Framework
cd ~/AI-Agent-Builder
pip install -e .

# GUI
./gui/setup.sh
./gui/launch.sh
```

### Documentation Locations
```bash
# Main overview
cat README.md

# GUI quick start
cat GUI_QUICK_START.md

# Complete GUI guide
cat gui/README.md

# Framework details
ls docs/
```

### Creating Agents
```bash
# Visual (no coding)
./gui/launch.sh

# Code (manual)
vim examples/my_agent.py
```

### Integration
```python
# In thesis-ai
from AI-Agent-Builder.examples.my_agent import MyAgent
agent = MyAgent()
```

## What's Where

| Topic | Document |
|-------|----------|
| Framework overview | README.md |
| GUI overview | GUI_QUICK_START.md |
| GUI complete guide | gui/README.md |
| Framework setup | QUICK_START.md |
| Database | docs/DATABASE_SETUP.md |
| LLM config | docs/LLM_CUSTOMIZATION.md |
| Integration | gui/README.md + thesis-ai/...README.md |

---

**After cleanup, run:**
```bash
# Remove this file too
rm ~/AI-Agent-Builder/gui/CLEANUP.md
rm ~/AI-Agent-Builder/gui/cleanup_docs.sh
```

**Documentation is now clean and user-focused!**
