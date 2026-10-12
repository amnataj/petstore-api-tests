import pytest
from jsonschema import validate
from schemas.pet_schema import PET_SCHEMA


@pytest.mark.smoke
def test_create_pet(client, pet_payload):
    r = client.post("/pet", json=pet_payload)
    assert r.status_code == 200
    validate(r.json(), PET_SCHEMA)
    assert r.json()["name"] == pet_payload["name"]
    client.delete(f"/pet/{pet_payload['id']}")


@pytest.mark.smoke
def test_get_pet(client, created_pet):
    r = client.get(f"/pet/{created_pet['id']}")
    assert r.status_code == 200
    validate(r.json(), PET_SCHEMA)
    assert r.json()["id"] == created_pet["id"]


@pytest.mark.regression
def test_update_pet(client, created_pet):
    created_pet["status"] = "sold"
    r = client.put("/pet", json=created_pet)
    assert r.status_code == 200
    assert client.get(f"/pet/{created_pet['id']}").json()["status"] == "sold"


@pytest.mark.regression
def test_delete_pet(client, created_pet):
    assert client.delete(f"/pet/{created_pet['id']}").status_code == 200
    assert client.get(f"/pet/{created_pet['id']}").status_code == 404


@pytest.mark.regression
@pytest.mark.parametrize("status", ["available", "pending", "sold"])
def test_find_by_status(client, status):
    r = client.get("/pet/findByStatus", params={"status": status})
    assert r.status_code == 200
    assert all(p["status"] == status for p in r.json())
