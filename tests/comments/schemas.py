
test_005_comments_get_comment_schema = {
    "type": "object",
    "properties": {
        "comment_id": {
            "type": "string"
        },
        "author": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer"
                },
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
                    },
                    "required": ["division_id", "name"]
                },
                "group": {
                    "oneOf": [
                        {
                            "type": "object",
                            "properties": {
                                "group_id": {
                                    "type": "integer"
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
                }
            },
            "required": ["user_id", "firstname", "lastname", "login", "division"]
        },
        "body": {
            "type": "string"
        },
        "creation_date": {
            "type": "string",
            "format": "date-time"
        },
        "type_": {
            "type": "string"
        },
        "reply_to": {
            "type": ["string", "null"]
        }
    },
    "required": ["comment_id", "author", "body", "creation_date", "type_"]
}
