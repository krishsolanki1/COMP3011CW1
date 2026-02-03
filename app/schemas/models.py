from pydantic import BaseModel, Field


class CarModelBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    series: str | None = Field(default=None, max_length=50)
    body_style: str | None = Field(default=None, max_length=50)
    fuel_type: str | None = Field(default=None, max_length=50)
    transmission: str | None = Field(default=None, max_length=50)


class CarModelCreate(CarModelBase):
    pass


class CarModelUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    series: str | None = Field(default=None, max_length=50)
    body_style: str | None = Field(default=None, max_length=50)
    fuel_type: str | None = Field(default=None, max_length=50)
    transmission: str | None = Field(default=None, max_length=50)


class CarModelOut(CarModelBase):
    id: int

    class Config:
        from_attributes = True
