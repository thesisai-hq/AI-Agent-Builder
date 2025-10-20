# Technical Analyst - Quick Reference

**Quick answers for technical analysis without reading full docs**

---

## 🎯 One-Minute Summary

The Technical Analyst tells you: **"What do the charts say about this stock?"**

Analyzes:
1. **Trend** - Is price going up, down, or sideways?
2. **Momentum** - Is it overbought/oversold?
3. **Volume** - Does volume confirm the move?
4. **Volatility** - What are the key support/resistance levels?

---

## 📊 Indicator Cheat Sheet

### Moving Averages

| Setup | Signal | Meaning |
|-------|--------|---------|
| Price > SMA20 > SMA50 > SMA200 | 🟢 BULLISH | Strong uptrend |
| Price < SMA20 < SMA50 < SMA200 | 🔴 BEARISH | Strong downtrend |
| SMA50 crosses above SMA200 | 🟢 Golden Cross | Long-term bullish |
| SMA50 crosses below SMA200 | 🔴 Death Cross | Long-term bearish |

### RSI (Relative Strength Index)

| RSI Level | State | Action |
|-----------|-------|--------|
| < 20 | Extreme Oversold | 🟢 STRONG BUY |
| 20-30 | Oversold | 🟢 Buy |
| 30-70 | Neutral | ⏸️ No signal |
| 70-80 | Overbought | 🔴 Sell |
| > 80 | Extreme Overbought | 🔴 STRONG SELL |

**Rule of thumb:** Buy when RSI < 30, sell when RSI > 70

### MACD

| Condition | Signal |
|-----------|--------|
| MACD > Signal Line AND both positive | 🟢 Strong Bullish |
| MACD crosses above Signal | 🟢 Bullish |
| MACD crosses below Signal | 🔴 Bearish |
| MACD < Signal Line AND both negative | 🔴 Strong Bearish |

### Bollinger Bands (%B)

| %B Value | Position | Action |
|----------|----------|--------|
| > 1.0 | Above upper band | 🔴 Overbought - Sell |
| 0.8-1.0 | Near upper | ⚠️ Caution |
| 0.2-0.8 | Middle range | ⏸️ No signal |
| 0.0-0.2 | Near lower | 🟢 Opportunity |
| < 0.0 | Below lower band | 🟢 Oversold - Buy |

### Volume Confirmation

| Price | Volume | Interpretation | Signal |
|-------|--------|----------------|--------|
| ↑ Rising | ↑ Rising | Healthy uptrend | 🟢 Bullish |
| ↑ Rising | ↓ Falling | Distribution warning | ⚠️ Caution |
| ↓ Falling | ↑ Rising | Strong selling | 🔴 Bearish |
| ↓ Falling | ↓ Falling | Possible accumulation | 🟢 Opportunity |

**Key Rule:** Volume should confirm price direction

---

## 🎓 Classic Patterns

### Reversal Patterns

| Pattern | Meaning | Reliability | Target |
|---------|---------|-------------|--------|
| Head & Shoulders | Bearish reversal | 60% | Neckline to head distance |
| Inverse H&S | Bullish reversal | 65% | Neckline to head distance |
| Double Top | Bearish reversal | 62% | Top to valley distance |
| Double Bottom | Bullish reversal | 67% | Valley to peak distance |

### Continuation Patterns

| Pattern | Meaning | Reliability | Target |
|---------|---------|-------------|--------|
| Bull Flag | Uptrend continues | 68% | Flagpole height |
| Ascending Triangle | Bullish breakout | 72% | Triangle height |
| Descending Triangle | Bearish breakdown | 64% | Triangle height |

---

## 🔍 Quick Diagnosis

### "Is this stock in an uptrend?"

**Check:**
1. Price > SMA200? (Yes = potential uptrend)
2. Price > SMA20 > SMA50? (Yes = confirmed uptrend)
3. SMA50 > SMA200? (Yes = long-term uptrend)

**All Yes → Strong Uptrend 🟢**

