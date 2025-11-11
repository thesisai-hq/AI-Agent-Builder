# Advanced Rule-Based Agents - Complete Guide

## Overview

Rule-based agents now support three strategies:

1. **Simple Rules** - Single condition per rule
2. **Advanced Rules** - Multi-condition with AND/OR logic
3. **Score-Based** - Point accumulation system

All strategies are visual - no coding required!

## 1. Simple Rules

**Best for:** Clear, straightforward criteria

### Example: Basic Value Investing

```
Rule 1: If PE Ratio < 15 → Bullish (0.8)
Rule 2: If PE Ratio > 30 → Bearish (0.7)
```

**In GUI:**
```
Rule Style: Simple Rules
Number of Rules: 2

Rule 1:
  Metric: pe_ratio
  Operator: <
  Threshold: 15
  Signal: bullish
  Confidence: 0.8

Rule 2:
  Metric: pe_ratio
  Operator: >
  Threshold: 30
  Signal: bearish
  Confidence: 0.7
```

**Generated Code:**
```python
def analyze(self, ticker, data):
    pe_ratio = data.get('pe_ratio', 0)
    
    if pe_ratio < 15:
        return Signal('bullish', 0.8, f'PE {pe_ratio:.1f} is bullish')
    
    if pe_ratio > 30:
        return Signal('bearish', 0.7, f'PE {pe_ratio:.1f} is bearish')
    
    return Signal('neutral', 0.5, 'No rules matched')
```

## 2. Advanced Rules (Multi-Condition)

**Best for:** Sophisticated strategies combining multiple factors

### Example: Quality Growth Strategy

**Strategy:** Buy companies with:
- (Growth > 20% AND Margin > 15%) → Strong bullish
- OR (PE < 15 AND ROE > 15%) → Moderate bullish

**In GUI:**
```
Rule Style: Advanced Rules
Number of Rules: 2

Rule 1:
  Number of Conditions: 2
  Combine with: AND
  
  Condition 1:
    Metric: revenue_growth
    Op: >
    Value: 20
  
  Condition 2:
    Metric: profit_margin
    Op: >
    Value: 15
  
  Signal: bullish
  Confidence: 0.9

Rule 2:
  Number of Conditions: 2
  Combine with: AND
  
  Condition 1:
    Metric: pe_ratio
    Op: <
    Value: 15
  
  Condition 2:
    Metric: roe
    Op: >
    Value: 15
  
  Signal: bullish
  Confidence: 0.75
```

**Generated Code:**
```python
def analyze(self, ticker, data):
    # Extract metrics
    revenue_growth = data.get('revenue_growth', 0)
    profit_margin = data.get('profit_margin', 0)
    pe_ratio = data.get('pe_ratio', 0)
    roe = data.get('roe', 0)
    
    # Rule 1: Growth AND Margin
    if (revenue_growth > 20) and (profit_margin > 15):
        return Signal('bullish', 0.9, 'High growth with strong margins')
    
    # Rule 2: Value AND Quality
    if (pe_ratio < 15) and (roe > 15):
        return Signal('bullish', 0.75, 'Undervalued with strong returns')
    
    return Signal('neutral', 0.5, 'No rules matched')
```

### Example: Defensive Screening

**Strategy:** Avoid companies with:
- (Debt > 2.0 OR Current Ratio < 1.0) → Bearish

**In GUI:**
```
Advanced Rule:
  Conditions: 2
  Logic: OR
  
  Condition 1: debt_to_equity > 2.0
  Condition 2: current_ratio < 1.0
  
  Signal: bearish
  Confidence: 0.8
```

### Calculated Metrics

**PEG Ratio** (PE / Growth):
```
Metric: peg_ratio
Op: <
Value: 1.0
→ "Fairly valued growth stock"
```

**Quality Score** (Weighted combination):
```
Formula: (ROE × 0.4) + (Margin × 0.3) + (1/Debt × 0.3)

Metric: quality_score
Op: >
Value: 20
→ "High quality company"
```

