import pytest


@pytest.mark.regression
@pytest.mark.parametrize("pet_id", ["abc", "-1", "0", "99999999999999999999"])
def test_get_pet_invalid_id(client, pet_id):
    r = client.get(f"/pet/{pet_id}")
    print(f"GET /pet/{pet_id} -> {r.status_code}")
    assert r.status_code in (400, 404)


@pytest.mark.regression
def test_find_by_invalid_status(client):
    r = client.get("/pet/findByStatus", params={"status": "invalid"})
    print(f"findByStatus=invalid -> {r.status_code}")
    assert r.status_code == 400


@pytest.mark.regression
def test_create_pet_missing_required_fields(client):
    r = client.post("/pet", json={"status": "available"})
    print(f"POST /pet missing fields -> {r.status_code}")
    assert r.status_code == 400
