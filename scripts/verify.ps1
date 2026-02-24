# scripts/verify.ps1
param(
  [switch]$ResetDb
)

$ErrorActionPreference = "Stop"

# CW1 polish: run from project root (same folder as app/, alembic/, scripts/)
if (!(Test-Path "app") -or !(Test-Path "alembic")) {
  throw "Run this from the project root (folder containing app/ and alembic/)."
}

# venv
if (!(Test-Path ".venv")) {
  python -m venv .venv
}

. .\.venv\Scripts\Activate.ps1

# deps
pip install -r requirements.txt

# CW1 polish: make scripts imports reliable on Windows when running via python scripts\...
$env:PYTHONPATH = "$PWD"

# migrations
alembic upgrade head

# seed
if ($ResetDb) {
  python scripts\import_bmw.py --reset
} else {
  python scripts\import_bmw.py
}

# tests
pytest -q

Write-Host "OK: deps + migrations + seed + tests all passed." -ForegroundColor Green