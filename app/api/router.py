from fastapi import APIRouter

from app.api.routes import analytics, health, models, records

api_router = APIRouter()

# CW1 polish: keep routing in one place with consistent prefixes + tags (cleaner OpenAPI output)
api_router.include_router(health.router, tags=["health"])
api_router.include_router(models.router, prefix="/models", tags=["models"])
api_router.include_router(records.router, prefix="/models", tags=["records"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])