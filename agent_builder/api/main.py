"""
Main FastAPI Application - WITH CONNECTION POOLING
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from contextlib import asynccontextmanager
import logging

from agent_builder.repositories.repository import Repository
from agent_builder.repositories.connection import (
    get_database_connection,
    create_tables,
    ConnectionPool,  # ← Import pool
)
from agent_builder.agents.registry import get_registry
from agent_builder.config import Config
from agent_builder.utils import generate_id
from agent_builder.security import sanitize_ticker, validate_agent_id

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown"""
    logger.info("🚀 Starting AI Agent Builder API...")

    try:
        # Initialize connection pool FIRST
        ConnectionPool.initialize()

        # Get initial connection for table creation
        db_connection = get_database_connection()
        create_tables(db_connection)

        # Return connection to pool
        ConnectionPool.return_connection(db_connection)

        # Store pool reference (for shutdown)
        app.state.pool = ConnectionPool
        app.state.repo = Repository(db_connection)
        logger.info("✅ Database connected with connection pool")

        # Initialize registry
        app.state.registry = get_registry()

        # Register agents
        try:
            from examples.register_agents import register_all_agents

            register_all_agents()
            logger.info("✅ Agents registered")
        except ImportError:
            logger.warning("⚠️  No agents to register")

        stats = app.state.registry.stats()
        logger.info(
            f"✅ Registry ready: {stats['total_agents']} agents, {stats['enabled_agents']} enabled"
        )

    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise

    yield

    # Shutdown - Close pool
    logger.info("👋 Shutting down...")
    ConnectionPool.close_all()
    logger.info("✅ Cleanup complete")


# Create app
app = FastAPI(
    title="AI Agent Builder API",
    description="Optimized with connection pooling",
    version="0.6.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global Error Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception on {request.url}: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if Config.DEBUG else "An error occurred",
            "path": str(request.url),
        },
    )


# Models
class AnalyzeRequest(BaseModel):
    ticker: str = Field(
        ..., min_length=1, max_length=5, description="Stock ticker (1-5 chars)"
    )
    agent_ids: Optional[List[str]] = Field(None, description="Specific agent IDs")

    @validator("ticker")
    def validate_ticker(cls, v):
        """Validate and sanitize ticker"""
        return sanitize_ticker(v)

    @validator("agent_ids", each_item=True)
    def validate_agent_ids(cls, v):
        """Validate each agent ID"""
        if v:
            return validate_agent_id(v)
        return v


# Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    stats = app.state.registry.stats()
    return {
        "name": "AI Agent Builder API",
        "version": "0.6.0",
        "architecture": "optimized with connection pooling",
        "storage": {
            "agents": "registry (in-memory)",
            "analyses": (
                "postgresql with connection pool" if Config.is_postgres() else "memory"
            ),
        },
        "performance": {
            "connection_pooling": Config.is_postgres(),
            "pool_size": "2-10 connections" if Config.is_postgres() else "n/a",
        },
        "agents": stats,
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected (pooled)" if Config.is_postgres() else "memory",
        "agents": app.state.registry.stats(),
    }


@app.get("/agents")
async def list_agents(enabled: Optional[bool] = None):
    """List all registered agents"""
    try:
        registry = app.state.registry
        agent_ids = registry.list_enabled() if enabled else registry.list_all()

        agents = [registry.get_metadata(aid) for aid in agent_ids]
        agents = [a for a in agents if a]

        return {"agents": agents, "total": len(agents)}

    except Exception as e:
        logger.error(f"Error listing agents: {e}")
        raise HTTPException(status_code=500, detail="Error listing agents")


