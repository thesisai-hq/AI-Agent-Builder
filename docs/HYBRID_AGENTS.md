# Hybrid Agents Explained

**What:** Combines rule-based screening with LLM-powered analysis  
**Why:** Best of both worlds - speed + intelligence  
**When:** Analyzing large sets of stocks where you need both filtering and deep insights

---

## 🎯 **The Four Agent Types**

### 1. **Rule-Based** 🎲
```python
def analyze(ticker, data):
    if PE < 15:
        return Signal('bullish', 0.8, 'Undervalued')
    else:
        return Signal('neutral', 0.5, 'Fair value')
```

**Pros:**
- ✅ Very fast (milliseconds)
- ✅ Deterministic (same input = same output)
- ✅ No LLM costs
- ✅ Easy to understand

**Cons:**
- ❌ No nuanced analysis
- ❌ Can't consider context
- ❌ Rigid logic

**Use when:** Clear rules, need speed, analyzing many stocks

---

### 2. **LLM-Powered** 🤖
```python
def analyze(ticker, data):
    prompt = f"Analyze {ticker}: {fundamentals}"
    response = llm.chat(prompt)
    return parse_llm_signal(response)
```

**Pros:**
- ✅ Nuanced analysis
- ✅ Considers context
- ✅ Natural language reasoning
- ✅ Adapts to complex situations

**Cons:**
- ❌ Slower (seconds per stock)
- ❌ Costs money (API calls)
- ❌ Non-deterministic (varies slightly)
- ❌ Requires LLM setup

**Use when:** Deep analysis needed, small number of stocks, context matters

---

### 3. **Hybrid** ⚡ (Rules + LLM)
```python
def analyze(ticker, data):
    # Step 1: Fast screening with rules
    if PE < 20 and Growth > 10:
        # Passed screening!
        # Step 2: Deep LLM analysis
        return llm_analysis(ticker, data)
    else:
        # Didn't pass - skip LLM
        return Signal('neutral', 0.5, 'Did not pass screening')
```

**Pros:**
- ✅ Fast screening (rules filter 95% of stocks)
- ✅ Deep analysis (LLM on the 5% that matter)
- ✅ Cost-effective (fewer LLM calls)
- ✅ Best of both worlds

**Cons:**
- ⚠️ More complex to configure
- ⚠️ Two-step logic to understand
- ⚠️ Still requires LLM setup

**Use when:** Analyzing large universe of stocks (e.g., screen S&P 500, analyze top 20)

---

### 4. **RAG-Powered** 📄
```python
async def analyze_async(ticker, document_text):
    # Extract insights from documents (10-Ks, news, etc.)
    chunks = rag.add_document(document_text)
    context = rag.query("What are the key risks?")
    return llm.chat(query, context)
```

**Pros:**
- ✅ Analyzes documents (PDFs, 10-Ks, news)
- ✅ Extracts relevant sections
- ✅ Contextual understanding

**Cons:**
- ❌ Requires documents
- ❌ More complex setup
- ❌ Slower processing

**Use when:** Have documents to analyze (earnings reports, SEC filings)

---

## ⚡ **Hybrid Agent Deep Dive**

### Real-World Example:

**Scenario:** You want to analyze the entire S&P 500 (500 stocks)

**Pure LLM Approach:**
```python
for ticker in sp500:  # 500 stocks
    signal = llm.chat(f"Analyze {ticker}")  # 500 LLM calls!
    
# Result:
# - Time: 500 calls × 3 seconds = 25 minutes!
# - Cost: 500 calls × $0.01 = $5.00
# - Too slow and expensive!
```

**Pure Rules Approach:**
```python
for ticker in sp500:  # 500 stocks
    if PE < 15:
        signal = Signal('bullish', ...)  # Simple logic
    
# Result:
# - Time: 500 checks × 0.001s = 0.5 seconds ✅
# - Cost: $0 ✅
# - But: No nuanced analysis, might miss opportunities ❌
```

**Hybrid Approach:**
```python
for ticker in sp500:  # 500 stocks
    # Step 1: Fast filter
    if PE < 20 and Growth > 10:  # Only 25 stocks pass!
        # Step 2: Deep analysis on candidates
        signal = llm.chat(f"Analyze {ticker}")  # 25 LLM calls
    else:
        signal = Signal('neutral', 0.5, 'Screening failed')

# Result:
# - Time: Fast filter + 25 LLM calls = 90 seconds ✅
# - Cost: 25 calls × $0.01 = $0.25 ✅
# - Analysis: Deep LLM insights on filtered candidates ✅
# - Best of both worlds!
```

