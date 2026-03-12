def _pick_model_with_records(client, max_checks=20):
    resp_models = client.get("/models")
    assert resp_models.status_code == 200
    models = resp_models.json()
    assert models, "Expected at least one seeded model in the DB"

    for m in models[:max_checks]:
        mid = m["id"]
        resp_recs = client.get(f"/models/{mid}/records")
        if resp_recs.status_code == 200 and isinstance(resp_recs.json(), list) and resp_recs.json():
            return mid, m, resp_recs.json()

    raise AssertionError("Couldn't find a model with records (expected imported data to include records).")


def test_average_price_for_existing_model(client):
    model_id, model, _records = _pick_model_with_records(client)

    resp = client.get(f"/analytics/average-price?model_id={model_id}")
    assert resp.status_code == 200

    body = resp.json()
    assert body["model_id"] == model_id
    assert body["model_name"] == model["name"]
    assert "average_price" in body
    assert isinstance(body["average_price"], (int, float))


def test_average_price_model_not_found(client):
    missing_id = 999_999_999
    resp = client.get(f"/analytics/average-price?model_id={missing_id}")
    assert resp.status_code == 404
    assert "detail" in resp.json()


def test_top_models_for_year(client):
    # Grab a year we *know* exists by looking at actual records.
    _model_id, _model, records = _pick_model_with_records(client)
    year = records[0]["year"]

    resp = client.get(f"/analytics/top-models?year={year}&limit=3")
    assert resp.status_code == 200

    body = resp.json()
    assert body["year"] == year
    assert "results" in body
    assert isinstance(body["results"], list)

    # If imported dataset is tiny, this could be 1, but should not be empty for a known year.
    assert body["results"], "Expected at least one top model for a year that exists in the records"

    first = body["results"][0]
    assert "model_id" in first
    assert "model_name" in first
    assert "average_price" in first
    assert "num_records" in first


def test_price_trend_for_existing_model(client):
    model_id, model, _records = _pick_model_with_records(client)

    resp = client.get(f"/analytics/price-trend?model_id={model_id}")
    assert resp.status_code == 200

    body = resp.json()
    assert body["model_id"] == model_id
    assert body["model_name"] == model["name"]
    assert "trend" in body
    assert isinstance(body["trend"], list)
    assert body["trend"], "Expected at least one trend point for a model with records"

    point = body["trend"][0]
    assert "year" in point
    assert "average_price" in point
    assert isinstance(point["average_price"], (int, float))
    assert "num_records" in point
    assert point["num_records"] >= 1


def test_price_trend_model_not_found(client):
    missing_id = 999_999_999
    resp = client.get(f"/analytics/price-trend?model_id={missing_id}")
    assert resp.status_code == 404
    assert "detail" in resp.json()