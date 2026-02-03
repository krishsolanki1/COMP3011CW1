from fastapi import APIRouter
from app.api.routes import health, models, records, analytics

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(models.router, prefix="/models", tags=["models"])
api_router.include_router(records.router, prefix="/models", tags=["records"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
