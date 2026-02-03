from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import CarModel


def list_car_models(db: Session) -> Sequence[CarModel]:
    stmt = select(CarModel).order_by(CarModel.id)
    return db.scalars(stmt).all()


def get_car_model(db: Session, car_model_id: int) -> CarModel | None:
    return db.get(CarModel, car_model_id)


def create_car_model(
    db: Session,
    *,
    name: str,
    series: str | None,
    body_style: str | None,
    fuel_type: str | None,
    transmission: str | None,
) -> CarModel:
    obj = CarModel(
        name=name,
        series=series,
        body_style=body_style,
        fuel_type=fuel_type,
        transmission=transmission,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_car_model(
    db: Session,
    car_model: CarModel,
    *,
    name: str | None,
    series: str | None,
    body_style: str | None,
    fuel_type: str | None,
    transmission: str | None,
) -> CarModel:
    if name is not None:
        car_model.name = name
    if series is not None:
        car_model.series = series
    if body_style is not None:
        car_model.body_style = body_style
    if fuel_type is not None:
        car_model.fuel_type = fuel_type
    if transmission is not None:
        car_model.transmission = transmission

    db.add(car_model)
    db.commit()
    db.refresh(car_model)
    return car_model


def delete_car_model(db: Session, car_model: CarModel) -> None:
    db.delete(car_model)
    db.commit()
