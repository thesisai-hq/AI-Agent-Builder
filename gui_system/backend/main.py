"""Main FastAPI application for GUI system."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from .models import HealthResponse
from .routes import agents, templates, analysis, formulas
from .config import settings


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
@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint.
    
    Returns:
        System health status
    """
    return HealthResponse(
        status="healthy",
        version=settings.api_version,
        timestamp=datetime.now()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
