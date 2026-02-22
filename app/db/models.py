from sqlalchemy import Integer, String, Float, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CarModel(Base):
    __tablename__ = "car_models"

    # CW1 polish: extra index on name helps lookup / debug and makes the schema feel more “real”
    __table_args__ = (
        Index("ix_car_models_name", "name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    series: Mapped[str | None] = mapped_column(String(50), nullable=True)
    body_style: Mapped[str | None] = mapped_column(String(50), nullable=True)
    fuel_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    transmission: Mapped[str | None] = mapped_column(String(50), nullable=True)

    market_records: Mapped[list["MarketRecord"]] = relationship(
        back_populates="car_model",
        cascade="all, delete-orphan",
        passive_deletes=True,  # CW1 polish: let DB enforce ON DELETE CASCADE cleanly
    )


class MarketRecord(Base):
    __tablename__ = "market_records"

    # CW1 polish: analytics endpoints filter by (model_id) and/or (year) constantly.
    # These indexes match the common query shapes:
    # - average-price: WHERE car_model_id = ?
    # - price-trend:  WHERE car_model_id = ? GROUP BY year
    # - top-models:   WHERE year = ? GROUP BY car_model_id
    __table_args__ = (
        CheckConstraint("year >= 1900 AND year <= 2100", name="ck_market_records_year_range"),
        CheckConstraint("price > 0", name="ck_market_records_price_positive"),
        CheckConstraint(
            "sales_volume IS NULL OR sales_volume >= 0",
            name="ck_market_records_sales_volume_nonneg",
        ),
        Index("ix_market_records_year", "year"),
        Index("ix_market_records_model_year", "car_model_id", "year"),
    )

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