from pydantic import BaseModel, Field


class AveragePriceOut(BaseModel):
    model_id: int
    model_name: str
    average_price: float | None = Field(
        default=None,
        description="Average price across all records for this model. None if the model has no records.",
    )


class TrendPoint(BaseModel):
    year: int
    average_price: float
    num_records: int


class PriceTrendOut(BaseModel):
    model_id: int
    model_name: str
    trend: list[TrendPoint]


class TopModelResult(BaseModel):
    model_id: int
    model_name: str
    average_price: float
    num_records: int


class TopModelsOut(BaseModel):
    year: int
    results: list[TopModelResult]