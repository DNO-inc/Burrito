from pydantic import BaseModel


class QueueResponseSchema(BaseModel):
    queue_id: int
    division_id: int
    name: str
    scope: str
