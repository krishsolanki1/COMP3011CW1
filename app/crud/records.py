from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import MarketRecord


def list_records_for_model(db: Session, car_model_id: int) -> Sequence[MarketRecord]:
    stmt = (
        select(MarketRecord)
        .where(MarketRecord.car_model_id == car_model_id)
        .order_by(MarketRecord.year)
    )
    return db.scalars(stmt).all()


def create_record_for_model(
    db: Session,
    *,
    car_model_id: int,
    year: int,
    price: float,
) -> MarketRecord:
    obj = MarketRecord(
        car_model_id=car_model_id,
        year=year,
        price=price,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
