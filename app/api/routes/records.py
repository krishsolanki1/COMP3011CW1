from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_car_model_or_404_path, get_record_or_404
from app.core.security import require_api_key
from app.crud import records as crud_records
from app.db.models import CarModel, MarketRecord
from app.db.session import get_db
from app.schemas.records import MarketRecordCreate, MarketRecordOut, MarketRecordUpdate

router = APIRouter()


@router.get(
    "/{model_id}/records",
    response_model=list[MarketRecordOut],
    summary="List market records for a model",
)
def list_records_for_model(
    car_model: CarModel = Depends(get_car_model_or_404_path),
    db: Session = Depends(get_db),
    year: int | None = Query(default=None, ge=1900, le=2100, description="Filter by exact year."),
    min_price: float | None = Query(default=None, gt=0, description="Minimum price (inclusive)."),
    max_price: float | None = Query(default=None, gt=0, description="Maximum price (inclusive)."),
    skip: int = Query(default=0, ge=0, description="Rows to skip (pagination)."),
    limit: int = Query(default=200, ge=1, le=1000, description="Max rows to return (1–1000)."),
):
    return list(crud_records.list_records_for_model(
        db, car_model.id, year=year, min_price=min_price,
        max_price=max_price, skip=skip, limit=limit,
    ))


@router.post(
    "/{model_id}/records",
    response_model=MarketRecordOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_api_key)],
    summary="Create a market record for a model (API key required)",
)
def create_record_for_model(
    payload: MarketRecordCreate,
    car_model: CarModel = Depends(get_car_model_or_404_path),
    db: Session = Depends(get_db),
):
    obj = crud_records.create_record_for_model(db, car_model_id=car_model.id, **payload.model_dump())
    return obj


@router.get(
    "/{model_id}/records/{record_id}",
    response_model=MarketRecordOut,
    summary="Get a single market record",
)
def get_record(
    car_model: CarModel = Depends(get_car_model_or_404_path),
    record: MarketRecord = Depends(get_record_or_404),
):
    if record.car_model_id != car_model.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return record


@router.patch(
    "/{model_id}/records/{record_id}",
    response_model=MarketRecordOut,
    dependencies=[Depends(require_api_key)],
    summary="Partially update a market record (API key required)",
)
def update_record(
    payload: MarketRecordUpdate,
    car_model: CarModel = Depends(get_car_model_or_404_path),
    record: MarketRecord = Depends(get_record_or_404),
    db: Session = Depends(get_db),
):
    if record.car_model_id != car_model.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return record
    return crud_records.update_record(db, record, **updates)


@router.delete(
    "/{model_id}/records/{record_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_api_key)],
    summary="Delete a market record (API key required)",
)
def delete_record(
    car_model: CarModel = Depends(get_car_model_or_404_path),
    record: MarketRecord = Depends(get_record_or_404),
    db: Session = Depends(get_db),
):
    if record.car_model_id != car_model.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    crud_records.delete_record(db, record)
    return None