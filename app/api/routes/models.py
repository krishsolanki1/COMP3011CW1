from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_car_model_or_404_path
from app.core.security import require_api_key
from app.crud import models as crud_models
from app.db.models import CarModel
from app.db.session import get_db
from app.schemas.models import CarModelCreate, CarModelOut, CarModelUpdate

router = APIRouter()


@router.get("/", response_model=list[CarModelOut], summary="List all car models")
def list_models(db: Session = Depends(get_db)):
    return list(crud_models.list_car_models(db))


@router.post(
    "/",
    response_model=CarModelOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_api_key)],
    summary="Create a new car model (API key required)",
)
def create_model(payload: CarModelCreate, db: Session = Depends(get_db)):
    # CW1 polish: avoids repeating each field manually
    obj = crud_models.create_car_model(db, **payload.model_dump())
    return obj


@router.get(
    "/{model_id}",
    response_model=CarModelOut,
    summary="Get a car model by ID",
)
def get_model(car_model: CarModel = Depends(get_car_model_or_404_path)):
    return car_model


@router.patch(
    "/{model_id}",
    response_model=CarModelOut,
    dependencies=[Depends(require_api_key)],
    summary="Partially update a car model (API key required)",
)
def update_model(
    payload: CarModelUpdate,
    car_model: CarModel = Depends(get_car_model_or_404_path),
    db: Session = Depends(get_db),
):
    # CW1 polish: PATCH semantics done properly:
    # - omit field => do not modify it
    # - send null => explicitly clear it
    updates = payload.model_dump(exclude_unset=True)

    # If someone sends an empty PATCH body, just return the existing resource.
    if not updates:
        return car_model

    obj = crud_models.update_car_model(db, car_model, **updates)
    return obj


@router.delete(
    "/{model_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_api_key)],
    summary="Delete a car model (API key required)",
)
def delete_model(
    car_model: CarModel = Depends(get_car_model_or_404_path),
    db: Session = Depends(get_db),
):
    crud_models.delete_car_model(db, car_model)
    return None