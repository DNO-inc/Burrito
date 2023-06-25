from pydantic import BaseModel

from burrito.schemas.group_schema import GroupResponseSchema
from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.status_schema import StatusResponseSchema
from burrito.schemas.queue_schema import QueueResponseSchema


class ResponseStatusesListSchema(BaseModel):
    statuses_list: list[StatusResponseSchema]


class ResponseGroupsListSchema(BaseModel):
    groups_list: list[GroupResponseSchema]


class ResponseFacultiesListSchema(BaseModel):
    faculties_list: list[FacultyResponseSchema]


class RequestQueueListSchema(BaseModel):
    faculty: int


class ResponseQueueListSchema(BaseModel):
    queues_list: list[QueueResponseSchema]
