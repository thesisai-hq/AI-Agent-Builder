"""FastAPI application"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting API...")
    from agent_builder.core.database import DatabasePool, Database
    from agent_builder.agents.registry import get_registry
    
    app.state.pool = DatabasePool(app.state.config.database)
    app.state.pool.create_tables()
    app.state.db = Database(app.state.pool)
    app.state.registry = get_registry()
    
    try:
        from examples.register_agents import register_all_agents
        register_all_agents()
        stats = app.state.registry.stats()
        logger.info(f"✅ {stats['total']} agents registered ({stats['enabled']} enabled)")
    except ImportError:
        logger.warning("⚠️  No agents found (run setup_3_agents.py)")
    
    yield
    
    app.state.pool.close()
    logger.info("✅ Shutdown complete")


def create_app(config=None):
    from agent_builder.core.config import Config
    from agent_builder.api.routes import create_router
    
    if config is None:
        config = Config.from_env()
    
    app = FastAPI(
        title="AI Agent Builder API",
        description="Multi-agent stock analysis system",
        version="1.0.0",
        lifespan=lifespan
    )
    app.state.config = config
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(create_router())
    return app
