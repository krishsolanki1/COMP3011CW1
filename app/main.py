from fastapi import FastAPI

from app.api.router import api_router

openapi_tags = [
    {
        "name": "health",
        "description": "Lightweight liveness checks for the service.",
    },
    {
        "name": "models",
        "description": "CRUD operations for BMW car models (read is public; write requires API key).",
    },
    {
        "name": "records",
        "description": "Market price observations linked to a given car model (write requires API key).",
    },
    {
        "name": "analytics",
        "description": "Aggregations over market records (average price, trends, rankings).",
    },
]

app = FastAPI(
    title="BMW Market Analytics API",
    version="0.1.0",
    description=(
        "Data-driven API for BMW pricing and market analytics (COMP3011 CW1).\n\n"
        "**Auth:** write endpoints require `X-API-Key`.\n"
        "**Core resources:** `CarModel` and `MarketRecord`."
    ),
    openapi_tags=openapi_tags,  # CW1 polish: makes Swagger grouping/descriptions clearer
    contact={  # CW1 polish: small professional touch (doesn't affect functionality)
        "name": "COMP3011 Coursework",
    },
)

app.include_router(api_router)


@app.get("/", include_in_schema=False)
def root():
    # CW1 polish: tiny friendly root endpoint (kept out of schema so it doesn’t clutter docs)
    return {"message": "BMW Market Analytics API. See /docs for Swagger UI."}