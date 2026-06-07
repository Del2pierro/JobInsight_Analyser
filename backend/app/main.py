import logging
import logging.config
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.exceptions import (
    JobInsightException,
    generic_exception_handler,
    jobinsight_exception_handler,
)

# ---------------------------------------------------------------------------
# Structured Logging Configuration
# ---------------------------------------------------------------------------

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "json",
            }
        },
        "root": {"level": "INFO", "handlers": ["console"]},
    }
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Application Lifespan (startup / shutdown hooks)
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    FastAPI lifespan context manager.

    Startup:
      - Pre-warm the Qdrant connection and ensure collections exist.
      - Pre-load the embedding model into memory.
      - (Future) Run Alembic migrations automatically on startup.

    Shutdown:
      - Graceful cleanup of open connections.
    """
    logger.info("JobInsight AI starting up...")

    # Pre-warm singletons so the first request is not slow
    from app.services.qdrant import get_qdrant_service
    from app.services.embeddings import get_embedding_service

    get_qdrant_service()      # Opens Qdrant connection + creates collections
    get_embedding_service()   # Loads SentenceTransformer model into RAM

    logger.info("All services initialized. JobInsight AI is ready.")

    yield  # Application runs here

    logger.info("JobInsight AI shutting down. Goodbye.")


# ---------------------------------------------------------------------------
# FastAPI Application Factory
# ---------------------------------------------------------------------------

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application instance.

    Using a factory function (instead of a bare module-level `app`) enables:
    - Clean testing with different configurations.
    - Future support for multiple app instances.
    """
    app = FastAPI(
        title="JobInsight AI",
        description=(
            "Intelligent job market analysis platform powered by multi-agent AI. "
            "Collect, analyze, and match job offers using NLP, semantic search, and predictive analytics."
        ),
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # ------------------------------------------------------------------
    # CORS Middleware
    # ------------------------------------------------------------------
    # Allow the Next.js frontend (dev: localhost:3000) to communicate
    # with the backend without browser CORS blocks.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",  # Next.js dev server
            "http://localhost:3001",  # Alternate dev port
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ------------------------------------------------------------------
    # Global Exception Handlers
    # ------------------------------------------------------------------
    app.add_exception_handler(JobInsightException, jobinsight_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    # ------------------------------------------------------------------
    # API Routers (registered here, implemented in api/v1/)
    # ------------------------------------------------------------------
    from app.api.v1 import auth
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
    # app.include_router(jobs.router,     prefix="/api/v1/jobs",     tags=["Jobs"])
    # app.include_router(skills.router,   prefix="/api/v1/skills",   tags=["Skills"])
    # app.include_router(trends.router,   prefix="/api/v1/trends",   tags=["Trends"])
    # app.include_router(resumes.router,  prefix="/api/v1/resumes",  tags=["Resumes"])
    # app.include_router(matching.router, prefix="/api/v1/matching", tags=["Matching"])
    # app.include_router(reports.router,  prefix="/api/v1/reports",  tags=["Reports"])

    # ------------------------------------------------------------------
    # Health Check Endpoint
    # ------------------------------------------------------------------
    @app.get("/health", tags=["System"], summary="Application health check")
    async def health_check() -> dict:
        """
        Docker and load-balancer health probe.
        Returns 200 OK with application version when the service is alive.
        """
        return {"status": "healthy", "service": "jobinsight-ai", "version": "1.0.0"}

    return app


# ---------------------------------------------------------------------------
# Module-level app instance (used by Uvicorn)
# ---------------------------------------------------------------------------
app = create_app()
