# BMW Market Analytics API Documentation
COMP3011 – Web Services and Web Data

---

## 1. Overview

This document describes all endpoints exposed by the BMW Market Analytics API.

Base URL (local development):

http://127.0.0.1:8000

All responses are returned in JSON format.

---

## 2. Authentication

Write operations require an API key.

Header:
X-API-Key: <your_api_key>

Example:
X-API-Key: super-secret-key

If the key is missing or invalid:

Status Code: 401 Unauthorized

Response:
{
  "detail": "Invalid or missing API key"
}

Read-only endpoints do not require authentication.

---

# 3. Endpoints

---

## 3.1 Health

### GET /health

Description:
Returns API status.

Authentication: Not required

Example Request:
GET /health

Example Response (200 OK):
{
  "status": "ok"
}

---

## 3.2 Car Models

---

### GET /models

Description:
Returns all car models.

Authentication: Not required

Example Request:
GET /models

Example Response:
[
  {
    "id": 1,
    "name": "3 Series",
    "series": "3 Series",
    "body_style": null,
    "fuel_type": "Petrol",
    "transmission": "Automatic"
  }
]

---

### GET /models/{id}

Path Parameter:
- id (integer)

Description:
Returns a single model by ID.

Authentication: Not required

Example Request:
GET /models/1

Example Response:
{
  "id": 1,
  "name": "3 Series",
  "series": "3 Series",
  "body_style": null,
  "fuel_type": "Petrol",
  "transmission": "Automatic"
}

Error (404 Not Found):
{
  "detail": "Model not found"
}

---

### POST /models

Authentication: Required

Request Body:
{
  "name": "X5",
  "series": "X5",
  "body_style": "SUV",
  "fuel_type": "Diesel",
  "transmission": "Automatic"
}

Example Request:
POST /models

Example Response (201 Created):
{
  "id": 10,
  "name": "X5",
  "series": "X5",
  "body_style": "SUV",
  "fuel_type": "Diesel",
  "transmission": "Automatic"
}

---

### PATCH /models/{id}

Authentication: Required

Path Parameter:
- id (integer)

Request Body Example:
{
  "fuel_type": "Hybrid"
}

Example Request:
PATCH /models/1

Example Response:
{
  "id": 1,
  "name": "3 Series",
  "series": "3 Series",
  "body_style": null,
  "fuel_type": "Hybrid",
  "transmission": "Automatic"
}

---

### DELETE /models/{id}

Authentication: Required

Example Request:
DELETE /models/1

Success Response:
Status Code: 204 No Content

---

## 3.3 Market Records

---

### GET /models/{id}/records

Path Parameter:
- id (integer)

Description:
Returns all price records for a model.

Authentication: Not required

Example Request:
GET /models/1/records

Example Response:
[
  {
    "id": 20,
    "car_model_id": 1,
    "year": 2018,
    "price": 19000.0
  }
]

---

### POST /models/{id}/records

Authentication: Required

Path Parameter:
- id (integer)

Request Body:
{
  "year": 2018,
  "price": 19000
}

Example Request:
POST /models/1/records

Example Response (201 Created):
{
  "id": 25,
  "car_model_id": 1,
  "year": 2018,
  "price": 19000.0
}

Error (404 Not Found):
{
  "detail": "Model not found"
}

---

## 3.4 Analytics Endpoints

---

### GET /analytics/average-price

Query Parameter:
- model_id (integer, required)

Example Request:
GET /analytics/average-price?model_id=1

Example Response:
{
  "model_id": 1,
  "model_name": "3 Series",
  "average_price": 18250.75
}

---

### GET /analytics/price-trend

Query Parameter:
- model_id (integer, required)

Example Request:
GET /analytics/price-trend?model_id=1

Example Response:
{
  "model_id": 1,
  "model_name": "3 Series",
  "trend": [
    {
      "year": 2016,
      "average_price": 18000.0,
      "num_records": 12
    }
  ]
}

---

### GET /analytics/top-models

Query Parameters:
- year (integer, required)
- limit (integer, optional)

Example Request:
GET /analytics/top-models?year=2018&limit=5

Example Response:
{
  "year": 2018,
  "results": [
    {
      "model_id": 3,
      "model_name": "X5",
      "average_price": 35000.0,
      "num_records": 7
    }
  ]
}

---

# 4. Error Codes Summary

| Code | Meaning |
|------|----------|
| 200 | Successful request |
| 201 | Resource created |
| 204 | Resource deleted |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

---

# 5. Setup Notes

- Run database migrations before starting the API.
- Import dataset using: python -m scripts.import_bmw
- Start server with: uvicorn app.main:app --reload
