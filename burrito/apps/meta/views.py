from playhouse.shortcuts import model_to_dict

from fastapi import Depends

from burrito.models.statuses_model import Statuses
from burrito.models.group_model import Groups
from burrito.models.faculty_model import Faculties
from burrito.models.queues_model import Queues
from burrito.models.user_model import Users
from burrito.models.roles_model import Roles
from burrito.models.role_permissions_model import RolePermissions

from burrito.schemas.meta_schema import (
    ResponseStatusesListSchema,
    ResponseGroupsListSchema,
    ResponseFacultiesListSchema,
    RequestQueueListSchema,
    ResponseQueueListSchema,
    ResponseAdminListSchema
)
from burrito.schemas.group_schema import GroupResponseSchema
from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.status_schema import StatusResponseSchema
from burrito.schemas.queue_schema import QueueResponseSchema

from burrito.utils.converter import FacultyConverter
from burrito.utils.tickets_util import make_short_user_data
from burrito.utils.query_util import MIN_ADMIN_PRIORITY
from burrito.utils.auth import get_current_user

from burrito.apps.meta.utils import RolesResponse, RolePermissionResponse


async def meta__get_statuses_list():
    return ResponseStatusesListSchema(
        statuses_list=[
            StatusResponseSchema(**model_to_dict(s)) for s in Statuses.select()
        ]
    )


async def meta__get_groups_list(_curr_user: Users = Depends(get_current_user())):
    return ResponseGroupsListSchema(
        groups_list=[
            GroupResponseSchema(
                **model_to_dict(group)
            ) for group in Groups.select()
        ]
    )


async def meta__faculties_list():
    return ResponseFacultiesListSchema(
        faculties_list=[
            FacultyResponseSchema(
                **model_to_dict(faculty)
            ) for faculty in Faculties.select()
        ]
    )


async def meta__get_queues_list(faculty: int):
    faculty_object = FacultyConverter.convert(faculty)

    response_list: list[QueueResponseSchema] = []
    for queue in Queues.select().where(
        Queues.faculty == faculty_object
    ):
        queue = model_to_dict(queue)
        queue["faculty"] = faculty_object.faculty_id

        response_list.append(
            QueueResponseSchema(
                **queue
            )
        )

    return ResponseQueueListSchema(queues_list=response_list)


async def meta__get_admins(_curr_user: Users = Depends(get_current_user())):
    return ResponseAdminListSchema(
        admin_list=[
            make_short_user_data(
                admin,
                hide_user_id=False
            ) for admin in Users.select().where(Users.role.priority in MIN_ADMIN_PRIORITY)
        ]
    )


async def meta__get_roles(_curr_user: Users = Depends(get_current_user())):
    return {
        "roles": [
            RolesResponse(**model_to_dict(role)) for role in Roles.select()
        ]
    }


async def meta__get_role_permissions(_curr_user: Users = Depends(get_current_user())):
    return {
        "role_permissions": [
            RolePermissionResponse(
                **model_to_dict(role)
            ) for role in RolePermissions.select()
        ]
    }