---

## 🔧 **How Hybrid Agents Work**

### Architecture:
```
Stock Data
    ↓
[Rule-Based Filter]
    ↓
  Pass? ──NO→ Return neutral
    ↓YES
[LLM Analysis]
    ↓
Return detailed signal
```

### Code Flow:
```python
class HybridAgent(Agent):
    def analyze(self, ticker, data):
        # Step 1: Apply rules (FAST)
        if self._passes_screening(data):
            # Step 2: LLM analysis (SLOW but only on candidates)
            return self._llm_analysis(ticker, data)
        else:
            # Skip LLM - didn't pass screening
            return Signal('neutral', 0.5, 'Did not meet criteria')
    
    def _passes_screening(self, data):
        """Fast rule-based filter"""
        pe = data.get('pe_ratio', 0)
        growth = data.get('revenue_growth', 0)
        return pe < 20 and growth > 10
    
    def _llm_analysis(self, ticker, data):
        """Deep LLM analysis"""
        prompt = f"Detailed analysis of {ticker}..."
        response = self.llm.chat(prompt)
        return parse_llm_signal(response)
```

---

## 🎨 **Updated GUI for Hybrid Agents**

### What You'll See Now:

```
Agent Type: [Hybrid ▼]

🧑‍💻 What is a Hybrid Agent?

Combines rules + LLM:
1. Rules: Fast screening (filter stocks)
2. LLM: Deep analysis (only on filtered stocks)

Use when: You want to screen thousands of stocks quickly,
then use AI for detailed analysis on candidates.

┌─────────────────────────────────────────┐
│ LLM Configuration                       │
│ Provider: [ollama ▼]                    │
│ Temperature: [0.5 ━━━━━●━━━]            │
│ Max Tokens: [1000]                      │
│ System Prompt: [_______________]        │
└─────────────────────────────────────────┘

🎯 Screening Rules (Step 1: Filter Stocks)
Define rules to filter which stocks get LLM analysis

Rule Style: ● Simple Rules ○ Advanced ○ Score-Based

┌─────────────────────────────────────────┐
│ Rule 1:                                 │
│ Metric: [pe_ratio ▼]                    │
│ Operator: [< ▼]                         │
│ Threshold: [20]                         │
│ (If this passes → LLM analyzes)         │
└─────────────────────────────────────────┘

[Generate Code]
```

### Generated Code Example:

```python
class HybridValueAgent(Agent):
    """Screens for value stocks, then uses LLM for detailed analysis"""
    
    def analyze(self, ticker, data):
        # Step 1: Rule-based screening
        if data.get('pe_ratio', 0) < 20:
            # Passed screening! Use LLM for deep analysis
            return self._llm_analysis(ticker, data)
        
        # Didn't pass - return neutral
        return Signal('neutral', 0.5, 'Did not pass screening')
    
    def _llm_analysis(self, ticker, data):
        """LLM provides detailed reasoning"""
        prompt = f"Analyze {ticker}: {fundamentals}"
        response = self.llm.chat(prompt)
        return parse_llm_signal(response)
```

---

## 📊 **Comparison Table**

| Feature | Rule-Based | LLM-Powered | **Hybrid** | RAG-Powered |
|---------|------------|-------------|------------|-------------|
| **Speed** | ⚡ Very Fast | 🐌 Slow | ⚡🐌 Fast filter + Slow analysis | 🐌 Slow |
| **Cost** | Free | $$$ | $ (fewer calls) | $$$ |
| **Depth** | Surface | Deep | Deep (filtered) | Very Deep |
| **Rules** | Yes | No | **Yes (filter)** | No |
| **LLM** | No | Yes | **Yes (analysis)** | Yes |
| **Best For** | Speed | Depth | **Scale** | Documents |

**Hybrid Advantage:** Analyze 500 stocks at the cost of analyzing 25!

---

## 🎓 **When to Use Each Type**

### Scenarios:

#### Scenario 1: Daily Screening
```
Analyze 500 stocks every day

✅ Use Hybrid:
- Rules: Filter to 20 value candidates (fast)
- LLM: Deep analysis on those 20 (smart)
- Time: Minutes instead of hours
- Cost: $0.20 instead of $5.00
```

