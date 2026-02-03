from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import CarModel, MarketRecord
from app.crud import models as crud_models


router = APIRouter()


@router.get("/average-price")
def average_price(
    model_id: int = Query(..., ge=1),
    db: Session = Depends(get_db),
):
    car_model = crud_models.get_car_model(db, model_id)
    if not car_model:
        raise HTTPException(status_code=404, detail="Model not found")

    stmt = select(func.avg(MarketRecord.price)).where(
        MarketRecord.car_model_id == model_id
    )
    avg_price = db.scalar(stmt)

    return {
        "model_id": model_id,
        "model_name": car_model.name,
        "average_price": float(avg_price) if avg_price is not None else None,
    }


@router.get("/price-trend")
def price_trend(
    model_id: int = Query(..., ge=1),
    db: Session = Depends(get_db),
):
    car_model = crud_models.get_car_model(db, model_id)
    if not car_model:
        raise HTTPException(status_code=404, detail="Model not found")

    stmt = (
        select(MarketRecord.year, func.avg(MarketRecord.price), func.count())
        .where(MarketRecord.car_model_id == model_id)
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
        "model_id": model_id,
        "model_name": car_model.name,
        "trend": trend,
    }


@router.get("/top-models")
def top_models_for_year(
    year: int = Query(..., ge=1900, le=2100),
    limit: int = Query(5, ge=1, le=50),
    db: Session = Depends(get_db),
):
    # average price per model in that year, ranked highest first
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

    return {
        "year": year,
        "results": results,
    }