@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get agent metadata"""
    meta = app.state.registry.get_metadata(agent_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Agent not found")
    return meta


@app.post("/agents/{agent_id}/enable")
async def enable_agent(agent_id: str):
    """Enable an agent"""
    if not app.state.registry.get(agent_id):
        raise HTTPException(status_code=404, detail="Agent not found")

    app.state.registry.enable(agent_id)
    logger.info(f"Enabled agent: {agent_id}")
    return {"status": "enabled", "agent_id": agent_id}


@app.post("/agents/{agent_id}/disable")
async def disable_agent(agent_id: str):
    """Disable an agent"""
    if not app.state.registry.get(agent_id):
        raise HTTPException(status_code=404, detail="Agent not found")

    app.state.registry.disable(agent_id)
    logger.info(f"Disabled agent: {agent_id}")
    return {"status": "disabled", "agent_id": agent_id}


@app.post("/analyze", status_code=202)
async def analyze(request: AnalyzeRequest, background_tasks: BackgroundTasks):
    """Run analysis - WITH INPUT VALIDATION"""
    # Ticker already validated by Pydantic
    ticker = request.ticker

    analysis_id = generate_id()

    logger.info(f"Analysis requested for {ticker} (ID: {analysis_id})")

    analysis_data = {
        "id": analysis_id,
        "ticker": ticker,
        "status": "pending",
        "signals": [],
        "consensus": None,
        "error": None,
        "started_at": datetime.now().isoformat(),
        "completed_at": None,
    }

    try:
        app.state.repo.save("analyses", analysis_data)
        logger.info(f"Created analysis {analysis_id} for {request.ticker}")
    except Exception as e:
        logger.error(f"Failed to create analysis: {e}")
        raise HTTPException(status_code=500, detail="Failed to create analysis")

    # Run in background
    background_tasks.add_task(
        execute_analysis,
        app.state.registry,
        app.state.repo,
        analysis_id,
        request.ticker,
        request.agent_ids,
    )

    return {"analysis_id": analysis_id, "status": "pending"}


def execute_analysis(
    registry, repo, analysis_id: str, ticker: str, agent_ids: Optional[List[str]] = None
):
    """Execute analysis - Uses connection pool for all DB operations"""
    try:
        logger.info(f"Executing analysis {analysis_id} for {ticker}")

        # Get agents from registry
        if agent_ids:
            agents = [registry.get(aid) for aid in agent_ids]
            agents = [a for a in agents if a]
        else:
            agents = registry.get_enabled_agents()

        if not agents:
            raise Exception("No agents available")

        logger.info(f"Running {len(agents)} agents on {ticker}")

        # Execute agents (they use pooled connections!)
        signals = []
        for agent in agents:
            try:
                signal = agent.analyze(ticker)
                signals.append(
                    {
                        "agent_name": signal.agent_name,
                        "signal_type": signal.signal_type,
                        "confidence": signal.confidence,
                        "reasoning": signal.reasoning,
                        "timestamp": signal.timestamp.isoformat(),
                    }
                )
                logger.debug(
                    f"Agent {agent.name}: {signal.signal_type} ({signal.confidence:.2f})"
                )
            except Exception as e:
                logger.error(f"Agent {agent.name} failed: {e}")

        if not signals:
            raise Exception("All agents failed to execute")

        # Calculate consensus
        consensus = calculate_consensus(signals)
        logger.info(
            f"Consensus for {ticker}: {consensus['signal']} ({consensus['confidence']:.2%})"
        )

        # Update analysis (uses pooled connection)
        analysis = repo.find_by_id("analyses", analysis_id)
        if analysis:
            analysis.update(
                {
                    "status": "completed",
                    "signals": signals,
                    "consensus": consensus,
                    "completed_at": datetime.now().isoformat(),
                }
            )
            repo.save("analyses", analysis)
            logger.info(f"Analysis {analysis_id} completed")

    except Exception as e:
        logger.error(f"Analysis {analysis_id} failed: {e}", exc_info=True)
        analysis = repo.find_by_id("analyses", analysis_id)
        if analysis:
            analysis.update(
                {
                    "status": "failed",
                    "error": str(e),
                    "completed_at": datetime.now().isoformat(),
                }
            )
            repo.save("analyses", analysis)


def calculate_consensus(signals: List[Dict]) -> Dict:
    """Calculate consensus from signals"""
    if not signals:
        return {"signal": "neutral", "confidence": 0.0, "agreement": 0.0}

    signal_counts = {}
    total_confidence = 0

    for signal in signals:
        signal_type = signal["signal_type"]
        confidence = signal["confidence"]
        signal_counts[signal_type] = signal_counts.get(signal_type, 0) + 1
        total_confidence += confidence

    majority_signal = max(signal_counts.items(), key=lambda x: x[1])
    agreement = majority_signal[1] / len(signals)
    avg_confidence = total_confidence / len(signals)

    return {
        "signal": majority_signal[0],
        "confidence": round(avg_confidence, 3),
        "agreement": round(agreement, 3),
        "distribution": signal_counts,
    }


@app.get("/analyze/{analysis_id}")
async def get_analysis(analysis_id: str):
    """Get analysis results - Uses connection pool"""
    try:
        analysis = app.state.repo.find_by_id("analyses", analysis_id)
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching analysis {analysis_id}: {e}")
        raise HTTPException(status_code=500, detail="Error fetching analysis")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=Config.API_HOST, port=Config.API_PORT, log_level="info")