#### Scenario 2: One Stock Deep Dive
```
Deep analysis of one company (AAPL)

✅ Use LLM-Powered:
- No screening needed (just one stock)
- Want maximum depth
- Cost doesn't matter ($0.01)
```

#### Scenario 3: Portfolio Check
```
Check my 10-stock portfolio

✅ Use Rule-Based:
- Small number of stocks
- Just want quick signals
- No LLM cost needed
```

#### Scenario 4: Earnings Report
```
Analyze 10-K SEC filing (50 pages)

✅ Use RAG-Powered:
- Document analysis needed
- Extract specific insights
- Contextual understanding
```

---

## 💡 **Hybrid Agent Design Patterns**

### Pattern 1: Value Screening
```python
# Rule: Screen for undervalued
if PE < 15 and Dividend > 2%:
    # LLM: Check if it's a value trap
    llm.chat("Is this truly undervalued or a value trap?")
```

### Pattern 2: Growth Quality Check
```python
# Rule: Screen for high growth
if Growth > 25%:
    # LLM: Assess sustainability
    llm.chat("Is this growth sustainable?")
```

### Pattern 3: Risk Assessment
```python
# Rule: Flag high debt
if Debt > 1.5:
    # LLM: Detailed risk analysis
    llm.chat("What are the specific risks here?")
```

### Pattern 4: Multi-Stage Filter
```python
# Rule 1: Basic health check
if Current_Ratio > 1.0 and ROE > 10%:
    # Rule 2: Value screen
    if PE < 25:
        # LLM: Final decision on promising candidates
        return llm_analysis(ticker, data)
```

---

## 🆚 **Hybrid vs LLM-Powered**

### LLM-Powered (Pure):
```python
# Analyze EVERY stock with LLM
def analyze(self, ticker, data):
    prompt = f"Analyze {ticker}: {fundamentals}"
    return self.llm.chat(prompt)  # Every time!
```

**Use cases:**
- Small number of stocks (< 10)
- Deep research needed
- Cost not a concern
- Want maximum insight

---

### Hybrid (Smart):
```python
# Filter first, THEN use LLM
def analyze(self, ticker, data):
    # Fast filter (rules)
    if self._passes_filter(data):
        # LLM only on candidates
        return self._llm_analysis(ticker, data)
    return Signal('neutral', 0.5, 'Filtered out')
```

**Use cases:**
- Large number of stocks (> 50)
- Need to balance speed and depth
- Budget-conscious
- Want efficiency

---

## 🧪 **Example: Building a Hybrid Agent**

### Step-by-Step:

#### 1. **Define Screening Rules**
```
Rule 1: PE Ratio < 20 (undervalued or reasonable)
Rule 2: Revenue Growth > 10% (growing business)

Logic: If BOTH rules pass → Analyze with LLM
```

#### 2. **Configure LLM**
```
Provider: Ollama (free, local)
Temperature: 0.5 (balanced)
System Prompt: "You are a value investor looking for quality growth."
```

#### 3. **Generated Code**
```python
class HybridValueGrowth(Agent):
    def analyze(self, ticker, data):
        # Screening rules
        if data.get('pe_ratio', 0) < 20 and data.get('revenue_growth', 0) > 10:
            # Passed! Use LLM
            prompt = f"Detailed analysis of {ticker}..."
            response = self.llm.chat(prompt)
            return parse_llm_signal(response)
        
        # Filtered out
        return Signal('neutral', 0.5, 'Did not pass value + growth criteria')
```

#### 4. **Result**
```
Test on 500 stocks:
- 475 filtered out by rules (instant)
- 25 analyzed by LLM (3 seconds each = 75 seconds)
- Total time: 75 seconds vs 25 minutes (pure LLM)
- Total cost: $0.25 vs $5.00
- Quality: Same depth, but only on qualified candidates ✅
```

---

## 🎓 **Educational Value**

### What Students Learn:

#### 1. **Optimization**
```
How to balance speed, cost, and quality
```

#### 2. **Two-Stage Thinking**
```
Broad filter → Deep analysis
(Like college admissions: GPA filter → Interview)
```

#### 3. **Real-World Constraints**
```
Can't analyze everything deeply
Need to prioritize
Resource management matters
```

#### 4. **Combining Techniques**
```
Rules for what you know
LLM for what you don't
Use each tool for its strengths
```

