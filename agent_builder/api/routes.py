"""API routes"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)


class AnalyzeRequest(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=5)
    agent_ids: Optional[List[str]] = None
    
    @field_validator("ticker")
    @classmethod
    def validate_ticker(cls, v):
        from agent_builder.core.security import Validator
        return Validator.ticker(v)


def create_router():
    router = APIRouter()
    
    @router.get("/")
    async def root(request: Request):
        return {
            "name": "AI Agent Builder API",
            "version": "1.0.0",
            "agents": request.app.state.registry.stats(),
            "docs": "/docs",
        }
    
    @router.get("/health")
    async def health(request: Request):
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "database": "connected" if request.app.state.config.database.is_postgres else "memory",
        }
    
    @router.get("/agents")
    async def list_agents(request: Request):
        registry = request.app.state.registry
        agents = []
        for aid in registry.list_all():
            meta = registry.get_metadata(aid)
            if meta:
                agents.append({
                    "id": meta.id, "name": meta.name, "description": meta.description,
                    "weight": meta.weight, "enabled": meta.enabled, "tags": meta.tags,
                })
        return {"agents": agents, "total": len(agents)}
    
    @router.post("/agents/{agent_id}/enable")
    async def enable_agent(request: Request, agent_id: str):
        registry = request.app.state.registry
        if not registry.get(agent_id):
            raise HTTPException(404, "Agent not found")
        registry.enable(agent_id)
        return {"status": "enabled", "agent_id": agent_id}
    
    @router.post("/agents/{agent_id}/disable")
    async def disable_agent(request: Request, agent_id: str):
        registry = request.app.state.registry
        if not registry.get(agent_id):
            raise HTTPException(404, "Agent not found")
        registry.disable(agent_id)
        return {"status": "disabled", "agent_id": agent_id}
    
    @router.post("/analyze", status_code=202)
    async def analyze(request: Request, req: AnalyzeRequest, background_tasks: BackgroundTasks):
        analysis_id = str(uuid.uuid4())
        data = {
            "id": analysis_id, "ticker": req.ticker, "status": "pending",
            "signals": [], "consensus": None, "error": None,
            "started_at": datetime.now().isoformat(), "completed_at": None,
        }
        request.app.state.db.save_analysis(data)
        background_tasks.add_task(
            execute_analysis, request.app.state.registry,
            request.app.state.db, analysis_id, req.ticker, req.agent_ids
        )
        return {"analysis_id": analysis_id, "status": "pending"}
    
    @router.get("/analyze/{analysis_id}")
    async def get_analysis(request: Request, analysis_id: str):
        analysis = request.app.state.db.get_analysis(analysis_id)
        if not analysis:
            raise HTTPException(404, "Analysis not found")
        return analysis
    
    return router


def execute_analysis(registry, db, analysis_id, ticker, agent_ids):
    from agent_builder.agents.context import AgentContext
    try:
        agents = [registry.get(aid) for aid in agent_ids if registry.get(aid)] if agent_ids else registry.get_enabled_agents()
        if not agents:
            raise Exception("No agents available")
        
        context = AgentContext(ticker, db)
        signals = []
        for agent in agents:
            try:
                signal = agent.analyze(ticker, context)
                signals.append(signal.to_dict())
            except Exception as e:
                logger.error(f"Agent {agent.name} failed: {e}")
        
        if not signals:
            raise Exception("All agents failed")
        
        consensus = calculate_consensus(signals)
        db.save_analysis({
            "id": analysis_id, "ticker": ticker, "status": "completed",
            "signals": signals, "consensus": consensus, "error": None,
            "started_at": db.get_analysis(analysis_id)["started_at"],
            "completed_at": datetime.now().isoformat(),
        })
        logger.info(f"✅ Analysis {analysis_id} completed: {consensus['signal']}")
    except Exception as e:
        logger.error(f"❌ Analysis {analysis_id} failed: {e}")
        db.save_analysis({
            "id": analysis_id, "ticker": ticker, "status": "failed",
            "signals": [], "consensus": None, "error": str(e),
            "started_at": db.get_analysis(analysis_id)["started_at"],
            "completed_at": datetime.now().isoformat(),
        })


def calculate_consensus(signals):
    if not signals:
        return {"signal": "neutral", "confidence": 0.0}
    counts = {}
    total_conf = 0
    for s in signals:
        counts[s["signal_type"]] = counts.get(s["signal_type"], 0) + 1
        total_conf += s["confidence"]
    majority = max(counts.items(), key=lambda x: x[1])
    return {
        "signal": majority[0],
        "confidence": round(total_conf / len(signals), 3),
        "agreement": round(majority[1] / len(signals), 3),
        "distribution": counts,
    }
