from pydantic import BaseModel


class StatusResponseSchema(BaseModel):
    status_id: int
    name: str
