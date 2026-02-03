from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CarModel(Base):
    __tablename__ = "car_models"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    series: Mapped[str | None] = mapped_column(String(50), nullable=True)
    body_style: Mapped[str | None] = mapped_column(String(50), nullable=True)
    fuel_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    transmission: Mapped[str | None] = mapped_column(String(50), nullable=True)

    market_records: Mapped[list["MarketRecord"]] = relationship(
        back_populates="car_model",
        cascade="all, delete-orphan",
    )


class MarketRecord(Base):
    __tablename__ = "market_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    car_model_id: Mapped[int] = mapped_column(
        ForeignKey("car_models.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    sales_volume: Mapped[int | None] = mapped_column(Integer, nullable=True)

    car_model: Mapped["CarModel"] = relationship(back_populates="market_records")
