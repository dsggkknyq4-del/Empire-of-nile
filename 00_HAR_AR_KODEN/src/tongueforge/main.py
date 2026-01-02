from fastapi import FastAPI
from contextlib import asynccontextmanager

from ..shared.core.config import settings
from ..shared.core.logging import configure_logging, logger
from ..shared.db.base import engine, Base
from ..shared.core.middleware import GeoBlockMiddleware

from .api import chat

# Lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("TONGUEFORGE_STARTUP")
    
    # Initialize DB (Auto-create tables)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield
    logger.info("TONGUEFORGE_SHUTDOWN")

app = FastAPI(
    title="TongueForge API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Middleware
app.add_middleware(GeoBlockMiddleware, blocked_countries=["SE"])

# Routers
app.include_router(chat.router, prefix="/api", tags=["Chat"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "tongueforge"}
