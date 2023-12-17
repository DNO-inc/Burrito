
test_check_version_schema = {
    "type": "object",
    "properties": {
        "name": {"version": "string"}
    },
    "required": ["version"]
}

test_check_updates_schema = {
    "type": "object",
    "properties": {
        "name": {"changelog": "string"}
    },
    "required": ["changelog"]
}

test_check_team_schema = {
    "type": "object",
    "properties": {
        "name": {"team": "string"}
    },
    "required": ["team"]
}