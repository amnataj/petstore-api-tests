PET_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "photoUrls", "status"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "photoUrls": {"type": "array", "items": {"type": "string"}},
        "status": {"enum": ["available", "pending", "sold"]},
    },
}
