import pytest


@pytest.mark.regression
@pytest.mark.parametrize("pet_id", ["abc", "-1", "0", "99999999999999999999"])
def test_get_pet_invalid_id(client, pet_id):
    r = client.get(f"/pet/{pet_id}")
    print(f"GET /pet/{pet_id} -> {r.status_code}")
    assert r.status_code in (400, 404)


@pytest.mark.regression
@pytest.mark.xfail(
    strict=True,
    reason="BUG-001: spec says 400 for invalid status value; API returns 200",
)
def test_find_by_invalid_status(client):
    r = client.get("/pet/findByStatus", params={"status": "invalid"})
    assert r.status_code == 400


@pytest.mark.regression
@pytest.mark.xfail(
    strict=True,
    reason="BUG-002: spec says 405 for invalid input; API returns 200 and accepts a pet without required name/photoUrls",
)
def test_create_pet_missing_required_fields(client):
    r = client.post("/pet", json={"status": "available"})
    assert r.status_code == 405
