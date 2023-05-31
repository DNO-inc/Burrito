from pydantic import BaseModel


class QueueResponseSchema(BaseModel):
    queue_id: int
    faculty: int
    name: str
