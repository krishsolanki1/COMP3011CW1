import uuid


def _unique_model_payload():
    # avoid collisions if you run pytest a bunch of times
    suffix = uuid.uuid4().hex[:8]
    return {
        "name": f"Test BMW Model {suffix}",
        "series": "Test Series",
        "body_style": "Coupe",
        "fuel_type": "Petrol",
        "transmission": "Automatic",
    }


def test_list_models_ok(client):
    resp = client.get("/models")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert data, "Expected at least one seeded model in the DB"

    first = data[0]
    assert "id" in first
    assert "name" in first


def test_get_model_by_id_ok(client):
    resp_models = client.get("/models")
    assert resp_models.status_code == 200
    models = resp_models.json()
    assert models, "Expected at least one seeded model in the DB"

    model_id = models[0]["id"]
    resp_one = client.get(f"/models/{model_id}")
    assert resp_one.status_code == 200

    body = resp_one.json()
    assert body["id"] == model_id
    assert body["name"] == models[0]["name"]


def test_get_model_not_found(client):
    missing_id = 999_999_999
    resp = client.get(f"/models/{missing_id}")
    assert resp.status_code == 404
    assert "detail" in resp.json()


def test_create_model_unauthorised(client):
    payload = _unique_model_payload()
    resp = client.post("/models/", json=payload)  # no X-API-Key header
    assert resp.status_code == 401
    assert "detail" in resp.json()


def test_create_model_authorised(client, auth_headers):
    payload = _unique_model_payload()
    created_id = None

    resp = client.post("/models/", json=payload, headers=auth_headers)
    assert resp.status_code == 201

    body = resp.json()
    assert "id" in body
    created_id = body["id"]
    assert body["name"] == payload["name"]

    # quick sanity check: can read it back
    resp_get = client.get(f"/models/{created_id}")
    assert resp_get.status_code == 200
    assert resp_get.json()["id"] == created_id

    # cleanup so the DB doesn't bloat forever
    resp_del = client.delete(f"/models/{created_id}", headers=auth_headers)
    assert resp_del.status_code == 204