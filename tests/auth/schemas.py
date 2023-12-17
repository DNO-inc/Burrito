
test_002_refresh_access_token_schema = {
    "type": "object",
    "properties": {
        "user_id": {"type": "number"},
        "login": {"type": "string"},
        "access_token": {"type": "string"},
        "refresh_token": {"type": "null"}
    },
    "required": ["user_id", "login", "access_token", "refresh_token"]
}
