from pydantic import BaseModel


class FacultyResponseSchema(BaseModel):
    faculty_id: int
    name: str
