"""FastAPI REST API for frontend integration."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

from .database import MockDatabase


# Pydantic models for API
class SignalResponse(BaseModel):
    """API response for signals."""
    direction: str
    confidence: float
    reasoning: str
    timestamp: datetime
    metadata: Dict[str, Any] = {}


class AnalysisRequest(BaseModel):
    """API request for analysis."""
    agent_name: str
    ticker: str
    parameters: Dict[str, Any] = {}


class TickerData(BaseModel):
    """Complete ticker data response."""
    ticker: str
    fundamentals: Dict[str, Any]
    prices: List[Dict[str, Any]]
    news: List[Dict[str, str]]


# Create FastAPI app
app = FastAPI(
    title="AI Agent Framework API",
    description="REST API for AI agent financial analysis",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global database instance
db = MockDatabase()

# Global agent registry
_agents: Dict[str, Any] = {}


@app.get("/")
def root():
    """API health check."""
    return {
        "status": "online",
        "framework": "AI Agent Framework",
        "version": "1.0.0"
    }


@app.get("/tickers", response_model=List[str])
def list_tickers():
    """List all available tickers."""
    return db.list_tickers()


@app.get("/tickers/{ticker}", response_model=TickerData)
def get_ticker_data(ticker: str, days: int = 30):
    """Get complete data for a ticker.
    
    Args:
        ticker: Stock ticker symbol
        days: Number of days of price history
    """
    if ticker not in db.list_tickers():
        raise HTTPException(status_code=404, detail=f"Ticker {ticker} not found")
    
    return TickerData(
        ticker=ticker,
        fundamentals=db.get_fundamentals(ticker),
        prices=db.get_prices(ticker, days),
        news=db.get_news(ticker)
    )


@app.get("/agents", response_model=List[str])
def list_agents():
    """List all registered agents."""
    return list(_agents.keys())


@app.post("/agents/register")
def register_agent(name: str, agent_class: str):
    """Register an agent dynamically.
    
    Args:
        name: Agent name
        agent_class: Python path to agent class
    """
    # This would import and instantiate the agent
    # Simplified for framework demonstration
    return {"status": "registered", "agent": name}


@app.post("/analyze", response_model=SignalResponse)
def analyze(request: AnalysisRequest):
    """Run agent analysis on ticker.
    
    Args:
        request: Analysis request with agent name and ticker
    """
    # Get agent
    agent = _agents.get(request.agent_name)
    if not agent:
        raise HTTPException(
            status_code=404,
            detail=f"Agent {request.agent_name} not found"
        )
    
    # Get data
    if request.ticker not in db.list_tickers():
        raise HTTPException(
            status_code=404,
            detail=f"Ticker {request.ticker} not found"
        )
    
    data = db.get_fundamentals(request.ticker)
    
    # Run analysis
    try:
        signal = agent.analyze(request.ticker, data)
        return SignalResponse(
            direction=signal.direction,
            confidence=signal.confidence,
            reasoning=signal.reasoning,
            timestamp=signal.timestamp,
            metadata=signal.metadata
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@app.get("/health")
def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "database": "connected",
        "agents": len(_agents),
        "tickers": len(db.list_tickers())
    }


def register_agent_instance(name: str, agent):
    """Register an agent instance for API access.
    
    Args:
        name: Agent name
        agent: Agent instance
    """
    _agents[name] = agent