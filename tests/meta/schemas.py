
test_001_roles_schema = {
    "type": "object",
    "properties": {
        "roles": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "role_id": {"type": "number"},
                    "name": {"type": "string"}
                }
            }
        }
    }
}

test_002_role_permissions_schema = {
    "type": "object",
    "properties": {
        "role_permissions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "roles_id": {"type": "number"},
                    "name": {"type": "string"}
                }
            }
        }
    }
}

test_get_statuses_list_schema = {
    "type": "object",
    "properties": {
        "items": {
            "statuses_list": {
                "type": "object",
                "properties": {
                    "status_id": {"type": "number"},
                    "name": {"type": "string"}
                }
            }
        }
    }
}

test_groups_list_schema = {
    "type": "object",
    "properties": {
        "groups_list": {
            "type": "array",
            "items": {
                "group_id": {"type": "number"},
                "name": {"type": "string"}
            }
        }
    }
}

test_faculties_list_schema = {
    "type": "object",
    "properties": {
        "faculties_list": {
            "type": "array",
            "items": {
                "faculty_id": {"type": "number"},
                "name": {"type": "string"}
            }
        }
    }
}

test_queues_list_schema = {
    "type": "object",
    "properties": {
        "queues_list": {
            "type": "array",
            "items": {
                "queue_id": {"type": "number"},
                "faculty": {"type": "number"},
                "name": {"type": "string"},
                "scope": {"type": "string"}
            }
        }
    }
}

test_queues_list_with_wrong_faculty_schema = {
    "type": "object",
    "properties": {
        "detail": {"type": "string"}
    }
}

test_get_admin_list_schema = {
    "type": "object",
    "properties": {
        "admin_list": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "number"},
                    "firstname": {"type": "string"},
                    "lastname": {"type": "string"},
                    "login": {"type": "string"},
                    "faculty": {
                        "type": "object",
                        "properties": {
                            "faculty_id": {"type": "number"},
                            "name": {"type": "string"}
                        },
                        "required": ["faculty_id", "name"]
                    },
                    "group": {
                            "type": "null",
   #                         "properties": {
  #                              "group_id": {"type": "number"},
 #                               "name": {"type": "string"}
#                            }
                    }
                },
                "required": ["user_id", "firstname", "lastname", "login", "faculty", "group"]
            }
        }
    },
    "required": ["admin_list"]
}
