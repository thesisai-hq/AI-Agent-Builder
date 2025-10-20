"""API routes with LLM and RAG endpoints"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================


class AnalyzeRequest(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=5)
    agent_ids: Optional[List[str]] = None

    @field_validator("ticker")
    @classmethod
    def validate_ticker(cls, v):
        from agent_builder.core.security import Validator

        return Validator.ticker(v)


class LLMRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=10000)
    system_prompt: Optional[str] = Field(None, max_length=5000)
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(1000, ge=1, le=4000)
    provider: str = Field("ollama", description="ollama, openai, or anthropic")
    model: Optional[str] = Field(
        None, description="Model name (uses default if not specified)"
    )


class LLMResponse(BaseModel):
    content: str
    model: str
    provider: str
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class RAGIndexRequest(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=5)
    embedding: str = Field(
        "sentence-transformers", description="simple, sentence-transformers, or ollama"
    )
    vectorstore: str = Field("faiss", description="memory, chroma, or faiss")
    force_reindex: bool = Field(
        False, description="Force re-indexing even if already indexed"
    )

    @field_validator("ticker")
    @classmethod
    def validate_ticker(cls, v):
        from agent_builder.core.security import Validator

        return Validator.ticker(v)


class RAGSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    ticker: Optional[str] = Field(None, min_length=1, max_length=5)
    top_k: int = Field(3, ge=1, le=10)
    embedding: str = Field(
        "sentence-transformers", description="simple, sentence-transformers, or ollama"
    )
    vectorstore: str = Field("faiss", description="memory, chroma, or faiss")

    @field_validator("ticker")
    @classmethod
    def validate_ticker(cls, v):
        if v:
            from agent_builder.core.security import Validator

            return Validator.ticker(v)
        return v


class RAGSearchResult(BaseModel):
    text: str
    metadata: Dict[str, Any]
    similarity: float


class RAGAnalysisRequest(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=5)
    query: str = Field(..., min_length=1, max_length=1000)
    use_llm: bool = Field(True, description="Use LLM for analysis")
    llm_provider: str = Field("ollama", description="ollama, openai, or anthropic")
    embedding: str = Field("sentence-transformers")
    vectorstore: str = Field("faiss")

    @field_validator("ticker")
    @classmethod
    def validate_ticker(cls, v):
        from agent_builder.core.security import Validator

        return Validator.ticker(v)


# ============================================================================
# ROUTER FACTORY
# ============================================================================


def create_router():
    router = APIRouter()

    # ========================================================================
    # EXISTING ROUTES
    # ========================================================================

    @router.get("/")
    async def root(request: Request):
        return {
            "name": "AI Agent Builder API",
            "version": "1.0.0",
            "agents": request.app.state.registry.stats(),
            "docs": "/docs",
            "endpoints": {
                "agents": "/agents",
                "analyze": "/analyze",
                "llm": "/llm/*",
                "rag": "/rag/*",
            },
        }

    @router.get("/health")
    async def health(request: Request):
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "database": (
                "connected"
                if request.app.state.config.database.is_postgres
                else "memory"
            ),
        }

    @router.get("/agents")
    async def list_agents(request: Request):
        registry = request.app.state.registry
        agents = []
        for aid in registry.list_all():
            meta = registry.get_metadata(aid)
            if meta:
                agents.append(
                    {
                        "id": meta.id,
                        "name": meta.name,
                        "description": meta.description,
                        "weight": meta.weight,
                        "enabled": meta.enabled,
                        "tags": meta.tags,
                    }
                )
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
    async def analyze(
        request: Request, req: AnalyzeRequest, background_tasks: BackgroundTasks
    ):
        analysis_id = str(uuid.uuid4())
        data = {
            "id": analysis_id,
            "ticker": req.ticker,
            "status": "pending",
            "signals": [],
            "consensus": None,
            "error": None,
            "started_at": datetime.now().isoformat(),
            "completed_at": None,
        }
        request.app.state.db.save_analysis(data)
        background_tasks.add_task(
            execute_analysis,
            request.app.state.registry,
            request.app.state.db,
            analysis_id,
            req.ticker,
            req.agent_ids,
        )
        return {"analysis_id": analysis_id, "status": "pending"}

    @router.get("/analyze/{analysis_id}")
    async def get_analysis(request: Request, analysis_id: str):
        analysis = request.app.state.db.get_analysis(analysis_id)
        if not analysis:
            raise HTTPException(404, "Analysis not found")
        return analysis

    # ========================================================================
    # NEW LLM ROUTES
    # ========================================================================

    @router.get("/llm/providers")
    async def list_llm_providers():
        """List available LLM providers and their status"""
        from agent_builder.llm import get_llm_provider

        providers = {}

        # Check Ollama
        try:
            ollama = get_llm_provider("ollama")
            providers["ollama"] = {
                "available": ollama.is_available() if ollama else False,
                "models": ["llama3.2", "llama3.1", "mistral", "codellama"],
                "description": "Local LLM inference",
                "setup": "ollama serve && ollama pull llama3.2",
            }
        except Exception as e:
            providers["ollama"] = {"available": False, "error": str(e)}

        # Check OpenAI
        try:
            openai = get_llm_provider("openai")
            providers["openai"] = {
                "available": openai.is_available() if openai else False,
                "models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
                "description": "OpenAI GPT models",
                "setup": "Set OPENAI_API_KEY environment variable",
            }
        except Exception as e:
            providers["openai"] = {"available": False, "error": str(e)}

        # Check Anthropic
        try:
            anthropic = get_llm_provider("anthropic")
            providers["anthropic"] = {
                "available": anthropic.is_available() if anthropic else False,
                "models": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
                "description": "Anthropic Claude models",
                "setup": "Set ANTHROPIC_API_KEY environment variable",
            }
        except Exception as e:
            providers["anthropic"] = {"available": False, "error": str(e)}

        return {"providers": providers}

    @router.post("/llm/generate", response_model=LLMResponse)
    async def llm_generate(req: LLMRequest):
        """Generate text using LLM"""
        from agent_builder.llm import get_llm_provider

        try:
            # Get LLM provider
            llm = get_llm_provider(req.provider, model=req.model)

            if not llm:
                raise HTTPException(400, f"Provider '{req.provider}' not available")

            if not llm.is_available():
                raise HTTPException(
                    503, f"Provider '{req.provider}' is not running or configured"
                )

            # Generate
            response = llm.generate(
                prompt=req.prompt,
                system_prompt=req.system_prompt,
                temperature=req.temperature,
                max_tokens=req.max_tokens,
            )

            return LLMResponse(
                content=response.content,
                model=response.model,
                provider=response.provider,
                prompt_tokens=response.prompt_tokens,
                completion_tokens=response.completion_tokens,
                total_tokens=response.total_tokens,
            )

        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            raise HTTPException(500, f"LLM generation failed: {str(e)}")

    @router.post("/llm/analyze-stock")
    async def llm_analyze_stock(
        request: Request,
        ticker: str = Field(..., min_length=1, max_length=5),
        provider: str = Field("ollama"),
        model: Optional[str] = None,
    ):
        """Analyze a stock using LLM with fundamental data"""
        from agent_builder.llm import get_llm_provider, PromptTemplates
        from agent_builder.agents.context import AgentContext
        from agent_builder.core.security import Validator

        ticker = Validator.ticker(ticker)

        try:
            # Get LLM
            llm = get_llm_provider(provider, model=model)
            if not llm or not llm.is_available():
                raise HTTPException(503, f"LLM provider '{provider}' not available")

            # Get data
            context = AgentContext(ticker, request.app.state.db)
            fundamentals = context.get_fundamentals()

            if not fundamentals:
                raise HTTPException(404, f"No data found for {ticker}")

            # Create prompt
            prompt = PromptTemplates.fundamental_analysis(ticker, fundamentals)
            system = PromptTemplates.ANALYST_SYSTEM

            # Generate
            response = llm.generate(prompt, system, temperature=0.3, max_tokens=500)

            # Parse
            parsed = PromptTemplates.parse_llm_response(response.content)

            return {
                "ticker": ticker,
                "signal": parsed["signal"],
                "confidence": parsed["confidence"],
                "reasoning": parsed["reasoning"],
                "model": response.model,
                "provider": response.provider,
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Stock analysis error: {e}")
            raise HTTPException(500, str(e))

    # ========================================================================
    # NEW RAG ROUTES
    # ========================================================================

    @router.get("/rag/configurations")
    async def list_rag_configurations():
        """List available RAG configurations"""
        return {
            "embeddings": {
                "simple": {
                    "description": "Hash-based embeddings (no dependencies)",
                    "quality": "⭐",
                    "speed": "⚡⚡⚡",
                    "setup": "Built-in, no installation needed",
                },
                "sentence-transformers": {
                    "description": "Semantic embeddings (recommended)",
                    "quality": "⭐⭐⭐⭐⭐",
                    "speed": "⚡⚡",
                    "setup": "pip install sentence-transformers",
                },
                "ollama": {
                    "description": "Local embeddings via Ollama",
                    "quality": "⭐⭐⭐⭐",
                    "speed": "⚡",
                    "setup": "ollama pull nomic-embed-text",
                },
            },
            "vectorstores": {
                "memory": {
                    "description": "In-memory storage (no persistence)",
                    "persistent": False,
                    "speed": "⚡⚡⚡",
                    "setup": "Built-in, no installation needed",
                },
                "chroma": {
                    "description": "ChromaDB (persistent storage)",
                    "persistent": True,
                    "speed": "⚡⚡",
                    "setup": "pip install chromadb",
                },
                "faiss": {
                    "description": "FAISS (high performance)",
                    "persistent": False,
                    "speed": "⚡⚡⚡",
                    "setup": "pip install faiss-cpu",
                },
            },
            "recommended": {
                "testing": "embedding=simple, vectorstore=memory",
                "production": "embedding=sentence-transformers, vectorstore=faiss",
                "persistent": "embedding=sentence-transformers, vectorstore=chroma",
            },
        }

    @router.post("/rag/index")
    async def rag_index(request: Request, req: RAGIndexRequest):
        """Index SEC filings for semantic search"""
        from agent_builder.rag import RAGEngine

        try:
            # Create RAG engine
            rag = RAGEngine(
                db=request.app.state.db,
                embedding=req.embedding,
                vectorstore=req.vectorstore,
            )

            # Index SEC filings
            rag.index_sec_filings(req.ticker)

            return {
                "ticker": req.ticker,
                "status": "indexed",
                "embedding": req.embedding,
                "vectorstore": req.vectorstore,
                "message": f"SEC filings for {req.ticker} indexed successfully",
            }

        except Exception as e:
            logger.error(f"RAG indexing error: {e}")
            raise HTTPException(500, f"Indexing failed: {str(e)}")

    @router.post("/rag/search", response_model=List[RAGSearchResult])
    async def rag_search(request: Request, req: RAGSearchRequest):
        """Search through SEC filings using semantic search"""
        from agent_builder.rag import RAGEngine

        try:
            # Create RAG engine
            rag = RAGEngine(
                db=request.app.state.db,
                embedding=req.embedding,
                vectorstore=req.vectorstore,
            )

            # Index first (will be cached if already indexed)
            if req.ticker:
                rag.index_sec_filings(req.ticker)

            # Search
            results = rag.search_sec_filings(
                query=req.query, ticker=req.ticker, top_k=req.top_k
            )

            # Format results
            return [
                RAGSearchResult(
                    text=r["text"], metadata=r["metadata"], similarity=r["similarity"]
                )
                for r in results
            ]

        except Exception as e:
            logger.error(f"RAG search error: {e}")
            raise HTTPException(500, f"Search failed: {str(e)}")

    @router.post("/rag/analyze")
    async def rag_analyze(request: Request, req: RAGAnalysisRequest):
        """Analyze stock using RAG + LLM"""
        from agent_builder.rag import RAGEngine
        from agent_builder.llm import get_llm_provider, PromptTemplates

        try:
            # Create RAG engine
            rag = RAGEngine(
                db=request.app.state.db,
                embedding=req.embedding,
                vectorstore=req.vectorstore,
            )

            # Index and search
            rag.index_sec_filings(req.ticker)
            results = rag.search_sec_filings(
                query=req.query, ticker=req.ticker, top_k=3
            )

            if not results:
                return {
                    "ticker": req.ticker,
                    "query": req.query,
                    "signal": "neutral",
                    "confidence": 0.3,
                    "reasoning": "No relevant SEC filing data found",
                    "sources": [],
                }

            # Build context
            context_text = "\n\n".join(
                [f"[Excerpt {i+1}] {r['text']}" for i, r in enumerate(results)]
            )

            # Use LLM if requested
            if req.use_llm:
                llm = get_llm_provider(req.llm_provider)

                if not llm or not llm.is_available():
                    return {
                        "ticker": req.ticker,
                        "query": req.query,
                        "signal": "neutral",
                        "confidence": 0.5,
                        "reasoning": f"LLM provider '{req.llm_provider}' not available",
                        "context": context_text,
                        "sources": [r["metadata"] for r in results],
                    }

                # Generate analysis
                prompt = f"""Based on the following SEC filing excerpts for {req.ticker}, analyze the company's outlook regarding: {req.query}

