
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
        "group": {
            "anyOf": [
                {
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
                },
                {
                    "type": "null"
                }
            ]
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
    "required": ["firstname", "lastname", "login", "division", "role", "registration_date"]
}
