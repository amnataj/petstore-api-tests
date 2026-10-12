import random
import pytest
from api.client import ApiClient


@pytest.fixture(scope="session")
def client():
    return ApiClient()


@pytest.fixture
def pet_payload():
    return {
        "id": random.randint(10**6, 10**9),
        "name": f"test-pet-{random.randint(1, 9999)}",
        "category": {"id": 1, "name": "dogs"},
        "photoUrls": ["https://example.com/pet.jpg"],
        "tags": [{"id": 1, "name": "qa"}],
        "status": "available",
    }


@pytest.fixture
def created_pet(client, pet_payload):
    r = client.post("/pet", json=pet_payload)
    assert r.status_code == 200
    yield pet_payload
    client.delete(f"/pet/{pet_payload['id']}")


@pytest.fixture
def order_payload():
    # Petstore documents valid order IDs as 1-10
    return {
        "id": random.randint(1, 10),
        "petId": 1,
        "quantity": 2,
        "shipDate": "2026-10-12T10:00:00.000+0000",
        "status": "placed",
        "complete": True,
    }


@pytest.fixture
def created_order(client, order_payload):
    r = client.post("/store/order", json=order_payload)
    assert r.status_code == 200
    yield order_payload
    client.delete(f"/store/order/{order_payload['id']}")


@pytest.fixture
def user_payload():
    suffix = random.randint(10**5, 10**9)
    return {
        "id": suffix,
        "username": f"qa_user_{suffix}",
        "firstName": "Test",
        "lastName": "User",
        "email": f"qa_user_{suffix}@example.com",
        "password": "Passw0rd!",
        "phone": "1234567890",
        "userStatus": 1,
    }


@pytest.fixture
def created_user(client, user_payload):
    r = client.post("/user", json=user_payload)
    assert r.status_code == 200
    yield user_payload
    client.delete(f"/user/{user_payload['username']}")
