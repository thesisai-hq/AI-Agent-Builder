# Macro Analyst - Quick Reference

**Quick answers without reading full documentation**

---

## 🎯 One-Minute Summary

The Macro Analyst tells you: **"Should I buy this stock given current economic conditions?"**

It analyzes:
1. **Economic health** (Fed, inflation, GDP, jobs)
2. **Market regime** (bull/bear/risk-on/risk-off)
3. **Sector fit** (does macro favor this sector?)
4. **AI synthesis** (forward-looking view)

---

## 📊 Economic Indicator Cheat Sheet

| Indicator | Bullish | Neutral | Bearish |
|-----------|---------|---------|---------|
| **Fed Rate** | < 2% | 3.5-5% | > 6% |
| **Inflation** | < 2% | 2-3.5% | > 5% |
| **GDP Growth** | > 3.5% | 1.5-2.5% | < 0% |
| **Unemployment** | < 3.5% | 4.5-5.5% | > 7% |
| **10Y Yield** | < 2.5% | 3.5-4.5% | > 5.5% |
| **VIX** | < 15 | 15-20 | > 30 |

### Quick Interpretation

```
High GDP + Low rates + Low VIX = 🟢 BULL MARKET (buy cyclicals)
Low GDP + High rates + High VIX = 🔴 BEAR MARKET (buy defensives)
```

---

## 🎭 Market Regimes

| Regime | When | Buy | Avoid |
|--------|------|-----|-------|
| **BULL** | VIX<15, GDP>2.5% | Growth, Cyclicals | Defensives |
| **BEAR** | VIX>30, GDP<1% | Defensives, Cash | Cyclicals |
| **RISK-ON** | Low vol, strong economy | Small-caps, Emerging | Bonds |
| **RISK-OFF** | High vol, uncertainty | Large-caps, Treasuries | High beta |

---

## 🏭 Sector Rotation Guide

### Which Sectors Win in Each Environment?

#### Bull Market (VIX < 15, GDP > 2.5%)
✅ **Winners:**
- Technology (+22% avg)
- Consumer Discretionary (+18%)
- Financials (+16%)

❌ **Losers:**
- Utilities (+8%)
- Consumer Staples (+10%)

#### Bear Market (VIX > 25, GDP < 1%)
✅ **Winners:**
- Utilities (+2%)
- Healthcare (+1%)
- Consumer Staples (0%)

❌ **Losers:**
- Financials (-18%)
- Technology (-15%)
- Consumer Discretionary (-12%)

#### High Interest Rates (Fed > 5%)
✅ **Winners:**
- Energy (less rate-sensitive)
- Financials* (if steep yield curve)

❌ **Losers:**
- Utilities (very rate-sensitive)
- Real Estate (very rate-sensitive)
- Technology (growth stocks hurt)

*Financials are complex - need steep yield curve

#### Low Interest Rates (Fed < 2%)
✅ **Winners:**
- Technology (growth stocks benefit)
- Real Estate (borrowing cheap)
- Utilities (bond proxy attractive)

❌ **Losers:**
- Financials (narrow interest margins)

---

## 🎯 Signal Interpretation

### What Each Signal Means

| Signal | Translation | Action |
|--------|------------|--------|
| **BULLISH** | Macro tailwinds for this stock/sector | Consider buying |
| **NEUTRAL** | Macro neither helps nor hurts | No macro edge, use fundamentals |
| **BEARISH** | Macro headwinds for this stock/sector | Avoid or wait |

### Confidence Levels

| Confidence | Meaning | Reliability |
|------------|---------|-------------|
| **80%+** | All stages agree strongly | High |
| **60-80%** | Most stages agree | Good |
| **40-60%** | Mixed signals | Uncertain |
| **< 40%** | Stages disagree | Low - need more research |

---

## 🔧 Quick Customization

### Make It More Aggressive

```python
# In advanced_macro_analyst.py, line ~550
if final_score >= 0.55:  # Was 0.65
    final_signal = 'bullish'
```

### Make It More Conservative

```python
# In advanced_macro_analyst.py, line ~550
if final_score >= 0.75:  # Was 0.65
    final_signal = 'bullish'
```

### Adjust Sector Weights

