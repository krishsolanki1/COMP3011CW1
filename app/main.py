from fastapi import FastAPI
from app.api.router import api_router


app = FastAPI(
    title="BMW Market Analytics API",
    version="0.1.0",
    description="Data-driven API for BMW pricing and sales analytics (COMP3011 CW1).",
)

app.include_router(api_router)