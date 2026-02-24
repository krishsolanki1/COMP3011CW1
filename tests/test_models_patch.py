import uuid


def _unique_model_payload():
    suffix = uuid.uuid4().hex[:8]
    return {
        "name": f"PatchTest {suffix}",
        "series": "3 Series",
        "body_style": "Saloon",
        "fuel_type": "Petrol",
        "transmission": "Automatic",
    }


def test_patch_model_updates_only_provided_fields(client, auth_headers):
    # create a model we can safely mutate
    payload = _unique_model_payload()
    resp_create = client.post("/models/", json=payload, headers=auth_headers)
    assert resp_create.status_code == 201

    created = resp_create.json()
    model_id = created["id"]

    try:
        # patch only ONE field
        patch_payload = {"body_style": "Coupe"}
        resp_patch = client.patch(f"/models/{model_id}", json=patch_payload, headers=auth_headers)
        assert resp_patch.status_code == 200

        patched = resp_patch.json()
        assert patched["id"] == model_id
        assert patched["body_style"] == "Coupe"

        # other fields should remain unchanged
        assert patched["name"] == payload["name"]
        assert patched["series"] == payload["series"]
        assert patched["fuel_type"] == payload["fuel_type"]
        assert patched["transmission"] == payload["transmission"]

        # sanity: GET agrees
        resp_get = client.get(f"/models/{model_id}")
        assert resp_get.status_code == 200
        assert resp_get.json()["body_style"] == "Coupe"
    finally:
        # cleanup
        client.delete(f"/models/{model_id}", headers=auth_headers)