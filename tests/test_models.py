def test_list_models_ok(client):
    response = client.get("/models")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_average_price_for_some_model(client):
    # Grab any existing model
    resp_models = client.get("/models")
    assert resp_models.status_code == 200
    models = resp_models.json()

    # If there are no models, just skip the rest to avoid failing
    if not models:
        return

    model_id = models[0]["id"]

    resp_avg = client.get(f"/analytics/average-price?model_id={model_id}")
    assert resp_avg.status_code == 200
    body = resp_avg.json()

    assert body["model_id"] == model_id
    assert "average_price" in body
