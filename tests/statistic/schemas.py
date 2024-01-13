statistic_activity_schema = {
    "type": "object",
    "properties": {
        "average_process_time": {
            "type": "number"
        },
        "tickets_processed": {
            "type": "integer"
        },
        "users_registered": {
            "type": "integer"
        }
    }
}

statistic_faculty_schema = {
    "type": "object",
    "properties": {
        "faculties_data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "created_tickets_percent": {
                        "type": "number"
                    },
                    "faculty_id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "string"
                    },
                    "registered_users": {
                        "type": "integer"
                    }
                }
            }
        }
    }
}


statistic_period_schema = {
    "type": "object",
    "properties": {
        "scopes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string"
                    },
                    "scope": {
                        "type": "string"
                    },
                    "tickets_count": {
                        "type": "integer"
                    }
                }
            }
        },
        "statuses": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string"
                    },
                    "status_id": {
                        "type": "integer"
                    },
                    "status_name": {
                        "type": "string"
                    },
                    "tickets_count": {
                        "type": "integer"
                    }
                }
            }
        }
    }
}
