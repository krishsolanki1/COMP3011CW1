from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud import models as crud_models
from app.schemas.models import CarModelCreate, CarModelOut, CarModelUpdate
from app.core.security import require_api_key  


router = APIRouter()


@router.get("/", response_model=list[CarModelOut])
def list_models(db: Session = Depends(get_db)):
    return list(crud_models.list_car_models(db))


@router.post(
    "/",
    response_model=CarModelOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_api_key)],
)
def create_model(payload: CarModelCreate, db: Session = Depends(get_db)):
    obj = crud_models.create_car_model(
        db,
        name=payload.name,
        series=payload.series,
        body_style=payload.body_style,
        fuel_type=payload.fuel_type,
        transmission=payload.transmission,
    )
    return obj


@router.get("/{model_id}", response_model=CarModelOut)
def get_model(model_id: int, db: Session = Depends(get_db)):
    obj = crud_models.get_car_model(db, model_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Model not found")
    return obj


@router.patch(
    "/{model_id}",
    response_model=CarModelOut,
    dependencies=[Depends(require_api_key)],
)
def update_model(model_id: int, payload: CarModelUpdate, db: Session = Depends(get_db)):
    obj = crud_models.get_car_model(db, model_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Model not found")

    obj = crud_models.update_car_model(
        db,
        obj,
        name=payload.name,
        series=payload.series,
        body_style=payload.body_style,
        fuel_type=payload.fuel_type,
        transmission=payload.transmission,
    )
    return obj


@router.delete(
    "/{model_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_api_key)],
)
def delete_model(model_id: int, db: Session = Depends(get_db)):
    obj = crud_models.get_car_model(db, model_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Model not found")

    crud_models.delete_car_model(db, obj)
    return None
