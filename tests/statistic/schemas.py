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
                    "faculty_id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "string"
                    },
                    "created_tickets_count": {
                        "type": "number"
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
                    "scope": {
                        "type": "string"
                    },
                    "tickets_count": {
                        "type": "integer"
                    }
                }
            }
        },
        "faculty_scopes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "faculty_id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "string"
                    },
                    "reports_count": {
                        "type": "integer"
                    },
                    "qa_count": {
                        "type": "integer"
                    },
                    "suggestion": {
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
                    "status_id": {
                        "type": "integer"
                    },
                    "name": {
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
