from pydantic import BaseModel


class DivisionResponseSchema(BaseModel):
    division_id: int
    name: str
