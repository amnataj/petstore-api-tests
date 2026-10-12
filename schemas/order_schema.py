ORDER_SCHEMA = {
    "type": "object",
    "required": ["id", "petId", "quantity", "status"],
    "properties": {
        "id": {"type": "integer"},
        "petId": {"type": "integer"},
        "quantity": {"type": "integer"},
        "status": {"enum": ["placed", "approved", "delivered"]},
        "complete": {"type": "boolean"},
    },
}
