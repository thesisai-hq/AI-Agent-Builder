# Example Agents - Strategy Library

This directory contains both framework examples and investment strategy templates.

## Framework Examples (Protected)

These demonstrate the framework's capabilities:

- **01_basic.py** - Simple rule-based agents (Value, Growth)
- **02_llm_agent.py** - LLM-powered agents with different personas
- **03_rag_agent.py** - RAG-powered document analysis
- **04_custom_llm_config.py** - LLM customization

**Protected:** Cannot be deleted from GUI

## Investment Strategy Examples

Learn from famous investors! These are ready-to-use strategies:

### 05_buffett_quality.py
**Warren Buffett's Quality Investing**

```
Strategy: Score-Based
Focus: High-quality businesses

Criteria:
- ROE > 15%: +2 points (strong returns)
- Profit Margin > 15%: +2 points (pricing power)
- Debt < 0.5: +1 point (financial strength)
- Growth > 10%: +1 point (expanding business)
- Current Ratio > 1.5: +1 point (liquidity)

Bullish if score >= 4 (excellent quality)
```

**Best for:** Long-term investors seeking quality companies

---

### 06_lynch_garp.py
**Peter Lynch's Growth at Reasonable Price**

```
Strategy: Advanced Rules (Multi-Condition)
Focus: Growth companies at fair valuations

Rule 1 (AND):
- PEG < 1.0 (undervalued growth)
- Growth > 15% (strong expansion)
- Margin > 10% (profitable)
→ Bullish (90%)

Rule 2 (AND):
- Growth > 25% (high growth)
- PE < 30 (reasonable valuation)
→ Bullish (75%)
```

**Best for:** Growth investors seeking value

---

### 07_graham_value.py
**Benjamin Graham's Value Investing**

```
Strategy: Score-Based
Focus: Deep value with margin of safety

Criteria:
- PE < 15: +2 points (undervalued)
- PB < 1.5: +1 point (book value)
- Debt < 1.0: +1 point (conservative)
- Current Ratio > 2.0: +1 point (safety)
- Dividend > 2%: +1 point (income)

Bullish if score >= 3 (strong value)
```

**Best for:** Conservative value investors

---

## How to Use These Examples

### 1. Browse & Learn

```bash
# Launch GUI
./gui/launch.sh

# Go to: Browse Agents
# Click "👁️ View" on any strategy
# Study the code
```

### 2. Duplicate & Customize

```
Browse → Find "BuffettQualityAgent"
→ Click "📋 Copy"
→ Name: "buffett_quality_aggressive.py"
→ Duplicate!

Now modify:
- Lower thresholds for more signals
- Add more criteria
- Adjust confidence levels
```

### 3. Test with Different Data

```
Test Agent → Select "BuffettQualityAgent"

Try different scenarios:
- High quality: ROE=25%, Margin=20%, Debt=0.3
- Low quality: ROE=8%, Margin=5%, Debt=2.0
- Mixed: ROE=18%, Margin=12%, Debt=1.2

See how the strategy responds!
```

### 4. Create Variations

**From Buffett Quality, create:**
- `buffett_quality_strict.py` - Higher thresholds (ROE > 20%)
- `buffett_quality_relaxed.py` - Lower thresholds (ROE > 12%)
- `buffett_quality_tech.py` - Adapted for tech stocks

**From Lynch GARP, create:**
- `lynch_garp_aggressive.py` - Accept higher PEG (< 1.5)
- `lynch_garp_conservative.py` - Require lower PEG (< 0.8)

**From Graham Value, create:**
- `graham_deep_value.py` - Stricter criteria
- `graham_income_focus.py` - Emphasize dividends

## Comparison Table

| Strategy | Type | Risk | Best For | Typical Returns |
|----------|------|------|----------|-----------------|
| Buffett Quality | Score | Medium | Long-term | Steady growth |
| Lynch GARP | Advanced | Medium-High | Growth seekers | Higher growth |
| Graham Value | Score | Low | Conservative | Value + income |

## Learning Path

**Beginner:**
1. Start with 01_basic.py (simple rules)
2. Study 05_buffett_quality.py (score-based)
3. Duplicate and test variations

**Intermediate:**
1. Study 06_lynch_garp.py (advanced rules)
2. Learn PEG ratio calculations
3. Create multi-condition strategies

**Advanced:**
1. Study 02_llm_agent.py (AI-powered)
2. Study 03_rag_agent.py (document analysis)
3. Combine techniques (hybrid agents)

## Strategy Philosophy Summary

### Buffett (Quality)
> "It's far better to buy a wonderful company at a fair price than a fair company at a wonderful price."

Focus on business quality over price.

### Lynch (GARP)
> "Find a growth company at a value price."

Balance growth prospects with reasonable valuation.

### Graham (Value)
> "The margin of safety is always dependent on the price paid."

Buy with significant discount to intrinsic value.

## Tips for Customization

### Adjusting Thresholds

**More Aggressive (more signals):**
- Lower quality thresholds (ROE > 12% instead of 15%)
- Accept higher PE ratios
- Reduce required score

**More Conservative (fewer, better signals):**
- Raise quality thresholds (ROE > 20%)
- Require lower PE ratios
- Increase required score

### Adding Criteria

**Risk Metrics:**
- Add beta < 1.0 for lower volatility
- Add cash flow positive
- Add earnings stability

**Growth Metrics:**
- Add earnings growth > revenue growth
- Add market share expansion
- Add new product launches

### Combining Strategies

```python
# Duplicate Buffett Quality
# Add Lynch GARP PEG criterion
# Create "Buffett-Lynch Hybrid"

if peg < 1.0 and quality_score >= 4:
    return Signal('bullish', 0.95, 'Quality + GARP')
```

## Next Steps

1. **Browse** these examples in the GUI
2. **Test** them with different mock data
3. **Duplicate** to create your own variations
4. **Study** the code to understand the strategies
5. **Build** your own strategy combining ideas

---

**Remember:** These are educational examples based on published investment principles. Not financial advice. Always do your own research!
