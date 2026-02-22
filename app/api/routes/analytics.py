from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_car_model_or_404_query
from app.db.models import CarModel, MarketRecord
from app.db.session import get_db
from app.schemas.analytics import AveragePriceOut, PriceTrendOut, TopModelsOut

router = APIRouter()


@router.get(
    "/average-price",
    response_model=AveragePriceOut,
    summary="Average price for a model",
)
def average_price(
    car_model: CarModel = Depends(get_car_model_or_404_query),
    db: Session = Depends(get_db),
):
    # CW1 polish: query param validation + 404 handled in dependency
    stmt = select(func.avg(MarketRecord.price)).where(MarketRecord.car_model_id == car_model.id)
    avg_price = db.scalar(stmt)

    return {
        "model_id": car_model.id,
        "model_name": car_model.name,
        "average_price": float(avg_price) if avg_price is not None else None,
    }


@router.get(
    "/price-trend",
    response_model=PriceTrendOut,
    summary="Average price per year for a model",
)
def price_trend(
    car_model: CarModel = Depends(get_car_model_or_404_query),
    db: Session = Depends(get_db),
):
    stmt = (
        select(MarketRecord.year, func.avg(MarketRecord.price), func.count())
        .where(MarketRecord.car_model_id == car_model.id)
        .group_by(MarketRecord.year)
        .order_by(MarketRecord.year)
    )

    rows = db.execute(stmt).all()
    trend = [
        {
            "year": year,
            "average_price": float(avg_price),
            "num_records": count,
        }
        for (year, avg_price, count) in rows
    ]

    return {
        "model_id": car_model.id,
        "model_name": car_model.name,
        "trend": trend,
    }


@router.get(
    "/top-models",
    response_model=TopModelsOut,
    summary="Top models by average price for a given year",
)
def top_models_for_year(
    year: int = Query(
        ...,
        ge=1900,
        le=2100,
        description="Year to rank models within.",
        examples=[2019],
    ),
    limit: int = Query(
        5,
        ge=1,
        le=50,
        description="Max number of models to return (1–50).",
        examples=[5],
    ),
    db: Session = Depends(get_db),
):
    stmt = (
        select(
            CarModel.id,
            CarModel.name,
            func.avg(MarketRecord.price).label("avg_price"),
            func.count(MarketRecord.id).label("num_records"),
        )
        .join(MarketRecord, MarketRecord.car_model_id == CarModel.id)
        .where(MarketRecord.year == year)
        .group_by(CarModel.id, CarModel.name)
        .order_by(func.avg(MarketRecord.price).desc())
        .limit(limit)
    )

    rows = db.execute(stmt).all()

    results = [
        {
            "model_id": model_id,
            "model_name": name,
            "average_price": float(avg_price),
            "num_records": num_records,
        }
        for (model_id, name, avg_price, num_records) in rows
    ]

    return {"year": year, "results": results}