# Formula Feature Quick Reference

## What's This?

The GUI now supports **custom analytical models** using mathematical formulas! Finance students can implement sophisticated models like PEG ratios, Graham Numbers, Altman Z-Scores, and polynomial functions.

## Quick Start

### 1. Use Pre-built Formula Template

```bash
1. Open http://localhost:5173
2. Click "PEG Growth Investing" template (orange)
3. See formula-based conditions
4. Create agent!
```

### 2. Add Formula to New Agent

```bash
1. Create New Agent → Start from Scratch
2. Fill basic info
3. Choose "Rule-Based"
4. In Rule Builder, click "Add Formula Condition"
5. Enter formula, map variables, set threshold
6. Click "Validate Formula"
7. Create!
```

## Formula Syntax

### Operators
- `+` `-` `*` `/` - Basic arithmetic
- `**` - Power (e.g., `X**2` for X squared)
- `()` - Grouping

### Functions
- `sqrt(X)` - Square root
- `abs(X)` - Absolute value
- `log(X)` - Natural logarithm
- `pow(X, Y)` - X to power Y
- `max(X, Y)`, `min(X, Y)` - Min/max

### Variables
- Use UPPERCASE: `PE_RATIO`, `GROWTH_RATE`, etc.
- Map to data fields in GUI
- Multiple variables allowed

## Common Formulas

### PEG Ratio
```
Formula: PE_RATIO / GROWTH_RATE
Variables:
  PE_RATIO = pe_ratio
  GROWTH_RATE = revenue_growth
Threshold: < 1.0 (undervalued growth)
```

### Graham Number
```
Formula: sqrt(22.5 * EPS * BVPS)
Variables:
  EPS = eps
  BVPS = book_value_per_share
Threshold: > PRICE (price below intrinsic value)
```

### Custom Quality Score
```
Formula: (ROE * 0.4) + (GROWTH * 0.3) + (MARGIN * 0.3)
Variables:
  ROE = roe
  GROWTH = revenue_growth
  MARGIN = profit_margin
Threshold: > 18.0 (high quality)
```

## Available Data Fields

- `pe_ratio`, `pb_ratio` - Valuation
- `dividend_yield`, `payout_ratio` - Dividends
- `revenue_growth`, `earnings_growth` - Growth
- `roe`, `roa`, `profit_margin` - Profitability
- `debt_to_equity`, `current_ratio` - Financial health
- `price`, `market_cap` - Market data
- `eps`, `book_value_per_share` - Per-share metrics

## Validation

Always click **"Validate Formula"** to:
- ✅ Check syntax errors
- ✅ Verify variables are defined
- ✅ Test with sample data
- ✅ See calculated result

## Mixing Simple & Formula

You can combine both in one rule!

```
Rule 1:
  - Formula: PE_RATIO / GROWTH_RATE < 1.0
  - Simple: dividend_yield > 2.0
  - Simple: debt_to_equity < 0.5
  Action: Buy 10%
```

## Troubleshooting

**"Undefined variable" error:**
- Make sure all UPPERCASE words in formula are mapped
- Check spelling matches exactly

**"Invalid syntax" error:**
- Check parentheses are balanced
- Verify operator spelling
- Use `**` not `^` for power

**"Data field not found" error:**
- Selected data field doesn't exist in stock data
- Choose from available fields list

## Backend API

Restart backend to load formula support:
```bash
# Ctrl+C to stop backend, then:
cd AI-Agent-Builder/gui_system
python run.py
```

Frontend will auto-reload when you make changes.

## Support

- Pre-built templates: `/api/formulas/templates`
- Validation endpoint: `/api/formulas/validate`
- See API docs: http://localhost:8000/docs
