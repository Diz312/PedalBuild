"""
PedalBuild FastAPI Backend Server

Main application entry point with:
- REST API routes
- CORS configuration
- Error handling
- Request logging
- Health check endpoints
"""

import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

from .db import get_database, DatabaseError

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
TYPES_FILE = PROJECT_ROOT / "src" / "models" / "types.generated.ts"


# Response models
class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    database: str
    timestamp: float


class ErrorResponse(BaseModel):
    """Error response."""

    error: str
    detail: str | None = None
    timestamp: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Runs on startup and shutdown.
    """
    # Startup
    logger.info("Starting PedalBuild backend server...")

    # Verify database connection
    try:
        db = get_database()
        if not db.check_health():
            raise DatabaseError("Database health check failed")
        logger.info("Database connection verified")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise

    logger.info("PedalBuild backend server started successfully")

    yield

    # Shutdown
    logger.info("Shutting down PedalBuild backend server...")


# Create FastAPI app
app = FastAPI(
    title="PedalBuild API",
    description="Backend API for PedalBuild - Guitar Pedal Building Workflow",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://localhost:3001",  # Alternative dev port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests with timing."""
    start_time = time.time()

    # Process request
    response = await call_next(request)

    # Calculate duration
    duration_ms = (time.time() - start_time) * 1000

    # Log request
    logger.info(
        f"{request.method} {request.url.path} - {response.status_code} - {duration_ms:.2f}ms"
    )

    return response


# Global exception handler
@app.exception_handler(DatabaseError)
async def database_error_handler(request: Request, exc: DatabaseError):
    """Handle database errors."""
    logger.error(f"Database error on {request.url.path}: {exc}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Database Error",
            detail=str(exc),
            timestamp=time.time(),
        ).model_dump(),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            detail=None,
            timestamp=time.time(),
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions."""
    logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal Server Error",
            detail=str(exc) if logger.level == logging.DEBUG else None,
            timestamp=time.time(),
        ).model_dump(),
    )


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.

    Returns:
        Server and database health status
    """
    db = get_database()
    db_healthy = db.check_health()

    return HealthResponse(
        status="healthy" if db_healthy else "degraded",
        database="connected" if db_healthy else "disconnected",
        timestamp=time.time(),
    )


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "PedalBuild API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
    }


# Serve auto-generated TypeScript types
@app.get("/api/types")
async def get_types():
    """
    Serve auto-generated TypeScript types.

    Returns:
        TypeScript type definitions file
    """
    if not TYPES_FILE.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="TypeScript types file not found. Run 'npm run generate:types' first.",
        )

    return FileResponse(
        TYPES_FILE,
        media_type="text/typescript",
        filename="types.generated.ts",
    )


# Import and register route modules
try:
    from .routes import inventory, bom, import_routes

    app.include_router(inventory.router, prefix="/api/inventory", tags=["Inventory"])
    app.include_router(bom.router, prefix="/api/bom", tags=["BOM"])
    app.include_router(import_routes.router, prefix="/api/import", tags=["Import"])

    logger.info("API routes registered successfully")

except ImportError as e:
    logger.warning(f"Some route modules not yet implemented: {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
