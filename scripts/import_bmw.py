import argparse
import csv
from pathlib import Path
import sys

# CW1 polish: make imports work when running as a script (Windows/PowerShell especially)
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.db.session import SessionLocal
from app.db.models import CarModel, MarketRecord


def main() -> None:
    parser = argparse.ArgumentParser(description="Import BMW dataset into the database.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Wipe existing CarModel and MarketRecord rows before importing.",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    csv_path = project_root / "bmw.csv"

    if not csv_path.exists():
        raise SystemExit(f"CSV file not found at {csv_path}")

    session = SessionLocal()

    try:
        if args.reset:
            session.query(MarketRecord).delete()
            session.query(CarModel).delete()
            session.commit()
            print("Database reset: all existing rows removed.")

        # Cache for CarModel rows (so we don't create duplicates)
        models_cache: dict[str, CarModel] = {}

        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                model_name = row["model"].strip()
                year = int(row["year"])
                price = float(row["price"])

                car_model = models_cache.get(model_name)
                if car_model is None:
                    car_model = CarModel(
                        name=model_name,
                        series=None,
                        body_style=None,
                        fuel_type=row.get("fuelType") or None,
                        transmission=row.get("transmission") or None,
                    )
                    session.add(car_model)
                    session.flush()  # assigns an id without full commit yet
                    models_cache[model_name] = car_model

                record = MarketRecord(
                    car_model_id=car_model.id,
                    year=year,
                    price=price,
                )
                session.add(record)

        session.commit()
        print("Import complete.")

    finally:
        session.close()


if __name__ == "__main__":
    main()