## 3. Score-Based Rules

**Best for:** Complex multi-factor analysis with weighted importance

### Example: Comprehensive Quality Screening

**Strategy:** Score companies on multiple factors, buy if score ≥ 3

**Scoring Criteria:**
- PE < 20: +1 point (valuation)
- Growth > 15%: +1 point (growth)
- Margin > 12%: +1 point (profitability)
- ROE > 15%: +1 point (efficiency)
- Debt < 1.0: +1 point (safety)
- Dividend > 2%: +1 point (income)

**In GUI:**
```
Rule Style: Score-Based
Number of Criteria: 6

Criterion 1:
  Metric: pe_ratio
  Op: <
  Value: 20
  Points: 1

Criterion 2:
  Metric: revenue_growth
  Op: >
  Value: 15
  Points: 1

Criterion 3:
  Metric: profit_margin
  Op: >
  Value: 12
  Points: 1

Criterion 4:
  Metric: roe
  Op: >
  Value: 15
  Points: 1

Criterion 5:
  Metric: debt_to_equity
  Op: <
  Value: 1.0
  Points: 1

Criterion 6:
  Metric: dividend_yield
  Op: >
  Value: 2.0
  Points: 1

Score Thresholds:
  Bullish if score >= 3 (confidence: 0.8)
  Bearish if score <= 0 (confidence: 0.6)
```

**Generated Code:**
```python
def analyze(self, ticker, data):
    score = 0
    reasons = []
    
    # Extract metrics
    pe_ratio = data.get('pe_ratio', 0)
    revenue_growth = data.get('revenue_growth', 0)
    # ... etc
    
    # Calculate score
    if pe_ratio < 20:
        score += 1
        reasons.append(f'PE {pe_ratio:.1f} < 20 (+1 pts)')
    
    if revenue_growth > 15:
        score += 1
        reasons.append(f'Growth {revenue_growth:.1f}% > 15 (+1 pts)')
    
    # ... more criteria
    
    # Determine signal
    if score >= 3:
        return Signal('bullish', 0.8, f'Score: {score}. ' + '; '.join(reasons))
    elif score <= 0:
        return Signal('bearish', 0.6, f'Score: {score}. ' + '; '.join(reasons))
    else:
        return Signal('neutral', 0.5, f'Score: {score}. ' + '; '.join(reasons))
```

### Example: Risk-Adjusted Scoring

**Strategy:** Score with both positive and negative points

**Criteria:**
- Growth > 20%: +2 points (strong positive)
- Margin > 15%: +1 point
- ROE > 15%: +1 point
- Debt > 2.0: -2 points (strong negative)
- PE > 40: -1 point
- Current Ratio < 1.0: -1 point

**Thresholds:**
- Score ≥ 2: Bullish
- Score ≤ -2: Bearish
- Between: Neutral

## Comparison

### When to Use Each

| Strategy | Best For | Example |
|----------|----------|---------|
| **Simple** | Clear single conditions | "Buy if PE < 15" |
| **Advanced** | Multiple factors | "Buy if (growth > 20 AND margin > 15) OR (PE < 12 AND ROE > 20)" |
| **Score-Based** | Comprehensive screening | "Score on 10 factors, buy if score ≥ 5" |

### Complexity vs Power

| Strategy | Setup Time | Flexibility | Power |
|----------|------------|-------------|-------|
| Simple | 1 min | Low | Basic |
| Advanced | 3-5 min | Medium | Good |
| Score-Based | 5-10 min | High | Excellent |

## Real-World Examples

### Value Investing (Simple)

```
Rule 1: PE < 15 → Bullish (0.8)
Rule 2: Dividend Yield > 3% → Bullish (0.7)
Rule 3: PE > 30 → Bearish (0.7)
```

### GARP - Growth at Reasonable Price (Advanced)

