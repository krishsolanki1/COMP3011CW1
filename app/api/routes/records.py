from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud import models as crud_models
from app.crud import records as crud_records
from app.schemas.records import MarketRecordCreate, MarketRecordOut
from app.core.security import require_api_key

router = APIRouter()


@router.get(
    "/{model_id}/records",
    response_model=list[MarketRecordOut],
)
def list_records_for_model(model_id: int, db: Session = Depends(get_db)):
    car_model = crud_models.get_car_model(db, model_id)
    if not car_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Model not found")
    return list(crud_records.list_records_for_model(db, car_model_id=model_id))


@router.post(
    "/{model_id}/records",
    response_model=MarketRecordOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_api_key)],
)

def create_record_for_model(
    model_id: int,
    payload: MarketRecordCreate,
    db: Session = Depends(get_db),
):
    car_model = crud_models.get_car_model(db, model_id)
    if not car_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Model not found")

    obj = crud_records.create_record_for_model(
        db,
        car_model_id=model_id,
        year=payload.year,
        price=payload.price,
    )
    return obj
