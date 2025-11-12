# Agent Management - Complete Guide

## Overview

The Browse Agents page now includes full agent management capabilities:
- 🔍 **Search/Filter** agents
- 👁️ **View** agent code
- 📋 **Duplicate** agents
- ⬇️ **Export** agents
- 🗑️ **Delete** custom agents
- 📊 **Statistics** dashboard

## Features

### 1. Statistics Dashboard

At the top of Browse page:
```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Total Agents │ Rule-Based   │ LLM/RAG      │ Your Agents  │
│      12      │      5       │      4       │      8       │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

Shows at a glance:
- Total number of agents
- Breakdown by type
- How many you created vs framework examples

### 2. Search/Filter

```
🔍 Search agents: [type to filter...]
```

**Searches:**
- Agent names (e.g., "Value")
- Filenames (e.g., "custom")
- Real-time filtering

**Example:**
- Type "value" → Shows ValueAgent, CustomValueAgent
- Type "llm" → Shows all LLM-powered agents
- Type "my" → Shows my_agent.py, my_strategy.py

### 3. View Code

**Button:** 👁️ View

**Shows:**
- Complete agent source code
- Syntax highlighted
- Scrollable preview

**Use for:**
- Learning from examples
- Understanding implementation
- Debugging

### 4. Duplicate Agent

**Button:** 📋 Copy

**Workflow:**
1. Click "Copy" on any agent
2. Enter new filename (auto-suggests: `original_copy.py`)
3. Click "Duplicate" or "Cancel"
4. New agent created with updated class name

**What it does:**
- Copies all code
- Automatically renames class to match new filename
- Preserves all logic and configuration
- Creates independent copy (changes don't affect original)

**Use cases:**
- Create variations of working agents
- Test different parameters
- Build on existing strategies

**Example:**
```
Original: value_agent.py → class ValueAgent
Duplicate: value_agent_v2.py → class ValueAgentV2

