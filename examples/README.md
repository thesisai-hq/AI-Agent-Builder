# AI Agent Examples - Learning Path

This directory contains example agents that teach investment analysis concepts progressively.

---

## ⚠️ **Best Practice: One Agent Per File**

Each `.py` file contains exactly ONE agent class for clarity and ease of use.

**Why:** Clear identity, easy testing, professional organization

See [Agent File Guidelines](../docs/AGENT_FILE_GUIDELINES.md) for details.

---

## 📚 **Learning Path (Start Here!)**

Follow these examples in order to learn the framework progressively:

### 1. **01_basic.py** - Rule-Based Agent ⭐ START HERE
```
Agent: ValueAgent
Type: Rule-Based
Dependencies: None (core framework only)
Time: 2 minutes
Difficulty: ★☆☆☆☆

What You Learn:
- Agent base class basics
- Working with financial data
- Simple if/then investment rules
- Signal objects (direction, confidence, reasoning)

Run: python 01_basic.py
```

### 2. **02_llm_agent.py** - LLM-Powered Agent ⭐⭐
```
Agent: QualityInvestorAgent  
Type: LLM-Powered
Dependencies: pip install ollama
Setup: ollama pull llama3.2
Time: 5 minutes
Difficulty: ★★☆☆☆

What You Learn:
- AI-powered analysis with LLMs
- System prompts for agent personality
- Temperature and max_tokens configuration
- Error handling with fallback logic
- Natural language reasoning

Run: python 02_llm_agent.py
```

### 3. **03_hybrid.py** - Hybrid Agent (Rules + LLM) ⭐⭐⭐
```
Agent: GrowthQualityHybrid
Type: Hybrid
Dependencies: pip install ollama
Setup: ollama pull llama3.2
Time: 7 minutes
Difficulty: ★★★☆☆

What You Learn:
- Two-stage analysis (screening + deep dive)
- Combining rules and AI for efficiency
- Resource optimization (speed + cost)
- When to use hybrid vs pure approaches

Run: python 03_hybrid.py
```

### 4. **04_rag_agent.py** - RAG Document Analysis ⭐⭐⭐⭐
```
Agent: SECFilingAnalyst
Type: RAG-Powered
Dependencies: pip install ollama sentence-transformers
Setup: ollama pull llama3.2
Time: 10 minutes
Difficulty: ★★★★☆

What You Learn:
- Document analysis with RAG
- Semantic search and embeddings
- Chunking long documents
- Combining retrieval with LLM synthesis

Run: python 04_rag_agent.py
```

---

## 🎓 **Learning Progression**

```
01_basic.py (Rules)
    ↓
    Learn: Basic agent structure
    ↓
02_llm_agent.py (AI)
    ↓
    Learn: LLM integration
    ↓
03_hybrid.py (Rules + AI)
    ↓
    Learn: Optimization strategies
    ↓
04_rag_agent.py (Documents + AI)
    ↓
    Learn: Advanced document analysis
    ↓
Ready to build your own! 🚀
```

---

## 🌟 **Famous Investor Strategies**

After completing the learning path, explore these strategy implementations:

### 5. **05_buffett_quality.py** - Warren Buffett Quality
```
Strategy: Score-based quality metrics
Focus: High ROE, strong margins, low debt
Difficulty: ★★☆☆☆
```

### 6. **06_lynch_garp.py** - Peter Lynch GARP
```
Strategy: Growth at Reasonable Price
Focus: PEG ratio, sustainable growth
Difficulty: ★★☆☆☆
```

### 7. **07_graham_value.py** - Benjamin Graham Value
```
Strategy: Deep value with margin of safety
Focus: Low PE, low PB, high dividend
Difficulty: ★★☆☆☆
```

---

## 🎯 **Quick Start**

### First Time?
```bash
# 1. Ensure database is running
cd ~/AI-Agent-Builder
docker compose up -d postgres
sleep 5

# 2. Seed sample data (if not done)
python seed_data.py

# 3. Run examples in order
python examples/01_basic.py          # Start here!
python examples/02_llm_agent.py      # Then AI
python examples/03_hybrid.py         # Then hybrid
python examples/04_rag_agent.py      # Then RAG
```

### Dependencies by Agent Type:

| Example | Core | LLM | RAG | Install Command |
|---------|------|-----|-----|-----------------|
| 01_basic.py | ✅ | ❌ | ❌ | `pip install -e .` |
| 02_llm_agent.py | ✅ | ✅ | ❌ | `pip install -e ".[llm]"` |
| 03_hybrid.py | ✅ | ✅ | ❌ | `pip install -e ".[llm]"` |
| 04_rag_agent.py | ✅ | ✅ | ✅ | `pip install -e ".[llm,rag]"` |
| 05-07 (strategies) | ✅ | ❌ | ❌ | `pip install -e .` |

