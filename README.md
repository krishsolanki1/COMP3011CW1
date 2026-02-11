# BMW Market Analytics API
COMP3011 – Web Services and Web Data Coursework 1

---

## Overview

This project implements a RESTful web service for managing and analysing BMW used car market data.

The API provides:

- CRUD operations for BMW car models
- Nested CRUD operations for market price records
- Analytics endpoints for average prices and trends
- API key authentication for write operations

The system is built using FastAPI, SQLAlchemy, SQLite and Alembic.

---

## Repository Structure

app/
- api/          Route handlers
- crud/         Database logic
- db/           ORM models and session management
- schemas/      Pydantic request/response models
- core/         Configuration and security

scripts/
- import_bmw.py  Dataset import script

docs/
- api.md         API documentation (source)
- api.pdf        API documentation (final PDF)

tests/
- pytest test suite

---

## Requirements

Python 3.11+ recommended.

Install dependencies:

pip install -r requirements.txt

---

## Environment Variables

Create a `.env` file in the project root:

API_KEY=super-secret-key  
DATABASE_URL=sqlite:///./app.db

---

## Database Setup

Run database migrations:

alembic upgrade head

---

## Import Dataset

Download the BMW dataset from Kaggle and place the CSV file in the project root.

Then run:

python -m scripts.import_bmw

This populates the database with models and market records.

Note: The dataset is not included in this repository due to licensing and size considerations.

---

## Run the API

uvicorn app.main:app --reload

API will be available at:

http://127.0.0.1:8000

Interactive documentation (Swagger UI):

http://127.0.0.1:8000/docs

---

## Authentication

Write operations require an API key.

Include the following header in requests:

X-API-Key: super-secret-key

Read-only endpoints do not require authentication.

---

## Testing

Run tests using:

pytest

---

## API Documentation

Full API documentation is available in:

docs/api.pdf

This document describes all endpoints, parameters, request/response formats, authentication, and error codes.

---

## GenAI Usage

GenAI (ChatGPT) was used as a development assistant for scaffolding, debugging and documentation drafting. All generated code was reviewed, tested and adapted before inclusion in the final submission.

The final implementation and design decisions are the author’s own.