All references updated automatically!
```

### 5. Export Agent

**Button:** ⬇️ Export

**Functionality:**
- Downloads agent file to your computer
- Original filename preserved
- Can import to other projects
- Share with collaborators

**Use for:**
- Backup agents
- Share strategies
- Move to other systems
- Version control outside Git

### 6. Delete Agent

**Button:** 🗑️ Delete (or 🔒 Protected for framework examples)

**Safety features:**
- ⚠️ Confirmation required
- Cannot delete framework examples (01_*.py, 02_*.py, etc.)
- Shows warning before deletion
- Immediate visual feedback

**Workflow:**
1. Click "Delete" on custom agent
2. Confirmation dialog appears
3. Click "Confirm Delete" or "Cancel"
4. If confirmed, agent is permanently removed

**Protected agents:**
- 01_basic.py → 🔒 Protected
- 02_llm_agent.py → 🔒 Protected
- 03_rag_agent.py → 🔒 Protected
- 04_custom_llm_config.py → 🔒 Protected

**Your agents:**
- my_agent.py → 🗑️ Delete (available)
- custom_strategy.py → 🗑️ Delete (available)

## Complete Workflow Examples

### Example 1: Iterate on a Strategy

```
1. Create "value_agent.py" with PE < 15
2. Test it → too aggressive
3. Browse → Duplicate to "value_agent_v2.py"
4. Edit v2 → Change to PE < 18
5. Test both → compare results
6. Keep better version, delete other
```

### Example 2: Share with Team

```
1. Create sophisticated agent
2. Test thoroughly
3. Browse → Export agent
4. Share .py file with team
5. They import to their examples/ directory
6. Everyone uses same strategy
```

### Example 3: Clean Up Old Experiments

```
1. Browse agents
2. Search "test" → finds all test agents
3. Delete experimental agents one by one
4. Keep only production-ready agents
```

### Example 4: Build Agent Family

```
1. Create base "momentum_agent.py"
2. Duplicate to "momentum_aggressive.py"
3. Duplicate to "momentum_conservative.py"
4. Tweak thresholds in each
5. Test all three
6. Use different ones for different market conditions
```

## UI Layout

```
╔══════════════════════════════════════════════╗
║  Browse Existing Agents                      ║
╠══════════════════════════════════════════════╣
║  ┌─────┬─────┬─────┬─────┐                  ║
║  │Total│Rule │LLM/ │Your │                  ║
║  │  12 │  5  │  4  │  8  │                  ║
║  └─────┴─────┴─────┴─────┘                  ║
║  ─────────────────────────────────────────   ║
║  🔍 Search: [____________]                   ║
║  Showing 12 agent(s)                         ║
║                                              ║
║  ┌──────────────────────────────────────┐   ║
║  │ ▼ ValueAgent                         │   ║
║  │   File: value_agent.py               │   ║
║  │   Type: Rule-Based                   │   ║
║  │   ┌────┬────┬────┬────┐              │   ║
║  │   │👁️ │📋  │⬇️  │🗑️ │              │   ║
║  │   │View│Copy│Exp.│Del.│              │   ║
║  │   └────┴────┴────┴────┘              │   ║
║  └──────────────────────────────────────┘   ║
╚══════════════════════════════════════════════╝
```

## Keyboard Shortcuts

While in Browse page:
- Type in search box → Filter immediately
- Expand agent → Click anywhere in header
- Click button → Immediate action
- ESC → Close expanded agent

## Best Practices

### Naming Convention

**Good:**
- `value_agent.py` → Clear purpose
- `growth_screening.py` → Descriptive
- `quality_v2.py` → Versioned

**Bad:**
- `agent1.py` → Generic
- `test.py` → Not descriptive
- `asdf.py` → Meaningless

### Organization

**Strategy 1: Version Control**
```
momentum_agent.py
momentum_agent_v2.py
momentum_agent_v3.py
momentum_agent_final.py
```

**Strategy 2: Categorization**
```
value_low_pe.py
value_dividend.py
growth_high_margin.py
growth_explosive.py
```

**Strategy 3: Purpose-Based**
```
screening_quality.py
screening_value.py
screening_growth.py
analysis_fundamental.py
```

### When to Delete

✅ **Delete:**
- Experimental agents that didn't work
- Outdated versions after creating v2
- Duplicate strategies
- Test agents

❌ **Keep:**
- Production agents
- Framework examples (protected anyway)
- Agents used in thesis-ai
- Successful strategies

## Security

### Protected Files

Framework examples are **automatically protected**:
- Cannot be deleted
- Shows 🔒 Protected button
- Prevents accidental removal of learning materials

**Detection:**
```python
# Files starting with '0' are protected
01_basic.py ← Protected
02_llm_agent.py ← Protected
my_agent.py ← Can delete
```

### Confirmation Required

**Every delete action requires:**
1. Click "Delete" button
2. Read warning message
3. Click "Confirm Delete"

**No accidental deletions!**

## Advanced Features

### Bulk Export (Future)

Not yet implemented, but planned:
- Select multiple agents
- Export as ZIP
- Share entire strategy library

### Import Agents (Future)

Not yet implemented, but planned:
- Drag-and-drop .py files
- Automatic validation
- Conflict resolution

### Version Control (Future)

Not yet implemented, but planned:
- Track changes over time
- Revert to previous versions
- Compare versions

## Technical Details

### Duplicate Logic

```python
# 1. Read source file
code = read_file('value_agent.py')

# 2. Extract class name
class ValueAgent(Agent):  # Found

# 3. Generate new class name from filename
value_agent_v2.py → ValueAgentV2

# 4. Replace in code
class ValueAgent → class ValueAgentV2
ValueAgent() → ValueAgentV2()

# 5. Save as new file
```

### Delete Safety

```python
# Check if protected
if filename.startswith('0'):
    return False, "Cannot delete framework examples"

# Check if exists
if not file_exists:
    return False, "File not found"

# Delete
file.unlink()  # Permanent removal
```

## Files Changed

1. ✅ `gui/agent_loader.py` - Added `delete_agent()` and `duplicate_agent()`
2. ✅ `gui/app.py` - Enhanced Browse page with all management features
3. ✅ `gui/AGENT_MANAGEMENT.md` - This complete guide

## Summary

**Browse page now includes:**
- ✅ Statistics dashboard
- ✅ Search/filter
- ✅ View code
- ✅ Duplicate agents
- ✅ Export agents
- ✅ Delete agents (with protection)
- ✅ Confirmation dialogs

**Student workflow:**
```
Create → Test → Iterate → Manage → Deploy
```

**All visual, all safe, all simple!**

---

**Status:** Implemented ✅  
**Version:** 1.3.0  
**Date:** 2025-01-23
