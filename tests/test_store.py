import pytest
from jsonschema import validate
from schemas.order_schema import ORDER_SCHEMA


@pytest.mark.smoke
def test_place_order(client, order_payload):
    r = client.post("/store/order", json=order_payload)
    assert r.status_code == 200
    validate(r.json(), ORDER_SCHEMA)
    assert r.json()["quantity"] == order_payload["quantity"]
    client.delete(f"/store/order/{order_payload['id']}")


@pytest.mark.regression
def test_get_order(client, created_order):
    r = client.get(f"/store/order/{created_order['id']}")
    assert r.status_code == 200
    validate(r.json(), ORDER_SCHEMA)
    assert r.json()["id"] == created_order["id"]


@pytest.mark.regression
def test_delete_order(client, created_order):
    assert client.delete(f"/store/order/{created_order['id']}").status_code == 200
    assert client.get(f"/store/order/{created_order['id']}").status_code == 404


@pytest.mark.regression
def test_inventory(client):
    r = client.get("/store/inventory")
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, dict)
    assert all(isinstance(v, int) for v in body.values())


@pytest.mark.regression
@pytest.mark.parametrize("order_id", ["999999", "abc"])
def test_get_unknown_order(client, order_id):
    r = client.get(f"/store/order/{order_id}")
    print(f"GET /store/order/{order_id} -> {r.status_code}")
    assert r.status_code in (400, 404)
