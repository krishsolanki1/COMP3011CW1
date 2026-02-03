# COMP3011 CW1 — BMW Market Analytics API

Data-driven web API for BMW pricing and sales analytics (coursework project).

## Quickstart

```bash
python -m venv .venv

# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
uvicorn app.main:app --reload
