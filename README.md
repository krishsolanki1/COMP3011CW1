# BMW Market Analytics API — COMP3011 (Web Services & Web Data) CW1

A small FastAPI backend for managing BMW car models and market price observations, with a few analytics endpoints on top (average price, price trends, top models per year).  
Built with **FastAPI**, **SQLAlchemy ORM**, **Alembic**, **SQLite**, and **pytest**.

> **Write endpoints are protected by an API key** via `X-API-Key`.

---

## Contents

- [Quickstart](#quickstart)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [Configuration](#configuration)
- [Database + migrations](#database--migrations)
- [Dataset import / seeding](#dataset-import--seeding)
- [Run the API](#run-the-api)
- [Smoke checks (manual)](#smoke-checks-manual)
- [Testing](#testing)
- [MCP Server](#mcp-server)
- [API overview](#api-overview)
- [Deployment (PythonAnywhere)](#deployment-pythonanywhere)
- [Troubleshooting](#troubleshooting)
- [GenAI usage](#genai-usage)

---

## Quickstart

### Requirements
- **Python 3.11+** (recommended)
- pip
- (Optional) SQLite CLI for inspecting the DB

### 1) Create a venv + install deps

**macOS/Linux**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell)**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2) Set environment variables

Create a `.env` file in the project root:
```env
API_KEY=super-secret-key
DATABASE_URL=sqlite:///./app.db
```

Notes:
- `.env` contains secrets. It should **not** be committed to Git.

### 3) Run migrations
```bash
alembic upgrade head
```

### 4) Seed/import the dataset (if needed)
```bash
python scripts/import_bmw.py
# if you want to wipe + re-seed deterministically:
python scripts/import_bmw.py --reset
```

### 5) Run the API
```bash
uvicorn app.main:app --reload
```

Open Swagger UI:
- http://127.0.0.1:8000/docs

### 6) Run tests
```bash
pytest -q
```
### 7) One-command verification (recommended)

If you just want to verify everything end-to-end (deps → migrations → seed → tests):

**Windows (PowerShell)**
```powershell
powershell -ExecutionPolicy Bypass -File scripts\verify.ps1 -ResetDb
```

**macOS/Linux**
```bash
bash scripts/verify.sh --reset
```

---

## Tech stack

- **FastAPI** for HTTP routing + automatic OpenAPI docs
- **SQLAlchemy (2.x)** ORM for DB models + queries
- **Alembic** for schema migrations
- **SQLite** as the datastore (via `DATABASE_URL`)
- **pytest** + FastAPI **TestClient** for integration-style tests

---

## Project structure

```
app/
  main.py              # FastAPI app entrypoint (app.main:app)
  api/
    router.py          # central router wiring + prefixes/tags
    deps.py            # shared dependencies (e.g., get model or 404)
    routes/
      health.py
      models.py
      records.py
      analytics.py
  core/
    config.py          # settings (.env) loading
    security.py        # API key auth dependency
  db/
    base.py            # SQLAlchemy Base
    models.py          # CarModel + MarketRecord tables
    session.py         # engine + session + get_db dependency
  schemas/
    models.py          # Pydantic request/response schemas
    records.py
    analytics.py
  crud/
    models.py          # DB CRUD for CarModel
    records.py         # DB CRUD for MarketRecord

alembic/               # migration tooling
alembic/versions/      # migration scripts

scripts/
  import_bmw.py        # dataset import / seeding (idempotent)

tests/
  conftest.py          # shared TestClient + auth fixture
  test_health.py
  test_models.py
  test_records.py
  test_analytics.py
  test_auth.py

docs/
  api.md               # markdown API documentation
  api.pdf              # exported documentation
```

---

## Configuration

The service uses environment variables (loaded from `.env` in the project root).

| Variable | Purpose | Example |
|---|---|---|
| `API_KEY` | API key for write endpoints (`POST/PATCH/DELETE`) | `super-secret-key` |
| `DATABASE_URL` | SQLAlchemy DB URL | `sqlite:///./app.db` |

Notes:
- `.env` loading is **deterministic** (resolved relative to the project root), so running `pytest` vs `uvicorn` from different working directories is less likely to break config.
- Defaults exist for local dev, but for assessment you should define `.env`.

---

## Database + migrations

Alembic is used for schema management.

Run migrations:
```bash
alembic upgrade head
```

The DB layer includes:
- **foreign keys + cascade deletes** so deleting a `CarModel` removes linked `MarketRecord`s
- **SQLite FK enforcement enabled** (`PRAGMA foreign_keys=ON`) so cascades actually work
- **indexes** aligned with analytics query patterns (e.g., `(car_model_id, year)`)

---

## Dataset import / seeding

A helper script imports a CSV dataset into the DB.

Expected columns (minimum):
- `model` (string)
- `year` (int)
- `price` (float)
- (optional) `fuelType`, `transmission`

Typical usage:
```bash
python scripts/import_bmw.py
```

If the DB is already populated, the import script is designed to avoid accidental duplication.  
To force a clean deterministic re-seed:
```bash
python scripts/import_bmw.py --reset
```

If you’re on Windows and you ever see `ModuleNotFoundError: No module named 'app'`, run from the project root and set `PYTHONPATH`:
```powershell
$env:PYTHONPATH="$PWD"
python scripts\import_bmw.py --reset
```

---

## Run the API

Start the server:
```bash
uvicorn app.main:app --reload
```

Useful URLs:
- Base: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

Note: endpoints are defined with trailing slashes for collections (e.g. `/models/`).  
If you hit `/models` without the slash, FastAPI will redirect (`307`) to `/models/` — that’s normal.

---

## Smoke checks (manual)

After starting the API, these quick checks confirm the main behaviour is working:

```bash
# health
curl http://127.0.0.1:8000/health

# list models (should return JSON array)
curl http://127.0.0.1:8000/models/

# unauthenticated write (should be 401)
curl -X POST "http://127.0.0.1:8000/models/"   -H "Content-Type: application/json"   -d '{"name":"AuthTest","series":"3 Series","body_style":"Saloon","fuel_type":"Petrol","transmission":"Auto"}'
```

Authenticated create (replace the key to match `.env`):
```bash
curl -X POST "http://127.0.0.1:8000/models/"   -H "X-API-Key: super-secret-key"   -H "Content-Type: application/json"   -d '{"name":"AuthOK","series":"3 Series","body_style":"Saloon","fuel_type":"Petrol","transmission":"Auto"}'
```

---

## Testing

Tests use **pytest** + FastAPI **TestClient** (integration-ish tests over the real SQLite DB).

Run:
```bash
pytest -q
```

Test coverage includes:
- happy-path reads (`/health`, list/get models, analytics)
- common error paths (**404** for missing model IDs)
- auth enforcement (**401** for missing/invalid API key on writes)
- successful authenticated writes (create model, create record)
- analytics endpoints response shape + correctness over real imported data

The suite is split by feature (`test_health`, `test_models`, `test_records`, `test_analytics`, `test_auth`) to keep it readable and easy to extend.

---

## MCP Server

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server is included at `mcp_server.py`. It exposes the BMW analytics API as tools that Claude (and other MCP-compatible AI clients) can call directly.

### Tools exposed

| Tool | Description |
|---|---|
| `list_models` | List models with optional `fuel_type`, `transmission`, `name` filters |
| `get_model` | Get full details for a model by ID |
| `get_average_price` | Average market price for a model |
| `get_price_trend` | Year-by-year price trend for a model |
| `get_top_models` | Top models by average price for a given year |

### Install

```bash
pip install "mcp>=1.2.0"
```

### Add to Claude Desktop

Add the following to your `claude_desktop_config.json` (usually at `~/Library/Application Support/Claude/` on macOS or `%APPDATA%\Claude\` on Windows):

```json
{
  "mcpServers": {
    "bmw-market-analytics": {
      "command": "python",
      "args": ["C:/path/to/COMP3011CW1/mcp_server.py"]
    }
  }
}
```

### Run standalone (stdio)

```bash
python mcp_server.py
```

The server communicates over stdin/stdout using the MCP protocol.

---

## API overview

### Health
- `GET /health` → `{ "status": "ok" }`

### Models (CarModel)
- `GET /models/` → list models (optional: `?name=`, `?series=`, `?fuel_type=`, `?transmission=`, `?skip=`, `?limit=`)
- `GET /models/{id}` → model by ID (404 if missing)
- `POST /models/` → create model (**API key required**)
- `PATCH /models/{id}` → partial update (**API key required**)
- `DELETE /models/{id}` → delete model + records (**API key required**)

Example create (PowerShell):
```powershell
$env:API_KEY="super-secret-key"
curl -Method POST "http://127.0.0.1:8000/models/" `
  -Headers @{ "X-API-Key" = $env:API_KEY } `
  -ContentType "application/json" `
  -Body '{"name":"Test Model","series":"3 Series","body_style":"Saloon","fuel_type":"Petrol","transmission":"Auto"}'
```

### Records (MarketRecord)
- `GET /models/{id}/records` → list records for model (optional: `?year=`, `?min_price=`, `?max_price=`, `?skip=`, `?limit=`)
- `POST /models/{id}/records` → add a record (**API key required**, 404 if model missing)
- `GET /models/{id}/records/{record_id}` → single record (404 if missing or wrong model)
- `PATCH /models/{id}/records/{record_id}` → partial update (**API key required**)
- `DELETE /models/{id}/records/{record_id}` → delete record (**API key required**)

Example create record:
```bash
curl -X POST "http://127.0.0.1:8000/models/1/records"   -H "X-API-Key: super-secret-key"   -H "Content-Type: application/json"   -d '{"year":2020,"price":12345.67}'
```

### Analytics
- `GET /analytics/average-price?model_id=...`
  - returns `{ model_id, model_name, average_price }`
- `GET /analytics/price-trend?model_id=...`
  - returns `{ model_id, model_name, trend: [ {year, average_price, num_records}, ... ] }`
- `GET /analytics/top-models?year=YYYY&limit=N`
  - returns `{ year, results: [ {model_id, model_name, average_price, num_records}, ... ] }`

---

## Deployment (PythonAnywhere)

PythonAnywhere's free "Beginner" tier hosts the API at a public URL with persistent SQLite storage.

### One-time setup

**1. Create a free account** at https://www.pythonanywhere.com

**2. Open a Bash console** and clone the repo:
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

**3. Create a virtualenv and install deps:**
```bash
mkvirtualenv --python=python3.11 bmwapi
pip install -r requirements.txt
```

**4. Create a `.env` file** (use the absolute path — note 4 slashes for SQLite):
```env
DATABASE_URL=sqlite:////home/<username>/<repo>/app.db
API_KEY=<choose-a-secret-key>
```

**5. Run migrations and seed data:**
```bash
alembic upgrade head
python scripts/import_bmw.py --reset
```

**6. Set up the web app:**
- Go to the **Web** tab → **Add a new web app**
- Domain: `<username>.pythonanywhere.com`
- Framework: **Manual configuration** → Python 3.11

**7. Configure the web app settings:**
- **Source code**: `/home/<username>/<repo>`
- **WSGI configuration file**: click the link and replace the entire content with:
  ```python
  import sys
  sys.path.insert(0, '/home/<username>/<repo>')
  from wsgi import application
  ```
- **Virtualenv**: `/home/<username>/.virtualenvs/bmwapi`

**8. Click Reload** — the API is now live at:
```
https://<username>.pythonanywhere.com/docs
```

### Updating after a git push

```bash
# In a PythonAnywhere Bash console:
cd <repo>
git pull
# Then click Reload in the Web tab
```

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'app'` (Windows)**
- Run from project root
- Set PYTHONPATH:
  ```powershell
  $env:PYTHONPATH="$PWD"
  ```

**SQLite cascade deletes not working**
- SQLite requires FK enforcement. This project enables it at engine startup (`PRAGMA foreign_keys=ON`).

**Got redirected from `/models` to `/models/`**
- Normal FastAPI behaviour (307 redirect). Use trailing slashes for collection endpoints.

**Tests fail because there’s no data**
- Run:
  ```bash
  alembic upgrade head
  python scripts/import_bmw.py --reset
  pytest -q
  ```

---

## GenAI usage

GenAI tools (ChatGPT and Claude Code) were used throughout development for scaffolding, debugging, understanding new technologies (ASGI/WSGI bridging, MCP protocol), and documentation drafting. All generated suggestions were reviewed, tested, and adapted before inclusion. Full declaration and conversation logs are in the technical report appendix.