### "Is this stock oversold?"

**Check:**
1. RSI < 30? (Yes = oversold)
2. Price near lower Bollinger Band? (Yes = extreme)
3. Volume declining? (Yes = possible bottom)

**All Yes → Oversold Buy Opportunity 🟢**

### "Is this a breakout?"

**Check:**
1. Price breaking above resistance?
2. Volume > 1.5x average?
3. RSI > 50 (strength)?

**All Yes → Valid Breakout 🟢**

### "Should I sell?"

**Check:**
1. RSI > 70? (Overbought)
2. Price at resistance level?
3. Volume increasing on down days?

**All Yes → Consider Taking Profits 🔴**

---

## 🎯 Trading Rules

### Entry Rules

**Bullish Entry:**
```
✅ Uptrend confirmed (Price > SMA20 > SMA50)
✅ RSI 30-50 (not overbought)
✅ Volume confirms (rising on up days)
✅ Near support level (risk/reward favorable)
```

**Bearish Entry (Short):**
```
✅ Downtrend confirmed (Price < SMA20 < SMA50)
✅ RSI 50-70 (not oversold)
✅ Volume confirms (rising on down days)
✅ Near resistance level
```

### Exit Rules

**Take Profit:**
- Price hits resistance level
- RSI > 70 (overbought)
- Bearish divergence (price up, momentum down)
- Volume declining on rallies

**Stop Loss:**
- Below recent support level
- Below 20-day SMA (for uptrends)
- 2-3 ATR below entry (volatility-adjusted)

---

## ⚡ Quick Signals

### Strong Buy Signals

1. **Oversold Bounce**
   - RSI < 30
   - Price at lower Bollinger Band
   - In established uptrend

2. **Breakout**
   - Price breaks resistance
   - Volume > 1.5x average
   - RSI 40-60

3. **Trend Continuation**
   - Price pulls back to SMA20
   - RSI 40-50
   - Volume declining (healthy pullback)

### Strong Sell Signals

1. **Overbought Reversal**
   - RSI > 70
   - Price at upper Bollinger Band
   - Bearish divergence

2. **Breakdown**
   - Price breaks support
   - Volume > 1.5x average
   - RSI < 50

3. **Death Cross**
   - SMA50 crosses below SMA200
   - Confirmed with >1% separation

---

## 🎨 Visual Patterns

### Chart Reading 101

```
Price > all MAs → UPTREND
Price < all MAs → DOWNTREND
Price between MAs → SIDEWAYS/TRANSITIONAL

RSI > 70 → OVERBOUGHT (reversal risk)
RSI < 30 → OVERSOLD (bounce likely)

Volume ↑ with Price ↑ → HEALTHY (continue)
Volume ↓ with Price ↑ → WEAK (reversal risk)
```

### Support/Resistance Quick Guide

**Support = Floor (price bounces up)**
- Prior lows
- Round numbers ($100, $150, $200)
- Moving averages (especially 200-day)

**Resistance = Ceiling (price bounces down)**
- Prior highs
- Round numbers
- Moving averages when price below

**Breakout:** Price moves through resistance with volume
**Breakdown:** Price moves through support with volume

---

## 🔧 Customization

### Adjust for Trading Style

**Day Trading (1-7 days):**
```python
# Use shorter MAs
sma_5, sma_10, sma_20
rsi_period = 9  # More responsive
```

**Swing Trading (1-4 weeks):**
```python
# Default settings work great
sma_20, sma_50
rsi_period = 14
```

**Position Trading (Months):**
```python
# Use longer MAs
sma_50, sma_100, sma_200
rsi_period = 21  # Smoother
```

### Adjust for Volatility

**High Volatility Stocks:**
```python
rsi_oversold = 20  # Stricter
rsi_overbought = 80
bollinger_std = 2.5  # Wider bands
```

**Low Volatility Stocks:**
```python
rsi_oversold = 40  # Looser
rsi_overbought = 60
bollinger_std = 1.5  # Tighter bands
```

