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
