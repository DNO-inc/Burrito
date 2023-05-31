from pydantic import BaseModel


class GroupResponseSchema(BaseModel):
    group_id: int
    name: str
