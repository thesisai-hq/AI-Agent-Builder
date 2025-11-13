# Choosing the Right Agent Type

This guide helps you choose between Rule-Based, LLM-Powered, Hybrid, and RAG-Powered agents.

---

## 🎯 **Quick Decision Guide**

### Choose Rule-Based if:
- ✅ You have clear investment criteria (PE < 15, Growth > 20%)
- ✅ Need fast execution (milliseconds)
- ✅ Analyzing large numbers of stocks (thousands)
- ✅ Want deterministic results (same input = same output)
- ✅ No LLM dependencies or costs

**Example:** Screening 3,000 stocks for PE < 15 and dividend > 3%

### Choose LLM-Powered if:
- ✅ Need nuanced, contextual analysis
- ✅ Analyzing small numbers of stocks (< 20)
- ✅ Want natural language reasoning
- ✅ Criteria are complex or subjective
- ✅ Quality matters more than speed

**Example:** Deep analysis of 5 top portfolio candidates

### Choose Hybrid if:
- ✅ Analyzing large numbers of stocks (100-1000+)
- ✅ Need both screening and deep analysis
- ✅ Want to optimize LLM costs (95% reduction)
- ✅ Need speed + intelligence
- ✅ Production workflows at scale

**Example:** Screen S&P 500 → Analyze top 25 candidates

### Choose RAG-Powered if:
- ✅ Analyzing documents (SEC filings, reports, news)
- ✅ Documents are too long for LLM context (50+ pages)
- ✅ Need to extract specific information
- ✅ Want semantic search capabilities
- ✅ Processing PDFs or unstructured text

**Example:** Analyze quarterly 10-Q filings for risk factors

---

## 📊 **Detailed Comparison**

| Feature | Rule-Based | LLM-Powered | Hybrid | RAG-Powered |
|---------|------------|-------------|--------|-------------|
| **Speed** | ⚡⚡⚡⚡⚡ | ⚡⚡☆☆☆ | ⚡⚡⚡⚡☆ | ⚡☆☆☆☆ |
| **Cost** | Free | $$$ | $ | $$$ |
| **Depth** | Surface | Deep | Deep (filtered) | Very Deep |
| **Dependencies** | None | LLM | LLM | LLM + RAG |
| **Setup** | None | API/Model | API/Model | API/Model + Embeddings |
| **Deterministic** | ✅ Yes | ❌ No | ⚠️ Partial | ❌ No |
| **Context Aware** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| **Document Analysis** | ❌ No | ⚠️ Limited | ⚠️ Limited | ✅ Yes |
| **Natural Language** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |

---

## 🎓 **Use Case Examples**

### Use Case 1: Daily Market Screening
```
Goal: Screen 500 stocks every morning for opportunities

❌ Pure LLM: 500 calls × 3 sec = 25 min, $5.00
✅ Rule-Based: 500 checks × 0.001 sec = 0.5 sec, $0
✅ Hybrid: Filter to 20 → LLM on 20 = 1 min, $0.20

Winner: Rule-Based for pure screening, Hybrid if need depth
```

### Use Case 2: Portfolio Deep Dive
```
Goal: Thorough analysis of 10 portfolio stocks

❌ Rule-Based: Too simplistic, misses nuances
✅ LLM-Powered: 10 calls × 3 sec = 30 sec, $0.10, deep insights

Winner: LLM-Powered (small number, need depth)
```

### Use Case 3: Quarterly Earnings Review
```
Goal: Analyze 10-Q filings (50 pages each) for 10 companies

❌ Rule-Based: Can't read documents
❌ LLM-Powered: Context limit (filings too long)
✅ RAG-Powered: Chunks → Search → Analyze

Winner: RAG-Powered (document analysis)
```

### Use Case 4: Sector Rotation
```
Goal: Analyze all tech stocks (200) → Pick top 10

❌ Rule-Based: Misses quality nuances
❌ LLM-Powered: 200 calls = expensive
✅ Hybrid: Rules filter to 30 → LLM picks top 10

Winner: Hybrid (scale + intelligence)
```

---

## ⚡ **Performance Comparison**

### Scenario: Analyze 500 Stocks

| Metric | Rule-Based | LLM-Powered | Hybrid | RAG-Powered |
|--------|------------|-------------|--------|-------------|
| **Time** | 1 sec | 25 min | 90 sec | N/A |
| **Cost** | $0 | $5.00 | $0.25 | N/A |
| **Depth** | ★☆☆☆☆ | ★★★★★ | ★★★★☆ | N/A |
| **Actionable** | 500 signals | 500 insights | 25 deep + 475 filtered | N/A |

**Winner for Scale:** Hybrid (95% cost reduction, same depth on candidates)

---

## 🔧 **Decision Tree**

```
Start: What are you analyzing?
    |
    ├─ Documents (PDFs, filings)? 
    |     └─→ Use RAG-Powered
    |
    ├─ How many stocks?
          |
          ├─ Small (< 20)
          |     |
          |     ├─ Need depth? → LLM-Powered
          |     └─ Simple criteria? → Rule-Based
          |
          └─ Large (100+)
                |
                ├─ Just screening? → Rule-Based
                ├─ Need some depth? → Hybrid
                └─ Need all deep? → LLM-Powered (expensive!)
```

