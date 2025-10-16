# API Reference

## Base URL

```
http://localhost:8000
```

## Authentication

Currently no authentication (v0.1.0). Coming in v0.2.0.

## Endpoints

### GET /

Get API information

**Response:**
```json
{
  "name": "AI Agent Builder API",
  "version": "0.6.0",
  "agents": {
    "total_agents": 10,
    "enabled_agents": 10
  }
}
```

---

### GET /health

Health check

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-10-15T18:30:00",
  "agents": {
    "total_agents": 10,
    "enabled_agents": 10
  }
}
```

---

### GET /agents

List all registered agents

**Query Parameters:**
- `enabled` (optional) - Filter by enabled status

**Response:**
```json
{
  "agents": [
    {
      "id": "pe_ratio_agent",
      "name": "PE Ratio Agent",
      "weight": 0.12,
      "enabled": true,
      "tags": ["basic", "valuation"],
      "type": "SimpleAgent"
    }
  ],
  "total": 10
}
```

---

### GET /agents/{agent_id}

Get agent metadata

**Response:**
```json
{
  "id": "pe_ratio_agent",
  "name": "PE Ratio Agent",
  "weight": 0.12,
  "enabled": true,
  "tags": ["basic", "valuation"]
}
```

---

### POST /agents/{agent_id}/enable

Enable an agent

**Response:**
```json
{
  "status": "enabled",
  "agent_id": "pe_ratio_agent"
}
```

---

### POST /agents/{agent_id}/disable

Disable an agent

**Response:**
```json
{
  "status": "disabled",
  "agent_id": "pe_ratio_agent"
}
```

---

### POST /analyze

Run multi-agent analysis

**Request Body:**
```json
{
  "ticker": "AAPL",
  "agent_ids": ["pe_ratio_agent", "roe_agent"]  // optional
}
```

**Response (202 Accepted):**
```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending"
}
```

---

### GET /analyze/{analysis_id}

Get analysis results

**Response:**
```json
{
  "id": "550e8400-...",
  "ticker": "AAPL",
  "status": "completed",
  "signals": [
    {
      "agent_name": "PE Ratio Agent",
      "signal_type": "bullish",
      "confidence": 0.85,
      "reasoning": "PE Ratio Agent analysis",
      "timestamp": "2024-10-15T18:30:00"
    }
  ],
  "consensus": {
    "signal": "bullish",
    "confidence": 0.82,
    "agreement": 0.75,
    "distribution": {
      "bullish": 7,
      "neutral": 2,
      "bearish": 1
    }
  },
  "started_at": "2024-10-15T18:30:00",
  "completed_at": "2024-10-15T18:30:01"
}
```

## Status Codes

- `200` - Success
- `202` - Accepted (async operation)
- `404` - Not found
- `500` - Server error

## Rate Limits

No rate limiting in v0.1.0. Coming in v0.2.0.

## Interactive Documentation

Visit http://localhost:8000/docs for interactive Swagger UI where you can test all endpoints.