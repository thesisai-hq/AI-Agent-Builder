"""FastAPI REST API with dependency injection and proper error handling."""

import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .config import Config
from .database import DBConnectionError
from .database import Database, DatabaseError

# Configure logging
logging.basicConfig(level=getattr(logging, Config.get_log_level()))
logger = logging.getLogger(__name__)


# Pydantic models for API
class SignalResponse(BaseModel):
    """API response for signals."""

    direction: str
    confidence: float
    reasoning: str
    timestamp: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AnalysisRequest(BaseModel):
    """API request for analysis."""

    agent_name: str = Field(min_length=1)
    ticker: str = Field(min_length=1, max_length=10)
    parameters: Dict[str, Any] = Field(default_factory=dict)


class TickerData(BaseModel):
    """Complete ticker data response."""

    ticker: str
    fundamentals: Optional[Dict[str, Any]]
    prices: List[Dict[str, Any]]
    news: List[Dict[str, str]]


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    database: str
    agents: int
    tickers: int


class ErrorResponse(BaseModel):
    """Error response."""

    detail: str
    error_type: str


# Global agent registry (agents registered at startup)
_agents: Dict[str, Any] = {}


# Database dependency injection
async def get_db(request: Request) -> Database:
    """Dependency injection for database.

    Args:
        request: FastAPI request object

    Returns:
        Database instance from app state

    Raises:
        HTTPException: If database not available
    """
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database not available"
        )
    return db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle.

    Startup: Connect to database
    Shutdown: Disconnect from database
    """
    # Startup
    connection_string = Config.get_database_url()

    logger.info("Starting application...")
    logger.info(
        f"Connecting to database: {connection_string.split('@')[1] if '@' in connection_string else connection_string}"
    )

    db = Database(connection_string)

    try:
        await db.connect()
        app.state.db = db
        logger.info("✅ Database connected successfully")

        yield

    finally:
        # Shutdown
        logger.info("Shutting down application...")
        if hasattr(app.state, "db"):
            await app.state.db.disconnect()
            logger.info("✅ Database disconnected")


# Create FastAPI app with lifespan
app = FastAPI(
    title="AI Agent Framework API",
    description="REST API for AI agent financial analysis with PostgreSQL",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS middleware with configurable origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(DatabaseError)
async def database_exception_handler(request: Request, exc: DatabaseError):
    """Handle database errors."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(detail=str(exc), error_type="database_error").model_dump(),
    )


@app.exception_handler(DBConnectionError)
async def connection_exception_handler(request: Request, exc: DBConnectionError):
    """Handle connection errors."""
    logger.error(f"Connection error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=ErrorResponse(detail=str(exc), error_type="connection_error").model_dump(),
    )


# Routes
@app.get("/", tags=["health"])
def root():
    """API health check."""
    return {
        "status": "online",
        "framework": "AI Agent Framework",
        "version": "2.0.0",
        "database": "PostgreSQL with asyncpg",
    }


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check(db: Database = Depends(get_db)):
    """Detailed health check with database status.

    Args:
        db: Database instance (injected)

    Returns:
        Health status
    """
    try:
        db_healthy = await db.health_check()
        tickers = await db.list_tickers()

        return HealthResponse(
            status="healthy" if db_healthy else "degraded",
            database="connected" if db_healthy else "disconnected",
            agents=len(_agents),
            tickers=len(tickers),
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service unhealthy"
        )


@app.get("/tickers", response_model=List[str], tags=["data"])
async def list_tickers(db: Database = Depends(get_db)):
    """List all available tickers.

    Args:
        db: Database instance (injected)

    Returns:
        List of ticker symbols
    """
    try:
        return await db.list_tickers()
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve tickers: {str(e)}",
        )


@app.get("/tickers/{ticker}", response_model=TickerData, tags=["data"])
async def get_ticker_data(ticker: str, days: int = 30, db: Database = Depends(get_db)):
    """Get complete data for a ticker.

    Args:
        ticker: Stock ticker symbol
        days: Number of days of price history
        db: Database instance (injected)

    Returns:
        Complete ticker data

    Raises:
        HTTPException: If ticker not found
    """
    try:
        # Check if ticker exists
        tickers = await db.list_tickers()
        if ticker not in tickers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Ticker {ticker} not found"
            )

        # Get all data
        fundamentals = await db.get_fundamentals(ticker)
        prices = await db.get_prices(ticker, days)
        news = await db.get_news(ticker)

        return TickerData(ticker=ticker, fundamentals=fundamentals, prices=prices, news=news)
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve ticker data: {str(e)}",
        )


@app.get("/agents", response_model=List[str], tags=["agents"])
def list_agents():
    """List all registered agents.

    Returns:
        List of agent names
    """
    return list(_agents.keys())


@app.post("/analyze", response_model=SignalResponse, tags=["analysis"])
async def analyze(request: AnalysisRequest, db: Database = Depends(get_db)):
    """Run agent analysis on ticker.

    Args:
        request: Analysis request with agent name and ticker
        db: Database instance (injected)

    Returns:
        Analysis signal

    Raises:
        HTTPException: If agent not found or analysis fails
    """
    # Get agent
    agent = _agents.get(request.agent_name)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {request.agent_name} not found. Available: {list(_agents.keys())}",
        )

    try:
        # Check ticker exists
        tickers = await db.list_tickers()
        if request.ticker not in tickers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Ticker {request.ticker} not found"
            )

        # Get data
        data = await db.get_fundamentals(request.ticker)
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No data available for {request.ticker}",
            )

        # Run analysis (now async)
        signal = await agent.analyze(request.ticker, data)

        return SignalResponse(
            direction=signal.direction,
            confidence=signal.confidence,
            reasoning=signal.reasoning,
            timestamp=signal.timestamp,
            metadata=signal.metadata,
        )
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Analysis failed: {str(e)}"
        )


def register_agent_instance(name: str, agent):
    """Register an agent instance for API access.

    Args:
        name: Agent name (must be unique)
        agent: Agent instance

    Raises:
        ValueError: If agent name already exists
    """
    if name in _agents:
        raise ValueError(f"Agent {name} already registered")
    _agents[name] = agent
    logger.info(f"Registered agent: {name}")


def clear_agents():
    """Clear all registered agents (useful for testing)."""
    global _agents
    _agents = {}
    logger.info("Cleared all agents")
