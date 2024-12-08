from pydantic import BaseModel

from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.group_schema import GroupResponseSchema
from burrito.schemas.queue_schema import QueueResponseSchema
from burrito.schemas.status_schema import StatusResponseSchema


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


class ResponseAdminDetailSchema(BaseModel):
    user_id: int
    firstname: str | None
    lastname: str | None
    login: str
    faculty: FacultyResponseSchema
    group: GroupResponseSchema | None


class ResponseAdminListSchema(BaseModel):
    admin_list: list[ResponseAdminDetailSchema]