---

## 🆚 **Quick Comparison**

### Analyzing 500 Stocks:

| Metric | Rule-Based | LLM-Powered | **Hybrid** |
|--------|------------|-------------|------------|
| **Time** | 1 second | 25 minutes | **90 seconds** |
| **Cost** | $0 | $5.00 | **$0.25** |
| **Depth** | Surface | Deep | **Deep (on 25)** |
| **Signals** | 500 signals | 500 signals | **25 deep + 475 neutral** |
| **Best For** | Quick screen | Deep research | **Production** |

**Winner:** Hybrid for real-world use (scale + quality)

---

## 🛠️ **Building Hybrid Agents in GUI**

### Updated UI:

```
Create Agent
├── Agent Type: [Hybrid ▼]
│
├── LLM Configuration
│   ├── Provider: ollama
│   ├── Temperature: 0.5
│   └── System Prompt: "You are..."
│
└── Screening Rules (Step 1: Filter) ← NEW!
    ├── Rule 1: PE < 20
    ├── Rule 2: Growth > 10%
    └── Logic: If pass → LLM analyzes
```

### The Flow:

```
1. Select "Hybrid" type
2. Configure LLM (provider, temp, prompt)
3. Define screening rules (what triggers LLM)
4. Generate code
5. Test with backtesting (see how many pass filter)
```

---

## 📈 **Performance Comparison**

### Test: Screening S&P 500

#### Pure LLM:
```
500 stocks × 3 seconds each = 1,500 seconds (25 minutes)
500 calls × $0.01 = $5.00
Result: 50 bullish, 100 bearish, 350 neutral
```

#### Hybrid (PE < 20, Growth > 10%):
```
500 stocks × rules check (instant) = 0.5 seconds
25 stocks pass filter
25 stocks × 3 seconds LLM = 75 seconds
25 calls × $0.01 = $0.25
Result: 15 bullish, 5 bearish, 5 neutral (detailed), 475 filtered
```

**Savings:** 95% time, 95% cost, same quality on qualified candidates!

---

## 🎯 **Best Practices**

### Good Hybrid Rules:

✅ **DO:**
```python
# Broad screening (filters 80-95% of stocks)
if PE < 25 and Margins > 5%:
    return llm_analysis()

# Result: Manageable number of LLM calls
```

❌ **DON'T:**
```python
# Too strict (filters 99% - misses opportunities)
if PE < 5 and ROE > 50%:
    return llm_analysis()

# Too loose (90% pass - defeats purpose)
if PE < 100:
    return llm_analysis()
```

### Optimal Filter Rate:

```
Filter should pass: 5-20% of stocks

Too strict (< 5%): Missing opportunities
Too loose (> 20%): Not saving enough on LLM costs
Sweet spot: 5-15% pass rate
```

---

## 🚀 **Hybrid Agent Use Cases**

### 1. **Daily Market Scan**
```
Screen 3,000 stocks → Find 50 candidates → Deep LLM analysis
Result: 50 actionable insights per day (manageable)
```

### 2. **Sector Rotation**
```
Screen each sector (100 stocks) → Find top 5 → LLM compares them
Result: Best pick from each sector
```

### 3. **Watchlist Builder**
```
Screen for setup (rules) → LLM confirms (detailed) → Add to watchlist
Result: High-quality watchlist with AI validation
```

### 4. **Risk-Managed Portfolio**
```
Screen for safety (rules) → LLM assesses specific risks → Build portfolio
Result: Safe candidates with detailed risk analysis
```

---

## ✅ **Summary**

**Hybrid Agents = Rules + LLM**

**The Idea:**
- Use fast rules to filter
- Use smart LLM to analyze

**The Benefit:**
- 95% cost reduction
- 95% time reduction
- Same depth of analysis (on qualified stocks)

**The Trade-off:**
- More complex to configure
- Need to tune filter rules
- Two-step process to understand

**The Use Case:**
- Analyzing large numbers of stocks
- Need both speed and depth
- Budget or time constraints
- Production workflows

**Now in GUI:**
- ✅ Clear explanation of hybrid concept
- ✅ Separate sections for rules and LLM
- ✅ Visual distinction from pure LLM
- ✅ Proper two-stage configuration

---

**Your observation was correct:** The UI wasn't showing what makes hybrid agents special. This is now fixed! 🎉
