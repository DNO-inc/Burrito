
detail_response_schema_template = {
    "type": "object",
    "properties": {
        "detail": {"type": "string"}
    },
    "required": ["detail"]
}

tickets_list_response_schema_template = {
  "type": "object",
  "properties": {
    "ticket_list": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "anonymous": { "type": "boolean" },
          "assignee": {
            "type": ["null", "object"],
            "properties": {
              "faculty": {
                "type": ["null", "object"],
                "properties": {
                  "faculty_id": { "type": "integer" },
                  "name": { "type": "string" }
                }
              },
              "firstname": { "type": "string" },
              "group": { "type": ["null", "object"] },
              "lastname": { "type": "string" },
              "login": { "type": "string" },
              "user_id": { "type": "integer" }
            }
          },
          "body": { "type": "string" },
          "creator": {
            "type": ["null", "object"],
            "properties": {
              "faculty": {
                "type": ["null", "object"],
                "properties": {
                  "faculty_id": { "type": "integer" },
                  "name": { "type": "string" }
                }
              },
              "firstname": { "type": "string" },
              "group": { "type": ["null", "object"] },
              "lastname": { "type": "string" },
              "login": { "type": "string" },
              "user_id": { "type": "integer" }
            }
          },
          "date": { "type": "string", "format": "date-time" },
          "faculty": {
            "type": "object",
            "properties": {
              "faculty_id": { "type": "integer" },
              "name": { "type": "string" }
            },
            "required": ["faculty_id", "name"]
          },
          "hidden": { "type": "boolean" },
          "is_bookmarked": { "type": "boolean" },
          "is_followed": { "type": "boolean" },
          "is_liked": { "type": "boolean" },
          "queue": {
            "type": "object",
            "properties": {
              "faculty": { "type": "integer" },
              "name": { "type": "string" },
              "queue_id": { "type": "integer" },
              "scope": { "type": "string" }
            },
            "required": ["faculty", "name", "queue_id", "scope"]
          },
          "status": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "status_id": { "type": "integer" }
            },
            "required": ["name", "status_id"]
          },
          "subject": { "type": "string" },
          "ticket_id": { "type": "integer" },
          "upvotes": { "type": "integer" }
        },
        "required": [
          "anonymous",
          "assignee",
          "body",
          "creator",
          "date",
          "faculty",
          "hidden",
          "is_bookmarked",
          "is_followed",
          "is_liked",
          "queue",
          "status",
          "subject",
          "ticket_id",
          "upvotes"
        ]
      }
    },
    "total_pages": { "type": "integer" }
  },
  "required": ["ticket_list", "total_pages"]
}

test_009_ticket_detail_view_schemas = {
  "type": "object",
  "properties": {
    "anonymous": { "type": "boolean" },
    "assignee": { "type": ["null", "object"] },
    "body": { "type": "string" },
    "creator": {
      "type": "object",
      "properties": {
        "faculty": {
          "type": "object",
          "properties": {
            "faculty_id": { "type": "integer" },
            "name": { "type": "string" }
          },
          "required": ["faculty_id", "name"]
        },
        "firstname": { "type": "string" },
        "group": { "type": ["null", "object"] },
        "lastname": { "type": "string" },
        "login": { "type": "string" },
        "user_id": { "type": "integer" }
      },
      "required": ["faculty", "firstname", "group", "lastname", "login", "user_id"]
    },
    "date": { "type": "string", "format": "date-time" },
    "faculty": {
      "type": "object",
      "properties": {
        "faculty_id": { "type": "integer" },
        "name": { "type": "string" }
      },
      "required": ["faculty_id", "name"]
    },
    "hidden": { "type": "boolean" },
    "is_bookmarked": { "type": "boolean" },
    "is_followed": { "type": "boolean" },
    "is_liked": { "type": "boolean" },
    "queue": {
      "type": "object",
      "properties": {
        "faculty": { "type": "integer" },
        "name": { "type": "string" },
        "queue_id": { "type": "integer" },
        "scope": { "type": "string" }
      },
      "required": ["faculty", "name", "queue_id", "scope"]
    },
    "status": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "status_id": { "type": "integer" }
      },
      "required": ["name", "status_id"]
    },
    "subject": { "type": "string" },
    "ticket_id": { "type": "integer" },
    "upvotes": { "type": "integer" }
  },
  "required": [
    "anonymous",
    "assignee",
    "body",
    "creator",
    "date",
    "faculty",
    "hidden",
    "is_bookmarked",
    "is_followed",
    "is_liked",
    "queue",
    "status",
    "subject",
    "ticket_id",
    "upvotes"
  ]
}

test_016_get_full_ticket_history_schema = {
  "type": "object",
  "properties": {
    "history": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "author": {
            "type": "object",
            "properties": {
              "faculty": {
                "type": "object",
                "properties": {
                  "faculty_id": { "type": "integer" },
                  "name": { "type": "string" }
                },
                "required": ["faculty_id", "name"]
              },
              "firstname": { "type": "string" },
              "group": { "type": ["null", "string"] },
              "lastname": { "type": "string" },
              "login": { "type": "string" },
              "user_id": { "type": "integer" }
            },
            "required": ["faculty", "firstname", "group", "lastname", "login", "user_id"]
          },
          "body": { "type": ["null", "string"] },
          "comment_id": { "type": "string" },
          "creation_date": { "type": "string", "format": "date-time" },
          "field_name": { "type": "string" },
          "file_meta_action": { "type": ["null", "string"] },
          "new_value": { "type": ["null", "string"] },
          "old_value": { "type": ["null", "string"] },
          "reply_to": { "type": ["null", "string"] },
          "ticket_id": { "type": "integer" },
          "type_": { "type": "string" },
          "value": { "type": ["null", "string"] }
        },
        "required": ["author", "creation_date", "type_", "ticket_id"]
      }
    },
    "page_count": { "type": "integer" }
  },
  "required": ["history", "page_count"]
}
