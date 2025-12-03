"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os

from app.config import get_settings
from app.database.connection import initialize_connection
from app.api.routes import funds, management, subfunds, share_classes, legal_entities, statistics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    neo4j_conn = initialize_connection()
    logger.info("Neo4j connection initialized")
    yield
    logger.info("Shutting down...")
    if neo4j_conn:
        neo4j_conn.close()


settings = get_settings()

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    lifespan=lifespan
)


# --------------------------
# CORS CONFIGURATION (FIXED)
# --------------------------

frontend_url = os.getenv("FRONTEND_URL")

allowed_origins = [
    frontend_url,
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(funds.router)
app.include_router(management.router)
app.include_router(subfunds.router)
app.include_router(share_classes.router)
app.include_router(legal_entities.router)
app.include_router(statistics.router)


@app.get("/")
async def root():
    return {
        "message": "Fund Referential API",
        "version": settings.api_version,
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
