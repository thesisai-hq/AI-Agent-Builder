# Hybrid Agents Explained

**What:** Combines rule-based screening with LLM-powered analysis  
**Why:** Best of both worlds - speed + intelligence  
**When:** Analyzing large sets of stocks where you need both filtering and deep insights

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

## Related Documentation

- [Data Flow](DATA_FLOW.md) - See how hybrid agents process data in two stages
- [Multi-Agent Systems](MULTI_AGENT_SYSTEMS.md) - Combine hybrid with other agent types
- [Choosing Agent Type](CHOOSING_AGENT_TYPE.md) - When to use hybrid vs other types
- [LLM Customization](LLM_CUSTOMIZATION.md) - Configure the LLM analysis stage

---

**Your observation was correct:** The UI wasn't showing what makes hybrid agents special. This is now fixed! 🎉
