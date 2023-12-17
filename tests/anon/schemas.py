
scheme_test_anon_tickets_list_filter = {
  "type": "object",
  "$defs": {
    "user": {
      "type": ["object", "null"],
      "properties": {
        "user_id": { "type": "null" },
        "firstname": { "type": "null" },
        "lastname": { "type": "null" },
        "login": { "type": "null" },
        "faculty": { "$ref": "#/$defs/faculty" }
      },
      "required": ["user_id", "firstname", "lastname", "login", "faculty"]
    },
    "faculty": {
      "type": "object",
      "properties": {
        "faculty_id": { "type": "number" },
        "name": { "type": "string" }
      },
      "required": ["faculty_id", "name"]
    }
  },
  "properties": {
    "ticket_list": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "creator": { "$ref": "#/$defs/user" },
          "assignee": { "$ref": "#/$defs/user" },
          "ticket_id": { "type": "number" },
          "subject": { "type": "string" },
          "body": { "type": "string" },
          "faculty": { "$ref": "#/$defs/faculty" },
          "queue": {
            "type": "object",
            "properties": {
              "queue_id": { "type": "number" },
              "faculty": { "type": "number" },
              "name": { "type": "string" },
              "scope": { "type": "string" }
            },
            "required": ["queue_id", "faculty", "name", "scope"]
          },
          "status": {
            "type": "object",
            "properties": {
              "status_id": { "type": "number" },
              "name": { "type": "string" }
            },
            "required": ["status_id", "name"]
          },
          "upvotes": { "type": "number" },
          "date": { "type": "string" }
        },
        "required": ["assignee", "ticket_id", "subject", "body", "faculty", "queue", "status", "upvotes", "date"]
      }
    },
    "total_pages": { "type": "number" }
  },
  "required": ["ticket_list", "total_pages"]
}
