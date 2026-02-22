from __future__ import annotations

from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import CarModel

# CW1 polish: keep an explicit allow-list for updates to avoid accidental attribute writes
_UPDATABLE_FIELDS = {"name", "series", "body_style", "fuel_type", "transmission"}


def list_car_models(db: Session) -> Sequence[CarModel]:
    stmt = select(CarModel).order_by(CarModel.id)
    return db.scalars(stmt).all()


def get_car_model(db: Session, car_model_id: int) -> CarModel | None:
    return db.get(CarModel, car_model_id)


def create_car_model(
    db: Session,
    **data: Any,
) -> CarModel:
    # CW1 polish: allows routes to do create_car_model(db, **payload.model_dump())
    obj = CarModel(
        name=data.get("name"),
        series=data.get("series"),
        body_style=data.get("body_style"),
        fuel_type=data.get("fuel_type"),
        transmission=data.get("transmission"),
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_car_model(
    db: Session,
    car_model: CarModel,
    **updates: Any,
) -> CarModel:
    # CW1 polish: PATCH correctness.
    # The route should pass payload.model_dump(exclude_unset=True) so we ONLY update provided fields,
    # but we still allow explicit None (client sends null) to clear a field.
    for key, value in updates.items():
        if key in _UPDATABLE_FIELDS:
            setattr(car_model, key, value)

    db.add(car_model)
    db.commit()
    db.refresh(car_model)
    return car_model


def delete_car_model(db: Session, car_model: CarModel) -> None:
    db.delete(car_model)
    db.commit()