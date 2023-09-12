from pydantic import BaseModel

from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.group_schema import GroupResponseSchema


class CheckProfileSchema(BaseModel):
    user_id: int | None


class BaseProfile(BaseModel):
    """_summary_

    This data must be transferred by user to update profile

    Args:
        firstname (str | None): user firstname
        lastname (str | None): user lastname

        login (str): users login

        faculty (str): faculty name
        group (str): group name

        phone (str | None): phone
        email (str | None): email
    """

    firstname: str | None
    lastname: str | None

    login: str

    faculty: int | None
    group: int | None

    phone: str | None
    email: str | None


class ResponseProfileSchema(BaseProfile):
    """_summary_

    This data must be transferred by user to update profile

    Args:
        registration_date (str): date when user registered account
    """

    faculty: FacultyResponseSchema | None
    group: GroupResponseSchema | None

    registration_date: str


class RequestUpdateProfileSchema(BaseProfile):
    login: str | None
    password: str | None