---

## 💰 **Cost Optimization**

### Daily Screening (500 stocks):

**Pure LLM (Expensive):**
```
500 stocks × $0.01 per call = $5/day
$5/day × 250 trading days = $1,250/year
```

**Hybrid (Smart):**
```
Rules filter 95% → 25 stocks need LLM
25 stocks × $0.01 = $0.25/day
$0.25/day × 250 days = $62.50/year

Savings: $1,187.50/year (95% reduction!)
```

**Rule-Based (Free):**
```
$0/day × 250 days = $0/year

Trade-off: Less intelligent, but free
```

---

## 🎯 **Framework Recommendations**

### For Beginners:
```
1. Start with Rule-Based (01_basic.py)
   - No dependencies
   - Easy to understand
   - See results immediately

2. Try LLM-Powered (02_llm_agent.py)
   - See AI intelligence
   - Understand LLM configuration
   - Compare to rules

3. Explore Hybrid (03_hybrid.py)
   - Best of both worlds
   - Learn optimization
   - See real-world pattern
```

### For Production:
```
Small scale (< 50 stocks/day):
  → LLM-Powered (depth matters more than cost)

Medium scale (50-500 stocks/day):
  → Hybrid (balance of speed, cost, depth)

Large scale (1000+ stocks/day):
  → Rule-Based + Hybrid
  → Rules for broad screening
  → Hybrid for sector-specific deep dives

Document analysis:
  → RAG-Powered (SEC filings, reports, news)
```

### For thesis-app Integration:
```
Use case: Multi-agent investment advisor

Recommended mix:
├── Rule-Based (Fast screening across universe)
├── Hybrid (Sector-specific analysis)
├── LLM-Powered (Final recommendation synthesis)
└── RAG-Powered (Document insights when available)

Why this mix?
- Rules handle scale (screen 1000s)
- Hybrid provides depth efficiently
- LLM synthesizes final decision
- RAG adds document intelligence
```

---

## 📈 **Real-World Patterns**

### Pattern 1: Funnel Approach
```
Stage 1: Rule-Based (screen 3000 → 100)
  ↓
Stage 2: Hybrid (analyze 100 → 20)
  ↓
Stage 3: LLM-Powered (deep dive on 20 → top 5)
  ↓
Result: 5 high-quality picks
```

### Pattern 2: Specialized Agents
```
Valuation: Rule-Based (PE, PB, etc.)
Growth: Hybrid (screen + quality check)
Sentiment: LLM-Powered (news analysis)
Risk: RAG-Powered (filing analysis)

Combine all signals for final decision
```

### Pattern 3: Market Regime
```
Bull Market: Hybrid (growth screening + quality)
Bear Market: Rule-Based (strict value criteria)
Sideways: LLM-Powered (nuanced opportunities)
```

---

## ⚙️ **Configuration Tips**

### Rule-Based:
```python
# Keep rules simple and clear
if pe < 15 and dividend > 2:
    return bullish

# Avoid over-optimization
# Don't: if pe == 14.73 and dividend == 2.51
```

### LLM-Powered:
```python
# Use low temperature for consistency
temperature=0.3  # Conservative analysis

# Use high temperature for creativity
temperature=0.8  # Growth/speculation

# Clear system prompts
system_prompt="You are Warren Buffett. Focus on quality..."
```

### Hybrid:
```python
# Rules should filter 80-95% of stocks
if growth > 15 and margin > 10:  # ~10% pass
    return llm_analysis()

# Don't filter too much (< 5% pass = missing opportunities)
# Don't filter too little (> 20% pass = too many LLM calls)
```

### RAG-Powered:
```python
# Smaller chunks for precise search
chunk_size=300  # Good for specific facts

# Larger chunks for context
chunk_size=500  # Good for understanding themes

# More chunks for comprehensive analysis
top_k=5  # Retrieve top 5 most relevant chunks
```

---

## 🚀 **Getting Started**

### Try Each Type:
```bash
# 1. Rule-Based (no dependencies)
python examples/01_basic.py

# 2. LLM-Powered (install: pip install ollama)
ollama pull llama3.2
python examples/02_llm_agent.py

# 3. Hybrid (same deps as LLM)
python examples/03_hybrid.py

# 4. RAG-Powered (install: pip install sentence-transformers)
python examples/04_rag_agent.py
```

### Or Use GUI:
```bash
./gui/launch.sh
# Create agents visually
# Try different types
# See what works for your use case
```

---

## ✅ **Summary**

**Choose Based On:**

| Your Need | Agent Type |
|-----------|-----------|
| Speed + Scale | Rule-Based |
| Depth + Intelligence | LLM-Powered |
| Speed + Depth + Scale | Hybrid |
| Document Analysis | RAG-Powered |

**Framework Recommendation:**
- **Learning:** Try all 4 types (01 → 02 → 03 → 04)
- **Production:** Mix types based on use case
- **Optimization:** Start Rule-Based, add intelligence where needed

**Remember:** No single type is "best" - choose based on your specific requirements!

---

See also:
- [Hybrid Agents Explained](HYBRID_AGENTS.md) - Deep dive on hybrid
- [LLM Customization](LLM_CUSTOMIZATION.md) - AI configuration
- [Examples Guide](../examples/README.md) - Try all types
