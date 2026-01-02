from fastapi import FastAPI
from contextlib import asynccontextmanager

from ..shared.core.config import settings
from ..shared.core.logging import configure_logging, logger
from ..shared.db.base import engine, Base
from ..shared.core.middleware import GeoBlockMiddleware

from .api import auth, profile, analysis

# Lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("MONEYPILOT_STARTUP")
    
    # Initialize DB (Auto-create tables for MVP simplicity, usually use migrations)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield
    logger.info("MONEYPILOT_SHUTDOWN")

app = FastAPI(
    title="MoneyPilot API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Middleware
app.add_middleware(GeoBlockMiddleware, blocked_countries=["SE"])

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "moneypilot"}
