from fastapi import Depends
from playhouse.shortcuts import model_to_dict

from burrito.apps.meta.utils import RolePermissionResponse, RolesResponse
from burrito.models.division_model import Divisions
from burrito.models.group_model import Groups
from burrito.models.queues_model import Queues
from burrito.models.role_permissions_model import RolePermissions
from burrito.models.roles_model import Roles
from burrito.models.statuses_model import Statuses
from burrito.models.user_model import Users
from burrito.schemas.division_schema import DivisionResponseSchema
from burrito.schemas.group_schema import GroupResponseSchema
from burrito.schemas.meta_schema import (
    RequestQueueListSchema,
    ResponseAdminListSchema,
    ResponseFacultiesListSchema,
    ResponseGroupsListSchema,
    ResponseQueueListSchema,
    ResponseStatusesListSchema,
)
from burrito.schemas.queue_schema import QueueResponseSchema
from burrito.schemas.status_schema import StatusResponseSchema
from burrito.utils.auth import get_current_user
from burrito.utils.converter import DivisionConverter
from burrito.utils.query_util import MIN_ADMIN_PRIORITY
from burrito.utils.tickets_util import make_short_user_data


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


async def meta__divisions_list():
    return ResponseFacultiesListSchema(
        divisions_list=[
            DivisionResponseSchema(
                **model_to_dict(division)
            ) for division in Divisions.select()
        ]
    )


async def meta__get_queues_list(division_data: RequestQueueListSchema):
    division_object = DivisionConverter.convert(division_data.division_id)

    response_list: list[QueueResponseSchema] = []
    for queue in Queues.select().where(
        Queues.division == division_object
    ):
        queue = model_to_dict(queue)
        queue["division_id"] = division_object.division_id

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
            ) for admin in Users.select().join(
                Roles
            ).where(
                Roles.priority >= MIN_ADMIN_PRIORITY
            )
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
