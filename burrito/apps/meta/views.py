from fastapi import status
from fastapi.responses import JSONResponse

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

from burrito.utils.converter import FacultyStrToModel


async def meta__get_statuses_list():
    return ResponseStatusesListSchema(
        statuses_list=[
            s.name for s in Statuses.select()
        ]
    )


async def meta__get_groups_list():
    return ResponseGroupsListSchema(
        groups_list=[
            group.name for group in Groups.select()
        ]
    )


async def meta__faculties_list():
    return ResponseFacultiesListSchema(
        faculties_list=[
            faculty.name for faculty in Faculties.select()
        ]
    )


async def meta__get_queues_list(faculty_data: RequestQueueListSchema):
    faculty_id = FacultyStrToModel.convert(faculty_data.faculty)

    if not faculty_id:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Faculty name is wrong"}
        )

    return ResponseQueueListSchema(
        queues_list=[
            queue.name for queue in Queues.select().where(
                Queues.faculty==faculty_id
            )
        ]
    )
