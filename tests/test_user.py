import pytest
from jsonschema import validate
from schemas.user_schema import USER_SCHEMA


@pytest.mark.smoke
def test_create_user(client, user_payload):
    r = client.post("/user", json=user_payload)
    assert r.status_code == 200
    fetched = client.get(f"/user/{user_payload['username']}")
    assert fetched.status_code == 200
    assert fetched.json()["username"] == user_payload["username"]
    client.delete(f"/user/{user_payload['username']}")


@pytest.mark.regression
def test_get_user(client, created_user):
    r = client.get(f"/user/{created_user['username']}")
    assert r.status_code == 200
    validate(r.json(), USER_SCHEMA)


@pytest.mark.regression
def test_update_user(client, created_user):
    created_user["firstName"] = "Updated"
    r = client.put(f"/user/{created_user['username']}", json=created_user)
    assert r.status_code == 200
    fetched = client.get(f"/user/{created_user['username']}")
    assert fetched.json()["firstName"] == "Updated"


@pytest.mark.regression
def test_delete_user(client, created_user):
    assert client.delete(f"/user/{created_user['username']}").status_code == 200
    assert client.get(f"/user/{created_user['username']}").status_code == 404


@pytest.mark.regression
def test_login_and_logout(client, created_user):
    r = client.get(
        "/user/login",
        params={"username": created_user["username"], "password": created_user["password"]},
    )
    assert r.status_code == 200
    assert "logged in" in r.text.lower()
    assert client.get("/user/logout").status_code == 200


@pytest.mark.regression
def test_get_unknown_user(client):
    r = client.get("/user/this_user_does_not_exist_98765")
    assert r.status_code == 404
