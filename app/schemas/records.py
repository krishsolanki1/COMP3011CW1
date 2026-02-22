from pydantic import BaseModel, ConfigDict, Field


class MarketRecordBase(BaseModel):
    # CW1 polish: align API validation with DB constraints so bad data is rejected early (422).
    year: int = Field(..., ge=1900, le=2100, description="Observation year.")
    price: float = Field(..., gt=0, description="Observed price (> 0).")
    sales_volume: int | None = Field(default=None, ge=0, description="Optional sales volume (>= 0).")


class MarketRecordCreate(MarketRecordBase):
    pass


class MarketRecordOut(MarketRecordBase):
    id: int
    car_model_id: int
    model_config = ConfigDict(from_attributes=True)