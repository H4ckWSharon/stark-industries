"""
STARK INDUSTRIES SQL — FastAPI Main Application
"""
import structlog
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database import init_db
from app.auth.router import router as auth_router
from app.challenges.router import router as challenges_router
from app.monitor.router import router as monitor_router

log = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    log.info("STARK INDUSTRIES SQL — Starting up")
    await init_db()
    log.info("Database initialized")
    yield
    log.info("STARK INDUSTRIES SQL — Shutting down")


app = FastAPI(
    title="STARK INDUSTRIES SQL",
    description=(
        "Cybersecurity Training Platform — SQL Injection Cyber Range. "
        "FOR AUTHORIZED EDUCATIONAL USE ONLY."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(challenges_router)
app.include_router(monitor_router)


@app.get("/health")
async def health():
    return {"status": "operational", "platform": "STARK INDUSTRIES SQL"}


@app.get("/")
async def root():
    return {
        "platform": "STARK INDUSTRIES SQL",
        "version": "1.0.0",
        "notice": "FOR AUTHORIZED EDUCATIONAL USE ONLY",
        "docs": "/docs",
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    log.error("Unhandled exception", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
