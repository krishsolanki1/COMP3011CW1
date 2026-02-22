from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_car_model_or_404_path
from app.core.security import require_api_key
from app.crud import records as crud_records
from app.db.models import CarModel
from app.db.session import get_db
from app.schemas.records import MarketRecordCreate, MarketRecordOut

router = APIRouter()


@router.get(
    "/{model_id}/records",
    response_model=list[MarketRecordOut],
    summary="List market records for a model",
)
def list_records_for_model(
    car_model: CarModel = Depends(get_car_model_or_404_path),
    db: Session = Depends(get_db),
):
    return list(crud_records.list_records_for_model(db, car_model_id=car_model.id))


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
    # CW1 polish: avoids repeating each field manually
    obj = crud_records.create_record_for_model(db, car_model_id=car_model.id, **payload.model_dump())
    return obj