```
Rule 1 (AND):
  - revenue_growth > 20
  - pe_ratio < 25
  - profit_margin > 10
  → Bullish (0.9)

Rule 2 (OR):
  - peg_ratio < 1.0
  - quality_score > 25
  → Bullish (0.75)
```

### Piotroski F-Score Style (Score-Based)

```
9 Criteria (each worth +1 point):

Profitability:
1. ROE > 0: +1
2. Operating Cash Flow > 0: +1
3. ROE > Last Year ROE: +1

Leverage:
4. Debt/Equity < Last Year: +1
5. Current Ratio > Last Year: +1

Efficiency:
6. Profit Margin > Last Year: +1
7. Asset Turnover > Last Year: +1

Other:
8. No new shares issued: +1
9. Revenue Growth > 0: +1

Bullish if score >= 7 (confidence: 0.9)
Bearish if score <= 3 (confidence: 0.7)
```

## Tips & Best Practices

### Simple Rules

**Do:**
- ✅ Use for straightforward screens
- ✅ Test one metric at a time
- ✅ Clear thresholds

**Don't:**
- ❌ Mix too many different strategies
- ❌ Use conflicting rules

### Advanced Rules

**Do:**
- ✅ Combine related metrics (growth + margin)
- ✅ Use AND for quality screens
- ✅ Use OR for opportunity identification

**Don't:**
- ❌ Create overly complex conditions (keep to 2-3 per rule)
- ❌ Mix unrelated metrics with AND

### Score-Based

**Do:**
- ✅ Weight important factors with more points
- ✅ Use negative points for red flags
- ✅ Set realistic thresholds (not too high)

**Don't:**
- ❌ Use too many criteria (diminishing returns after 8-10)
- ❌ Make all criteria equal weight (prioritize!)

## Testing Your Rules

### Backtest Mentally

Before creating, think through:
- **AAPL:** PE=28, Growth=10%, Margin=25%, ROE=45%
  - Would your rules signal correctly?
  
- **High-growth tech:** PE=60, Growth=40%, Margin=5%, Debt=0.5
  - Should be bullish or neutral (not bearish)
  
- **Stable utility:** PE=15, Growth=3%, Margin=10%, Dividend=5%
  - Should be bullish (income focus)

### Test in GUI

1. Create agent with your rules
2. Test with various mock data configurations
3. Adjust thresholds and weights
4. Iterate until results match your strategy

## Examples from Finance Literature

### Benjamin Graham (Value)

**Simple Rules:**
- PE < 15 → +1
- PB < 1.5 → +1
- Debt/Equity < 1.0 → +1
- Current Ratio > 2.0 → +1
- Score ≥ 3 → Bullish

### Peter Lynch (GARP)

**Advanced Rule:**
```
(peg_ratio < 1.0) AND (revenue_growth > 15) AND (debt_to_equity < 1.5)
→ Bullish (0.9)
```

### Warren Buffett (Quality)

**Score-Based:**
- ROE > 15%: +2 points
- Profit Margin > 15%: +2 points  
- Debt/Equity < 0.5: +1 point
- Revenue Growth > 10%: +1 point
- PE < 20: +1 point

Score ≥ 4 → Bullish

## Files Changed

1. ✅ `gui/app.py` - Added rule style selector and UI for all types
2. ✅ `gui/agent_creator.py` - Code generation for all three types
3. ✅ `gui/ADVANCED_RULES.md` - This documentation

## Summary

**What you can now create:**
- ✅ Simple single-condition rules
- ✅ Multi-condition rules with AND/OR
- ✅ Calculated metrics (PEG, Quality Score)
- ✅ Point-based scoring systems
- ✅ Weighted factor analysis
- ✅ Complex investment strategies

**All without writing code!** Students can build sophisticated strategies visually.

---

**Status:** Implemented ✅  
**Version:** 1.2.0  
**Date:** 2025-01-23