---

## 💡 Pro Tips

### 1. Trend Always Wins
```
Strong uptrend + Overbought RSI = Stay bullish
Weak uptrend + Oversold RSI = Be cautious
```
**Never fight the trend!**

### 2. Volume Confirms Everything
```
Price breakout + High volume = Valid
Price breakout + Low volume = False signal
```
**No volume = No conviction**

### 3. Multiple Timeframes
```
Daily chart: Uptrend
Weekly chart: Downtrend
→ Wait for alignment before trading
```

### 4. Risk Management
```
Always set stop loss below support
Risk 1% to make 2%+ (risk/reward ratio)
```

---

## 🐛 Troubleshooting

### "Why is everything neutral?"

**Possible causes:**
1. Market is choppy/sideways (common)
2. Indicators are mixed (waiting for clarity)
3. Thresholds too strict

**Solution:** This is correct! Wait for better setup.

### "RSI says oversold but still falling"

**Answer:** RSI can stay oversold in strong downtrends
- Check trend first (primary)
- Oversold in downtrend ≠ buy signal
- Wait for trend reversal confirmation

### "Golden Cross but stock drops"

**Answer:** Golden Cross is lagging indicator
- Works best in trending markets (70% success)
- Fails in whipsaw markets (30% failures)
- Confirm with momentum and volume

---

## ⚖️ Technical vs. Fundamental

| Aspect | Technical | Fundamental |
|--------|-----------|-------------|
| **What** | Price action | Company value |
| **When** | Short-term timing | Long-term investing |
| **Question** | "Is now the right time?" | "Is this the right stock?" |
| **Horizon** | Days to months | Months to years |
| **Best For** | Entry/exit timing | Stock selection |

**Best Practice:** Use BOTH
- Fundamental: Pick quality stocks
- Technical: Time the entry

---

## 📈 Common Scenarios

### Scenario 1: "Strong uptrend"
```
Trend: Price > SMA20 > SMA50 > SMA200
Momentum: RSI 55 (neutral)
Volume: Rising on up days
→ Signal: BULLISH (ride the trend)
→ Action: Hold or add on pullbacks to SMA20
```

### Scenario 2: "Oversold in uptrend"
```
Trend: Uptrend (price > MAs)
Momentum: RSI 28 (oversold)
Volume: Declining (healthy pullback)
→ Signal: BULLISH (buy the dip)
→ Action: Buy near SMA20 support
```

### Scenario 3: "Overbought but strong"
```
Trend: Strong uptrend
Momentum: RSI 78 (overbought)
Volume: High (continued interest)
→ Signal: NEUTRAL (wait)
→ Action: Don't short, but don't chase
```

### Scenario 4: "Breakdown"
```
Trend: Downtrend starting
Momentum: RSI 52 (neutral)
Volume: Surging on breakdown
→ Signal: BEARISH (avoid)
→ Action: Stay away or short
```

---

## ✅ Quick Checklist

Before taking a position, verify:

**For Long Position:**
- [ ] Uptrend confirmed (Price > SMA20)
- [ ] RSI not overbought (< 70)
- [ ] Volume confirms upside
- [ ] No nearby resistance
- [ ] Stop loss identified (below support)

**For Short Position:**
- [ ] Downtrend confirmed (Price < SMA20)
- [ ] RSI not oversold (> 30)
- [ ] Volume confirms downside
- [ ] No nearby support
- [ ] Stop loss identified (above resistance)

---

## 🎯 Key Takeaways

1. **Trend > Everything** - Don't fight the primary trend
2. **Volume Confirms** - Price without volume is suspect
3. **RSI for Timing** - Use for entry/exit, not direction
4. **Support/Resistance Matter** - Key levels act as magnets
5. **Combine Indicators** - No single indicator is perfect

---

**Remember: "The trend is your friend until it bends!"**

Price above 200-day MA = Uptrend (be bullish)
Price below 200-day MA = Downtrend (be cautious)