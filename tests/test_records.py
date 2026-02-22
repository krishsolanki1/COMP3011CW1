import uuid


def _pick_model_with_records(client, max_checks=20):
    resp_models = client.get("/models")
    assert resp_models.status_code == 200
    models = resp_models.json()
    assert models, "Expected at least one seeded model in the DB"

    # Try a few models until we find one that actually has records.
    for m in models[:max_checks]:
        mid = m["id"]
        resp_recs = client.get(f"/models/{mid}/records")
        if resp_recs.status_code == 200 and isinstance(resp_recs.json(), list) and resp_recs.json():
            return mid, m, resp_recs.json()

    raise AssertionError("Couldn't find a model with records (expected imported data to include records).")


def test_list_records_for_model_ok(client):
    model_id, _model, records = _pick_model_with_records(client)

    # already fetched records via helper, but keep it readable:
    assert isinstance(records, list)
    assert records, "Expected at least one record for the chosen model"

    first = records[0]
    assert "id" in first
    assert first["car_model_id"] == model_id
    assert "year" in first
    assert "price" in first


def test_create_record_authorised(client, auth_headers):
    # Create a fresh model so we can safely add a record + clean up after.
    suffix = uuid.uuid4().hex[:8]
    payload_model = {
        "name": f"Test BMW Model For Records {suffix}",
        "series": "Test Series",
        "body_style": "Saloon",
        "fuel_type": "Diesel",
        "transmission": "Manual",
    }

    created_model_id = None
    created_record_id = None

    resp_model = client.post("/models/", json=payload_model, headers=auth_headers)
    assert resp_model.status_code == 201
    created_model_id = resp_model.json()["id"]

    payload_record = {"year": 2020, "price": 12345.67}
    resp_record = client.post(
        f"/models/{created_model_id}/records",
        json=payload_record,
        headers=auth_headers,
    )
    assert resp_record.status_code == 201

    rec_body = resp_record.json()
    assert rec_body["car_model_id"] == created_model_id
    assert rec_body["year"] == payload_record["year"]
    assert abs(rec_body["price"] - payload_record["price"]) < 0.0001
    created_record_id = rec_body["id"]

    # sanity check: record shows up in list
    resp_list = client.get(f"/models/{created_model_id}/records")
    assert resp_list.status_code == 200
    ids = [r["id"] for r in resp_list.json()]
    assert created_record_id in ids

    # cleanup: deleting model should cascade delete the records
    resp_del = client.delete(f"/models/{created_model_id}", headers=auth_headers)
    assert resp_del.status_code == 204


def test_create_record_model_not_found(client, auth_headers):
    missing_id = 999_999_999
    payload_record = {"year": 2020, "price": 9999.99}

    resp = client.post(f"/models/{missing_id}/records", json=payload_record, headers=auth_headers)
    assert resp.status_code == 404
    assert "detail" in resp.json()