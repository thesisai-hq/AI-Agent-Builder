"""Main FastAPI application for GUI system."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from .models import HealthResponse
from .routes import agents, templates, analysis, formulas


# Create FastAPI app
app = FastAPI(
    title="AI Agent Builder - GUI System",
    description="Web-based GUI for creating and managing AI investment agents",
    version="1.0.0"
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:5174",  # Backup port
        "http://localhost:4173",  # Vite preview
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:4173",
    ],
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
        "message": "AI Agent Builder - GUI System",
        "version": "1.0.0",
        "docs": "/docs",
        "frontend": "http://localhost:5173"
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
        version="1.0.0",
        timestamp=datetime.now()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
