from pydantic import BaseModel


class QueueResponseSchema(BaseModel):
    queue_id: int
    division: int
    name: str
    scope: str
