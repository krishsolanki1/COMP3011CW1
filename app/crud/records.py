from __future__ import annotations

from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import MarketRecord

_UPDATABLE_FIELDS = {"year", "price", "sales_volume"}


def list_records_for_model(
    db: Session,
    car_model_id: int,
    *,
    year: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    skip: int = 0,
    limit: int = 200,
) -> Sequence[MarketRecord]:
    stmt = select(MarketRecord).where(MarketRecord.car_model_id == car_model_id)
    if year is not None:
        stmt = stmt.where(MarketRecord.year == year)
    if min_price is not None:
        stmt = stmt.where(MarketRecord.price >= min_price)
    if max_price is not None:
        stmt = stmt.where(MarketRecord.price <= max_price)
    return db.scalars(stmt.order_by(MarketRecord.year).offset(skip).limit(limit)).all()


def get_record(db: Session, record_id: int) -> MarketRecord | None:
    return db.get(MarketRecord, record_id)


def create_record_for_model(
    db: Session,
    *,
    car_model_id: int,
    **data: Any,
) -> MarketRecord:
    obj = MarketRecord(
        car_model_id=car_model_id,
        year=data.get("year"),
        price=data.get("price"),
        sales_volume=data.get("sales_volume"),  # was silently dropped before
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_record(
    db: Session,
    record: MarketRecord,
    **updates: Any,
) -> MarketRecord:
    for key, value in updates.items():
        if key in _UPDATABLE_FIELDS:
            setattr(record, key, value)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def delete_record(db: Session, record: MarketRecord) -> None:
    db.delete(record)
    db.commit()