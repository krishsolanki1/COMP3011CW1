"""add indexes + check constraints for market_records analytics

Revision ID: c1f93b2a1d7e
Revises: a7390c74678f
Create Date: 2026-02-22

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "c1f93b2a1d7e"
down_revision: Union[str, Sequence[str], None] = "a7390c74678f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # car_models: add lookup index on name
    op.create_index("ix_car_models_name", "car_models", ["name"], unique=False)

    # market_records: SQLite needs batch mode for adding CHECK constraints reliably
    with op.batch_alter_table("market_records") as batch_op:
        # constraints (DB-level integrity)
        batch_op.create_check_constraint(
            "ck_market_records_year_range",
            "year >= 1900 AND year <= 2100",
        )
        batch_op.create_check_constraint(
            "ck_market_records_price_positive",
            "price > 0",
        )
        batch_op.create_check_constraint(
            "ck_market_records_sales_volume_nonneg",
            "sales_volume IS NULL OR sales_volume >= 0",
        )

        # indexes (analytics performance)
        batch_op.create_index("ix_market_records_year", ["year"], unique=False)
        batch_op.create_index("ix_market_records_model_year", ["car_model_id", "year"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_car_models_name", table_name="car_models")

    with op.batch_alter_table("market_records") as batch_op:
        batch_op.drop_index("ix_market_records_model_year")
        batch_op.drop_index("ix_market_records_year")

        batch_op.drop_constraint("ck_market_records_sales_volume_nonneg", type_="check")
        batch_op.drop_constraint("ck_market_records_price_positive", type_="check")
        batch_op.drop_constraint("ck_market_records_year_range", type_="check")