{context_text}

Provide your analysis in this format:
SIGNAL: [BULLISH/BEARISH/NEUTRAL]
CONFIDENCE: [0.0-1.0]
REASONING: [Your analysis]"""

                response = llm.generate(
                    prompt=prompt,
                    system_prompt=PromptTemplates.ANALYST_SYSTEM,
                    temperature=0.3,
                    max_tokens=500,
                )

                parsed = PromptTemplates.parse_llm_response(response.content)

                return {
                    "ticker": req.ticker,
                    "query": req.query,
                    "signal": parsed["signal"],
                    "confidence": parsed["confidence"],
                    "reasoning": parsed["reasoning"],
                    "model": response.model,
                    "provider": response.provider,
                    "sources": [r["metadata"] for r in results],
                }

            # Without LLM, just return context
            avg_similarity = sum(r["similarity"] for r in results) / len(results)
            return {
                "ticker": req.ticker,
                "query": req.query,
                "signal": "neutral",
                "confidence": min(0.7, avg_similarity),
                "reasoning": f"Found {len(results)} relevant SEC filing excerpts",
                "context": context_text,
                "sources": [r["metadata"] for r in results],
            }

        except Exception as e:
            logger.error(f"RAG analysis error: {e}")
            raise HTTPException(500, f"Analysis failed: {str(e)}")

    @router.get("/rag/status/{ticker}")
    async def rag_status(request: Request, ticker: str):
        """Check if ticker is indexed"""
        from agent_builder.core.security import Validator

        ticker = Validator.ticker(ticker)

        # Check if SEC filings exist
        from agent_builder.rag import DataRetriever

        retriever = DataRetriever(request.app.state.db)
        filings = retriever.get_all_sec_filings(ticker)

        return {
            "ticker": ticker,
            "has_data": len(filings) > 0,
            "filing_count": len(filings),
            "filings": [
                {"type": f["filing_type"], "date": str(f["filing_date"])}
                for f in filings
            ],
        }

    return router


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def execute_analysis(registry, db, analysis_id, ticker, agent_ids):
    from agent_builder.agents.context import AgentContext

    try:
        agents = (
            [registry.get(aid) for aid in agent_ids if registry.get(aid)]
            if agent_ids
            else registry.get_enabled_agents()
        )
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
        db.save_analysis(
            {
                "id": analysis_id,
                "ticker": ticker,
                "status": "completed",
                "signals": signals,
                "consensus": consensus,
                "error": None,
                "started_at": db.get_analysis(analysis_id)["started_at"],
                "completed_at": datetime.now().isoformat(),
            }
        )
        logger.info(f"✅ Analysis {analysis_id} completed: {consensus['signal']}")
    except Exception as e:
        logger.exception(f"Analysis {analysis_id} failed")
        db.save_analysis(
            {
                "id": analysis_id,
                "ticker": ticker,
                "status": "failed",
                "signals": [],
                "consensus": None,
                "error": str(e),
                "started_at": db.get_analysis(analysis_id)["started_at"],
                "completed_at": datetime.now().isoformat(),
            }
        )


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
