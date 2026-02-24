import uuid


def test_create_record_rejects_invalid_payload_422(client, auth_headers):
    # create a model first
    suffix = uuid.uuid4().hex[:8]
    model_payload = {
        "name": f"ValidationTest {suffix}",
        "series": "X Series",
        "body_style": "SUV",
        "fuel_type": "Diesel",
        "transmission": "Manual",
    }

    resp_model = client.post("/models/", json=model_payload, headers=auth_headers)
    assert resp_model.status_code == 201
    model_id = resp_model.json()["id"]

    try:
        # invalid record: year too low + price negative
        bad_record = {"year": 1800, "price": -10.0}
        resp = client.post(f"/models/{model_id}/records", json=bad_record, headers=auth_headers)

        assert resp.status_code == 422
        body = resp.json()
        assert "detail" in body  # FastAPI validation shape
    finally:
        client.delete(f"/models/{model_id}", headers=auth_headers)