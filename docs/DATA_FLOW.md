# Agent Data Flow - Complete Transparency

**Understanding how data flows through agents from input to investment signal.**

**Audience:** Students, researchers, transparency-focused users, thesis-ai developers

**Related Documentation:**
- [Multi-Agent Systems](MULTI_AGENT_SYSTEMS.md) - How multiple agents work together
- [Choosing Agent Type](CHOOSING_AGENT_TYPE.md) - Compare agent types
- [API Reference](API_REFERENCE.md) - Technical API details

---

## Overview

This document shows **exactly** how data flows through the AI Agent Builder system, with full transparency on:
- What data goes in
- How it's processed  
- Where AI/LLM is involved
- What comes out
- No hidden logic

---

## Rule-Based Agent Flow (100% Transparent)

```
INPUT: Financial Data
├── pe_ratio: 12.5
├── roe: 18.2%
├── debt_to_equity: 0.4
├── profit_margin: 15.3%
└── revenue_growth: 12.1%

    ↓

RULE EVALUATION (Pure Python Logic - Visible in Code)
├── if pe_ratio < 15:       ✅ TRUE (12.5 < 15)
├── if roe > 15:            ✅ TRUE (18.2 > 15)
└── if debt_to_equity < 0.5: ✅ TRUE (0.4 < 0.5)

    ↓

SIGNAL GENERATION
├── direction: "bullish"  (all rules passed)
├── confidence: 0.85      (calculated from rule strength)
└── reasoning: "Undervalued with strong fundamentals"

    ↓

OUTPUT: Investment Signal
```

**Transparency: 100%**
- ✅ All rules visible in code
- ✅ All calculations explicit
- ✅ Deterministic (same input = same output)
- ✅ Fully auditable

---

## LLM-Powered Agent Flow (AI Processing)

```
INPUT: Financial Data
├── pe_ratio: 28.5
├── roe: 147%
└── revenue_growth: 11.2%

    ↓

DATA FORMATTING (Visible in Code)
Converts to human-readable text:

"Apple Inc. (AAPL)
 PE Ratio: 28.5
 ROE: 147%
 Revenue Growth: 11.2%
 Debt-to-Equity: 2.1"

    ↓

PROMPT CONSTRUCTION (Visible in Code)

System Prompt: "You are a value investor like Warren Buffett..."
User Prompt: "Analyze AAPL: [formatted data]
              Format: DIRECTION|CONFIDENCE|REASONING"

    ↓

LLM API CALL (External AI - Logged)
→ Sent to: Ollama/OpenAI/Anthropic
→ Via: HTTPS encrypted
→ Logged: Yes (can enable DEBUG logging)

    ↓

AI RESPONSE (Raw Output - Logged)
"bullish|75|Strong competitive moat with durable brand equity"

    ↓

RESPONSE PARSING (Visible in Code)
├── Split by "|"
├── direction = "bullish"
├── confidence = 0.75
└── reasoning = "Strong competitive moat..."

    ↓

VALIDATION (Visible in Code)
├── direction in ['bullish','bearish','neutral']? ✅
├── 0.0 <= confidence <= 1.0? ✅
└── reasoning non-empty? ✅

    ↓

OUTPUT: Investment Signal
```

**Transparency: High**
- ✅ Prompt construction visible
- ✅ AI response logged
- ✅ Parsing logic explicit
- ⚠️ AI reasoning process is opaque (neural network)

**What you can audit:**
- Exact prompt sent to AI
- Raw AI response
- How response is parsed

---

## Multi-Agent System Flow