```python
# For growth-focused strategy
weights = {
    'economic_indicators': 0.30,  # Less weight
    'sector_impact': 0.35,        # More weight
    'market_regime': 0.20,
    'ai_synthesis': 0.15
}
```

---

## 💡 Common Scenarios

### Scenario 1: "Fed is hiking rates"

```
Fed Rate: 5.5% (rising)
→ Restrictive policy
→ Hurts growth stocks (Technology)
→ Hurts rate-sensitive (Utilities, Real Estate)
→ Macro signal: BEARISH for these sectors
```

### Scenario 2: "Recession fears"

```
GDP: 0.5% (weak)
Unemployment: 5.8% (rising)
VIX: 28 (elevated)
→ Regime: BEAR_MARKET or RISK_OFF
→ Favor: Healthcare, Utilities, Staples
→ Avoid: Cyclicals
```

### Scenario 3: "Strong economy, low inflation"

```
GDP: 3.8% (strong)
Inflation: 2.1% (target)
VIX: 13 (low)
→ Regime: BULL_MARKET / RISK_ON
→ Favor: Technology, Discretionary, Small-caps
→ Macro signal: BULLISH for growth stocks
```

### Scenario 4: "Mixed signals"

```
GDP: 2.3% (ok)
Fed: 5.0% (high)
Inflation: 3.2% (elevated)
VIX: 18 (normal)
→ Regime: TRANSITIONAL
→ Macro signal: NEUTRAL
→ Rely on fundamental analysis for stock selection
```

---

## 🧪 Quick Test

```bash
# Test economic indicators
python test_macro_analyst.py --indicators

# Test regime detection
python test_macro_analyst.py --regime

# Test sector rotation
python test_macro_analyst.py --sectors

# Full analysis for AAPL
python test_macro_analyst.py --single AAPL

# All tests
python test_macro_analyst.py --all
```

---

## 🎓 Key Concepts

### Top-Down vs. Bottom-Up

**Top-Down (Macro):**
```
Economy → Sectors → Stocks
"Is this a good time to own stocks?"
"Which sectors are favored?"
```

**Bottom-Up (Fundamental):**
```
Stock → Industry → Economy
"Is this a good company?"
"Is it undervalued?"
```

**Best Approach:** Use BOTH
- Macro for timing and sector selection
- Fundamentals for stock selection within sectors

### Business Cycle Stages

```
1. Early Recovery → Buy: Financials, Industrials
2. Mid Expansion → Buy: Technology, Discretionary  
3. Late Expansion → Buy: Energy, Materials
4. Recession → Buy: Healthcare, Utilities, Staples

Current stage determines sector rotation
```

---

## ⚠️ Important Notes

### What Macro CAN Tell You

✅ General market environment (bull/bear)  
✅ Which sectors are favored  
✅ Major headwinds/tailwinds  
✅ Regime changes (risk-on to risk-off)

### What Macro CANNOT Tell You

❌ Exact timing of market moves  
❌ Individual stock quality  
❌ Short-term price movements  
❌ Company-specific risks

**Always combine with fundamental analysis!**

---

## 📞 Quick Answers

**Q: When should I use macro analysis?**  
A: When making sector allocation decisions or market timing.

**Q: Can I ignore macro and just use fundamentals?**  
A: You can, but you'll miss major regime shifts (e.g., 2022 rate shock).

**Q: What if macro and fundamentals disagree?**  
A: Macro = timing, Fundamentals = selection. Great company in bad macro = wait. Bad company in good macro = still avoid.

**Q: How often should I re-run macro analysis?**  
A: Monthly (Fed meetings), or when major economic data released.

**Q: Is macro analysis useful for day trading?**  
A: No. Macro is for position trading (weeks to months), not day trading.

---

## 🎯 Best Practices

1. ✅ Run macro analysis BEFORE picking stocks
2. ✅ Update when major economic data released
3. ✅ Use for sector rotation decisions
4. ✅ Combine with fundamental analysis
5. ✅ Pay attention to regime changes
6. ✅ Don't fight the Fed (most important rule)

---

**Remember: "Don't fight the Fed" - most important macro rule!**

When Fed is:
- **Easing (cutting rates)**: Be bullish 🟢
- **Tightening (raising rates)**: Be cautious 🔴
- **Pausing**: Use fundamentals 🟡

**Marty Zweig**: "Don't fight the Fed" - wins 80%+ of the time historically.