**Recommendation:** Install everything at once:
```bash
pip install -e ".[all]"
```

---

## 📊 **Agent Type Comparison**

| Type | Example | Speed | Cost | Depth | Best For |
|------|---------|-------|------|-------|----------|
| **Rule-Based** | 01 | ⚡⚡⚡⚡⚡ | Free | ★☆☆☆☆ | Clear criteria, quick screening |
| **LLM-Powered** | 02 | ⚡⚡☆☆☆ | $ | ★★★★★ | Nuanced analysis, small datasets |
| **Hybrid** | 03 | ⚡⚡⚡⚡☆ | $ | ★★★★☆ | Large-scale + depth |
| **RAG-Powered** | 04 | ⚡☆☆☆☆ | $$ | ★★★★★ | Document analysis |

---

## 🔧 **Creating Your Own Agents**

### Option 1: Use the GUI (Easiest)
```bash
./gui/launch.sh
# Navigate to "➕ Create Agent"
# Build visually, no coding needed!
```

### Option 2: Duplicate an Example
```bash
# Copy an example that's close to what you want
cp 01_basic.py my_value_strategy.py

# Edit and customize
nano my_value_strategy.py

# Test it
python my_value_strategy.py
```

### Option 3: Write from Scratch
```python
"""My Custom Strategy"""

from agent_framework import Agent, Signal

class MyStrategy(Agent):
    """Your strategy description"""
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        # Your logic here
        return Signal('bullish', 0.8, 'Your reasoning')

# Add async main() for testing
```



---

## 🧪 **Testing Examples**

```bash
# Test each example
python 01_basic.py     # Fast, should work immediately
python 02_llm_agent.py  # Requires: ollama + llama3.2
python 03_hybrid.py     # Requires: ollama + llama3.2
python 04_rag_agent.py  # Requires: ollama + llama3.2 + sentence-transformers

# If LLM examples fail:
# 1. Install dependencies: pip install 'ai-agent-framework[llm,rag]'
# 2. Start Ollama: ollama serve
# 3. Pull model: ollama pull llama3.2
```

---

## 💡 **Tips**

### For Beginners:
1. **Start with 01_basic.py** - No dependencies, pure rules
2. **Then 02_llm_agent.py** - Add AI intelligence
3. **Skip to strategies** - Try Buffett, Lynch, Graham approaches
4. **Return to 03-04** when ready for advanced techniques

### For Experienced:
1. Jump to strategies (05-07) for implementation patterns
2. Review 03_hybrid.py for optimization techniques
3. Check 04_rag_agent.py for document analysis

### For Production:
- Rule-based: Ready to use
- LLM: Configure API keys in .env, add error handling
- Hybrid: Perfect for scale (screen → analyze workflow)
- RAG: Use vector database (pgvector) for production

---

## 📖 **Additional Resources**

- [Data Flow](../docs/DATA_FLOW.md) - How each example processes data ⭐
- [Multi-Agent Systems](../docs/MULTI_AGENT_SYSTEMS.md) - Combine examples together ⭐
- [Framework Documentation](../README.md) - Complete guide
- [Agent Guidelines](../docs/AGENT_FILE_GUIDELINES.md) - Best practices
- [Hybrid Agents](../docs/HYBRID_AGENTS.md) - Deep dive on hybrid
- [LLM Setup](../docs/LLM_CUSTOMIZATION.md) - AI configuration
- [Choosing Agent Type](../docs/CHOOSING_AGENT_TYPE.md) - Type comparison

---

## ✅ **Summary**

**Total Examples:** 7+ agents
**Learning Path:** 4 progressive examples (01-04)
**Strategy Examples:** 3 famous investor approaches (05-07)
**Organization:** One agent per file (clear, professional)

**Start here:** `python 01_basic.py` and progress through the examples! 🚀

**Having issues?** See [TROUBLESHOOTING.md](../docs/TROUBLESHOOTING.md)

---

## ⚖️ Disclaimer

**Educational use only.** Not financial advice. Do not use for real trading.

See [DISCLAIMER.md](../DISCLAIMER.md) for complete legal terms.

**For production systems:** [thesis-app](https://thesisai.app)

---

## 📜 License

MIT License - See [LICENSE](../LICENSE) for details.

Copyright (c) 2025 ThesisAI LLC
