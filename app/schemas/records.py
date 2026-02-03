from pydantic import BaseModel, Field


class MarketRecordBase(BaseModel):
    year: int = Field(ge=1900, le=2100)
    price: float = Field(gt=0)


class MarketRecordCreate(MarketRecordBase):
    pass


class MarketRecordOut(MarketRecordBase):
    id: int
    car_model_id: int

    class Config:
        from_attributes = True
