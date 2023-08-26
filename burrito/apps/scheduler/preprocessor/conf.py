from burrito.models.group_model import Groups
from burrito.models.statuses_model import Statuses
from burrito.models.faculty_model import Faculties
from burrito.models.queues_model import Queues
from burrito.models.permissions_model import Permissions
from burrito.models.roles_model import Roles
from burrito.models.role_permissions_model import RolePermissions


MODEL_KEYS = {
    "groups": Groups,
    "faculties": Faculties,
    "statuses": Statuses,
    "queues": Queues,
    "permissions": Permissions,
    "roles": Roles,
    "role_permissions": RolePermissions
}

DEFAULT_CONFIG = {
    "__tables_option": {
        "groups": "SELECT * FROM `groups`;",
        "faculties": "SELECT * FROM `faculties`;",
        "statuses": "SELECT * FROM `statuses`;",
        "queues": "SELECT * FROM `queues`;",
        "permissions": "SELECT * FROM `permissions`;",
        "roles": "SELECT * FROM `roles`;",
        "role_permissions": "SELECT * FROM `role_permissions`;"
    },
    "groups": [],     # will be updated automatic
    "faculties": [],  # will be updated automatic
    "statuses": [
        {"status_id": 1, "name": "NEW"},
        {"status_id": 2, "name": "ACCEPTED"},
        {"status_id": 3, "name": "OPEN"},
        {"status_id": 4, "name": "WAITING"},
        {"status_id": 5, "name": "REJECTED"},
        {"status_id": 6, "name": "CLOSE"}
    ],
    "queues": [
        {"queue_id": 1, "name": "Lecturers", "faculty_id": 414, "scope": "Reports"},
        {"queue_id": 2, "name": "Food", "faculty_id": 414, "scope": "Reports"},
        {"queue_id": 3, "name": "Scholarship", "faculty_id": 414, "scope": "Q/A"},
        {"queue_id": 4, "name": "Dormitory", "faculty_id": 414, "scope": "Q/A"},
        {"queue_id": 5, "name": "Dormitory", "faculty_id": 414, "scope": "Reports"},
    ],
    "permissions": [
        {"permission_id": 1, "name": "UPDATE_PROFILE"},
        {"permission_id": 2, "name": "CREATE_TICKET"},
        {"permission_id": 3, "name": "READ_TICKET"},
        {"permission_id": 4, "name": "SEND_MESSAGE"},
        {"permission_id": 5, "name": "ADMIN"},
        {"permission_id": 6, "name": "GOD_MODE"}
    ],
    "roles": [
        {"role_id": 1, "name": "USER_ALL"},
        {"role_id": 2, "name": "USER_NO_M"},
        {"role_id": 3, "name": "USER_NO_CT"},
        {"role_id": 4, "name": "USER_NO_P"},
        {"role_id": 5, "name": "USER_NO_PCT"},
        {"role_id": 6, "name": "USER_NO_CTM"},
        {"role_id": 7, "name": "USER_NO_PM"},
        {"role_id": 8, "name": "USER_NO_PCTM"},
        {"role_id": 9, "name": "ADMIN"},
        {"role_id": 10, "name": "CHIEF_ADMIN"}
    ],
    "role_permissions": [
        {"role_id": 1, "permission_id": 1},
        {"role_id": 1, "permission_id": 2},
        {"role_id": 1, "permission_id": 3},
        {"role_id": 1, "permission_id": 4},

        {"role_id": 2, "permission_id": 1},
        {"role_id": 2, "permission_id": 2},
        {"role_id": 2, "permission_id": 3},

        {"role_id": 3, "permission_id": 1},
        {"role_id": 3, "permission_id": 3},
        {"role_id": 3, "permission_id": 4},

        {"role_id": 4, "permission_id": 2},
        {"role_id": 4, "permission_id": 3},
        {"role_id": 4, "permission_id": 4},

        {"role_id": 5, "permission_id": 3},
        {"role_id": 5, "permission_id": 4},

        {"role_id": 6, "permission_id": 1},
        {"role_id": 6, "permission_id": 3},

        {"role_id": 7, "permission_id": 2},
        {"role_id": 7, "permission_id": 3},

        {"role_id": 8, "permission_id": 3},

        {"role_id": 9, "permission_id": 1},
        {"role_id": 9, "permission_id": 2},
        {"role_id": 9, "permission_id": 3},
        {"role_id": 9, "permission_id": 4},
        {"role_id": 9, "permission_id": 5},

        {"role_id": 10, "permission_id": 1},
        {"role_id": 10, "permission_id": 2},
        {"role_id": 10, "permission_id": 3},
        {"role_id": 10, "permission_id": 4},
        {"role_id": 10, "permission_id": 5},
        {"role_id": 10, "permission_id": 6}
    ]
}
