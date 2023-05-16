from pydantic import BaseModel


class ResponseStatusesListSchema(BaseModel):
    statuses_list: list[str]


class ResponseGroupsListSchema(BaseModel):
    groups_list: list[str]


class ResponseFacultiesListSchema(BaseModel):
    faculties_list: list[str]


class RequestQueueListSchema(BaseModel):
    faculty: str


class ResponseQueueListSchema(BaseModel):
    queues_list: list[str]
