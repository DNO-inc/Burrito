from fastapi import status
from fastapi.responses import JSONResponse

from playhouse.shortcuts import model_to_dict

from burrito.models.statuses_model import Statuses
from burrito.models.group_model import Groups
from burrito.models.faculty_model import Faculties
from burrito.models.queues_model import Queues

from burrito.schemas.meta_schema import (
    ResponseStatusesListSchema,
    ResponseGroupsListSchema,
    ResponseFacultiesListSchema,
    RequestQueueListSchema,
    ResponseQueueListSchema
)
from burrito.schemas.group_schema import GroupResponseSchema
from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.status_schema import StatusResponseSchema
from burrito.schemas.queue_schema import QueueResponseSchema

from burrito.utils.converter import FacultyStrToModel


async def meta__get_statuses_list():
    return ResponseStatusesListSchema(
        statuses_list=[
            StatusResponseSchema(**model_to_dict(s)) for s in Statuses.select()
        ]
    )


async def meta__get_groups_list():
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


async def meta__get_queues_list(faculty_data: RequestQueueListSchema):
    faculty_object = FacultyStrToModel.convert(faculty_data.faculty)

    if not faculty_object:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Faculty name is wrong"}
        )

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