```
INPUT: Ticker "AAPL"
    ↓
┌────────────────────────────────────┐
│ Fetch Data (Single Database Call) │
└────────────────────────────────────┘
    ↓
    Data distributed to all agents
    ↓ ↓ ↓ ↓ (Parallel - Simultaneous)
    │ │ │ │
┌───┘ │ │ └────┐
│     │ │      │
▼     ▼ ▼      ▼

ValueAgent   GrowthAgent   QualityAgent   MomentumAgent
    │            │              │              │
    │ Analyze    │ Analyze      │ Analyze      │ Analyze
    │ 0.5s       │ 0.6s         │ 2.1s (LLM)   │ 0.4s
    │            │              │              │
    ▼            ▼              ▼              ▼
  Bullish      Bearish        Bullish        Neutral
   80%          70%            85%            60%

    │            │              │              │
    └────────────┴──────────────┴──────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│ Consensus Calculation                        │
│ (Your Chosen Strategy - Explicit in Code)    │
│                                              │
│ Strategy: Weighted Consensus                 │
│ • ValueAgent:    Bullish 80% × 0.35 = +0.28 │
│ • GrowthAgent:   Bearish 70% × 0.25 = -0.18 │
│ • QualityAgent:  Bullish 85% × 0.30 = +0.26 │
│ • MomentumAgent: Neutral 60% × 0.10 = +0.00 │
│                                              │
│ Total Score: +0.36 (bullish)                 │
│ Confidence: 0.36 (moderate)                  │
└──────────────────────────────────────────────┘
    ↓
OUTPUT: Consensus Signal + All Individual Signals
{
  "consensus": {
    "direction": "bullish",
    "confidence": 0.65,
    "reasoning": "Weighted consensus from 4 agents"
  },
  "individual_signals": {
    "value":    {"direction": "bullish", "confidence": 0.80, "reasoning": "..."},
    "growth":   {"direction": "bearish", "confidence": 0.70, "reasoning": "..."},
    "quality":  {"direction": "bullish", "confidence": 0.85, "reasoning": "..."},
    "momentum": {"direction": "neutral", "confidence": 0.60, "reasoning": "..."}
  },
  "agreement_level": 0.50  (50% agreement - agents split)
}
```

**Transparency: Complete**
- ✅ All agents shown
- ✅ Each signal preserved
- ✅ Consensus formula explicit
- ✅ Weights visible
- ✅ Agreement level calculated
- ✅ Users can override if they disagree

---

## GUI Data Flow

```
USER ACTION: Create Agent
    ↓
GUI FORM INPUT
├── Agent Name: "My Value Agent"
├── PE Threshold: "15"
└── Confidence: "0.8"

    ↓

INPUT SANITIZATION (Security)
├── Sanitize name: "MyValueAgent" (remove special chars)
├── Validate number: 15.0 (convert to float)
└── Escape description (prevent code injection)

    ↓

CODE GENERATION (Template-Based)
Generates Python code using templates with sanitized values

    ↓

CODE PREVIEW (Shown to User)
User sees complete generated code before saving

    ↓

USER SAVES (Explicit Action)
File written to examples/my_value_agent.py

---

USER ACTION: Test Agent
    ↓

SELECT AGENT & DATA
├── Agent: MyValueAgent
├── Data: Mock/YFinance/Database
└── Ticker: AAPL

    ↓

LOAD AGENT (Dynamic Import)
Import examples/my_value_agent.py

    ↓

EXECUTE ANALYSIS
signal = await agent.analyze('AAPL', data)

    ↓

DISPLAY RESULTS
├── Signal: Bullish 🟢
├── Confidence: 85%
├── Reasoning: "Undervalued..."
└── Execution Time: 0.15s
```

**Transparency:**
- ✅ User controls all inputs
- ✅ Code shown before saving
- ✅ Data source is explicit
- ✅ All results displayed

---

## Database Query Flow

```
Agent calls: db.get_fundamentals('AAPL')
    ↓
┌──────────────────────────────────────┐
│ SQL Query (Logged if DEBUG enabled) │
│                                      │
│ SELECT ticker, pe_ratio, roe,        │
│        profit_margin, revenue_growth,│
│        debt_to_equity, ...           │
│ FROM fundamentals                    │
│ WHERE ticker = 'AAPL'                │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│ Database Result                      │
│                                      │
│ {                                    │
│   'ticker': 'AAPL',                  │
│   'pe_ratio': 28.5,                  │
│   'roe': 147.0,                      │
│   'profit_margin': 25.8,             │
│   ...                                │
│ }                                    │
└──────────────────────────────────────┘
    ↓
Returned to agent as Python dict
```

**Transparency:**
- ✅ SQL queries can be logged
- ✅ Results are plain Python dicts
- ✅ No data transformation (except type conversion)
- ✅ Connection pooling is transparent

---

## Error & Fallback Flow

