from fastapi import Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app.crud import models as crud_models
from app.crud import records as crud_records
from app.db.models import CarModel, MarketRecord
from app.db.session import get_db


def get_car_model_or_404_path(
    model_id: int = Path(
        ...,
        ge=1,
        description="Car model ID (path param).",
        examples=[1],
    ),
    db: Session = Depends(get_db),
) -> CarModel:
    # CW1 polish: centralise the “lookup + 404” so route files don’t repeat themselves.
    obj = crud_models.get_car_model(db, model_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Model not found")
    return obj


def get_record_or_404(
    record_id: int = Path(
        ...,
        ge=1,
        description="Market record ID.",
        examples=[1],
    ),
    db: Session = Depends(get_db),
) -> MarketRecord:
    obj = crud_records.get_record(db, record_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return obj


def get_car_model_or_404_query(
    model_id: int = Query(
        ...,
        ge=1,
        description="Car model ID (query param).",
        examples=[1],
    ),
    db: Session = Depends(get_db),
) -> CarModel:
    # CW1 polish: same idea as above, but for analytics endpoints that use ?model_id=...
    obj = crud_models.get_car_model(db, model_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Model not found")
    return obj