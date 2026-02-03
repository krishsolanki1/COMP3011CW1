import csv
from pathlib import Path

from app.db.session import SessionLocal
from app.db.models import CarModel, MarketRecord


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    csv_path = project_root / "bmw.csv"

    if not csv_path.exists():
        raise SystemExit(f"CSV file not found at {csv_path}")

    session = SessionLocal()

    try:
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
