
test_001_get_notifications_schema = {
    "type": "object",
    "properties": {
        "notifications": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "ticket_id": {"type": "number"},
                    "user_id": {"type": "number"},
                    "body_ua": {"type": "string"},
                    "body": {"type": "string"}
                }
            }
        }
    }
}
