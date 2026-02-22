from __future__ import annotations

from typing import Any, Sequence

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
    **data: Any,
) -> MarketRecord:
    # CW1 polish: allows routes to do create_record_for_model(db, car_model_id=id, **payload.model_dump())
    obj = MarketRecord(
        car_model_id=car_model_id,
        year=data.get("year"),
        price=data.get("price"),
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj