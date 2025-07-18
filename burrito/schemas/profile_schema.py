from pydantic import BaseModel

from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.group_schema import GroupResponseSchema


class ResponseRoleSchema(BaseModel):
    role_id: int
    name: str
    permission_list: list[str]


class CheckProfileSchema(BaseModel):
    user_id: int | None


class BaseProfile(BaseModel):
    """
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
    """
    This data must be transferred by user to update profile

    Args:
        registration_date (str): date when user registered account
    """

    faculty: FacultyResponseSchema | None
    group: GroupResponseSchema | None

    role: ResponseRoleSchema

    registration_date: str


class RequestUpdateProfileSchema(BaseModel):
    firstname: str | None
    lastname: str | None
    faculty: int | None
    group: int | None
    phone: str | None
    login: str | None
    password: str | None


class AdminRequestUpdateProfileSchema(BaseModel):
    firstname: str | None
    lastname: str | None
    faculty: int | None
    group: int | None
    phone: str | None
    user_id: int | None
    role_id: int | None
    login: str | None
