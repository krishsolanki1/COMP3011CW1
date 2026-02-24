# scripts/verify.sh
#!/usr/bin/env bash
set -euo pipefail

RESET_DB="${1:-}"

# CW1 polish: run from project root (same folder as app/, alembic/, scripts/)
if [[ ! -d "app" || ! -d "alembic" ]]; then
  echo "Run this from the project root (folder containing app/ and alembic/)." >&2
  exit 2
fi

python -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate

pip install -r requirements.txt

alembic upgrade head

if [[ "$RESET_DB" == "--reset" ]]; then
  python scripts/import_bmw.py --reset
else
  python scripts/import_bmw.py
fi

pytest -q
echo "OK: deps + migrations + seed + tests all passed."