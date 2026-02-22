import uuid


def test_write_with_wrong_api_key_rejected(client):
    suffix = uuid.uuid4().hex[:8]
    payload = {
        "name": f"Should Not Create {suffix}",
        "series": "Nope",
        "body_style": "Nope",
        "fuel_type": "Nope",
        "transmission": "Nope",
    }

    resp = client.post("/models/", json=payload, headers={"X-API-Key": "definitely-wrong-key"})
    assert resp.status_code == 401
    assert "detail" in resp.json()