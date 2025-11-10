"""Main FastAPI application for GUI system."""

import asyncio
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from .models import HealthResponse
from .data_cache import data_cache, price_history_cache
from .storage import storage
import sys
from .routes import agents, templates, analysis, formulas, documents
from .config import settings
from .constants import CACHE_CLEANUP_INTERVAL_SECONDS

# Setup logging
logger = logging.getLogger(__name__)


# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agents.router, prefix="/api")
app.include_router(templates.router, prefix="/api")
app.include_router(analysis.router, prefix="/api")
app.include_router(formulas.router, prefix="/api")
app.include_router(documents.router, prefix="/api")  # RAG document management


# Background task for cache cleanup
async def cleanup_cache_periodically():
    """Clean up expired cache entries periodically."""
    while True:
        await asyncio.sleep(CACHE_CLEANUP_INTERVAL_SECONDS)
        try:
            removed_stock = data_cache.cleanup_expired()
            removed_price = price_history_cache.cleanup_expired()
            if removed_stock or removed_price:
                logger.info(f"Cache cleanup: removed {removed_stock} stock + {removed_price} price entries")
        except Exception as e:
            logger.error(f"Cache cleanup error: {e}")


@app.on_event("startup")
async def startup_event():
    """Start background tasks on application startup."""
    logger.info("Starting cache cleanup background task")
    asyncio.create_task(cleanup_cache_periodically())


# Cache management
@app.get("/api/cache/stats")
async def get_cache_stats():
    """Get cache statistics.
    
    Returns:
        Cache statistics for all caches
    """
    return {
        "stock_data_cache": data_cache.get_stats(),
        "price_history_cache": price_history_cache.get_stats()
    }


@app.post("/api/cache/clear")
async def clear_cache(ticker: str = None):
    """Clear data cache.
    
    Args:
        ticker: Specific ticker to clear. If None, clears all.
        
    Returns:
        Cache clear status
    """
    try:
        if ticker:
            ticker_upper = ticker.upper()
            # Clear stock data
            data_cache.clear(ticker_upper)
            # Clear all price history for this ticker (keys like "AAPL_1y_1d")
            removed_price = price_history_cache.clear_prefix(f"{ticker_upper}_")
            
            logger.info(f"Cleared cache for {ticker_upper}: {removed_price} price history entries")
        else:
            data_cache.clear()
            price_history_cache.clear()
            logger.info("Cleared all caches")
        
        return {
            "status": "success",
            "message": f"Cache cleared for {ticker}" if ticker else "All caches cleared",
            "cache_stats": {
                "stock_data": data_cache.get_stats(),
                "price_history": price_history_cache.get_stats()
            }
        }
    except Exception as e:
        logger.error(f"Cache clear error: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": settings.api_title,
        "version": settings.api_version,
        "docs": "/docs",
        "frontend": f"http://localhost:5173"
    }


# Health check
@app.get("/api/health")
async def health_check():
    """Enhanced health check endpoint with service status.
    
    Returns:
        System health status with service details
    """
    # Check services
    services = {
        "storage": _check_storage(),
        "yfinance": _check_yfinance(),
        "agent_framework": _check_agent_framework(),
        "cache": _check_cache()
    }
    
    # Overall status
    all_healthy = all(svc["status"] == "healthy" for svc in services.values())
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "version": settings.api_version,
        "timestamp": datetime.now(),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "services": services
    }


def _check_storage() -> dict:
    """Check storage system health."""
    try:
        templates = storage.list_templates()
        agents = storage.list_agents()
        return {
            "status": "healthy",
            "templates_count": len(templates),
            "agents_count": len(agents)
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


def _check_yfinance() -> dict:
    """Check yfinance module availability.
    
    Note: Does not make actual API calls to avoid slow health checks.
    """
    try:
        import yfinance as yf
        # Just verify module is importable, don't make API call
        return {
            "status": "healthy",
            "module_available": True
        }
    except ImportError as e:
        return {
            "status": "unhealthy",
            "module_available": False,
            "error": str(e)
        }


def _check_agent_framework() -> dict:
    """Check agent_framework availability."""
    try:
        import agent_framework
        from agent_framework.utils import parse_llm_signal
        return {
            "status": "healthy",
            "installed": True
        }
    except ImportError as e:
        return {
            "status": "unhealthy",
            "installed": False,
            "error": str(e)
        }


def _check_cache() -> dict:
    """Check cache system."""
    try:
        stats = data_cache.get_stats()
        return {
            "status": "healthy",
            **stats
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
