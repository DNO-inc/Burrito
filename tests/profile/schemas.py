
profile_view_schema_template = {
    "type": "object",
    "properties": {
        "firstname": {
            "type": "string"
        },
        "lastname": {
            "type": "string"
        },
        "login": {
            "type": "string"
        },
        "division": {
            "type": "object",
            "properties": {
                "division_id": {
                    "type": "integer"
                },
                "name": {
                    "type": "string"
                }
            }
        },
        "groups": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "group_id": {
                        "type": "number"
                    },
                    "name": {
                        "type": "string"
                    }
                },
                "required": ["group_id", "name"]
            }
        },
        "phone": {
            "anyOf": [
                {"type": "null"},
                {"type": "string"}
            ]
        },
        "email": {
            "type": "string",
            "default": ""
        },
        "role": {
            "type": "object",
            "properties": {
                "role_id": {
                    "type": "integer"
                },
                "name": {
                    "type": "string"
                },
                "permission_list": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            }
        },
        "registration_date": {
            "type": "string",
            "format": "date-time"
        }
    },
    "required": ["firstname", "lastname", "login", "division", "groups", "role", "registration_date"]
}
