import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1.api_router import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("mahatwin")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="High-Fidelity 4D Digital Twin Platform of Mumbai City - Phase 1 Foundation API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["Health & Status"])
def health_check():
    return {
        "status": "healthy",
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }


@app.get("/health/database", tags=["Health & Status"])
def database_health_check():
    """Verify the configured database and required spatial/time extensions."""
    try:
        import psycopg2
        with psycopg2.connect(settings.DATABASE_URL, connect_timeout=2) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT extname FROM pg_extension WHERE extname IN ('postgis', 'timescaledb')")
                extensions = {row[0] for row in cursor.fetchall()}
        missing = {"postgis", "timescaledb"} - extensions
        if missing:
            raise HTTPException(status_code=503, detail={"status": "degraded", "missing_extensions": sorted(missing)})
        return {"status": "healthy", "extensions": sorted(extensions)}
    except HTTPException:
        raise
    except Exception as exc:
        logger.warning("Database health check failed: %s", exc)
        raise HTTPException(status_code=503, detail={"status": "unavailable", "service": "database"}) from exc

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