```
Agent Execution
    ↓
TRY: Normal Analysis
│
├─ Success ──→ Return Signal
│
└─ Error ────→ Error Detection
                    ↓
            ┌───────────────────┐
            │ Classify Error    │
            │ - LLM unavailable │
            │ - Invalid data    │
            │ - Timeout         │
            │ - Network error   │
            └───────────────────┘
                    ↓
            ┌───────────────────┐
            │ Generate Fallback │
            │                   │
            │ Signal(           │
            │   'neutral',      │
            │   0.3,            │
            │   'Error: [type]' │
            │ )                 │
            └───────────────────┘
                    ↓
            User sees error with solution
```

**Transparency:**
- ✅ Error type shown
- ✅ Fallback behavior documented
- ✅ User knows when normal processing failed
- ✅ Solution provided

---

## Confidence Score Transparency

### How Confidence is Calculated

**Rule-Based (Formula in Code):**
```python
# Example from generated agent
margin = abs(value - threshold) / threshold
confidence = 0.6 + (margin * 0.3)  # 60-90% range

# Specific example:
# PE=10, threshold=15
# margin = (15-10)/15 = 0.33 (33% below)
# confidence = 0.6 + (0.33 * 0.3) = 0.70 (70%)
```

**LLM-Powered (AI Provides):**
```python
# AI includes confidence in response
response = "bullish|75|..."
            confidence ↑

# Framework validates:
conf = float(75) / 100  # 0.75
if conf < 0 or conf > 1:
    conf = 0.5  # Fallback
```

**Consensus (Weighted Average):**
```python
# Formula visible in orchestrator code
weighted_score = sum(
    weight[agent] * signal.confidence * direction_multiplier
    for agent, signal in signals.items()
)

# Direction multiplier:
# bullish: +1
# bearish: -1  
# neutral: 0
```

---

## Data Sources Transparency

### Mock Data (GUI)

```
User inputs in form:
├── PE Ratio: 15.0       (user types this)
├── ROE: 20.0            (user types this)
└── Revenue Growth: 12.0 (user types this)

Data passed to agent AS-IS (no transformation)
```

**Transparency: 100%** - User creates the data

---

### YFinance (Real Market Data)

```
Request to Yahoo Finance API
    ↓
yfinance.Ticker('AAPL').info
    ↓
Response (example fields):
{
  'trailingPE': 28.5,
  'returnOnEquity': 1.47,  (147%)
  'revenueGrowth': 0.112,  (11.2%)
  ...
}
    ↓
Conversion (visible in code):
{
  'pe_ratio': 28.5,        (direct copy)
  'roe': 147.0,            (multiply by 100)
  'revenue_growth': 11.2,  (multiply by 100)
  ...
}
```

**Transparency: High**
- ✅ Source: Yahoo Finance (public API)
- ✅ Conversion formulas shown in code
- ✅ Raw data can be logged
- ⚠️ Yahoo Finance data quality (external)

---

### Database (PostgreSQL)

```
SQL Query:
SELECT ticker, pe_ratio, roe, profit_margin, ...
FROM fundamentals
WHERE ticker = 'AAPL'

Result:
{
  'ticker': 'AAPL',
  'pe_ratio': 28.5,
  'roe': 147.0,
  ...
}
```

**Transparency: High**
- ✅ SQL queries loggable
- ✅ Sample data source is seed_data.py (visible)
- ✅ Database schema in schema.sql
- ⚠️ Production data depends on source

---

## Summary

### Transparency Levels

**100% Transparent:**
- Rule-Based agents (pure logic)
- Mock data (user-created)
- Consensus calculations (explicit formulas)

**High Transparency:**
- Database queries (SQL is loggable)
- LLM prompts (visible in code)
- LLM responses (logged)
- Data conversions (formulas in code)

**Partial Transparency:**
- LLM reasoning (AI black box)
- Embedding generation (neural network)

### For Maximum Transparency

```bash
# Enable DEBUG logging
echo "LOG_LEVEL=DEBUG" >> .env

# All data flows will be logged:
# - Database queries
# - LLM prompts
# - LLM responses
# - Signal generation
```

### For thesis-ai

The multi-agent orchestrator should:
- ✅ Log all individual agent signals
- ✅ Show consensus calculation
- ✅ Preserve all reasoning
- ✅ Track data sources
- ✅ Enable full audit trail

---

**Complete transparency - users see exactly what's happening!** 🔍

For multi-agent orchestration details, see: [MULTI_AGENT_SYSTEMS.md](MULTI_AGENT_SYSTEMS.md)
