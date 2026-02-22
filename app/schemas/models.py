from pydantic import BaseModel, ConfigDict, Field


class CarModelBase(BaseModel):
    # CW1 polish: basic input hygiene so we don't accept empty strings / garbage.
    # (Keeps API validation consistent with what you'd expect in a real service.)
    name: str = Field(..., min_length=1, max_length=120, description="Model name (e.g. '320d').")
    series: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="BMW series (e.g. '3 Series').",
    )
    body_style: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="Body style (e.g. 'Saloon', 'Coupe').",
    )
    fuel_type: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="Fuel type (e.g. 'Petrol', 'Diesel', 'Hybrid').",
    )
    transmission: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="Transmission type (e.g. 'Manual', 'Automatic').",
    )


class CarModelCreate(CarModelBase):
    pass


class CarModelUpdate(BaseModel):
    # CW1 polish: PATCH semantics — all optional, but if present must be valid.
    name: str | None = Field(default=None, min_length=1, max_length=120)
    series: str | None = Field(default=None, min_length=1, max_length=50)
    body_style: str | None = Field(default=None, min_length=1, max_length=50)
    fuel_type: str | None = Field(default=None, min_length=1, max_length=50)
    transmission: str | None = Field(default=None, min_length=1, max_length=50)


class CarModelOut(CarModelBase):
    id: int
    model_config = ConfigDict(from_attributes=True)