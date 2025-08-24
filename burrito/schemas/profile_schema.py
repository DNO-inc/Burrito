from typing import Optional

from pydantic import BaseModel

from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.group_schema import GroupResponseSchema


class ResponseRoleSchema(BaseModel):
    role_id: int
    name: str
    permission_list: list[str]


class CheckProfileSchema(BaseModel):
    user_id: int | None


class ResponseProfileSchema(BaseModel):
    """
    This data must be transferred by user to update profile

    Args:
        firstname (str | None): user firstname
        lastname (str | None): user lastname

        login (str): users login

        phone (str | None): phone
        email (str | None): email

        faculty (FacultyResponseSchema): faculty information
        group (GroupResponseSchema): group information

        role (ResponseRoleSchema): information about users's role

        registration_date (str): date when user registered account
    """

    firstname: Optional[str] = None
    lastname: Optional[str] = None

    login: str

    phone: Optional[str] = None
    email: Optional[str] = None

    faculty: Optional[FacultyResponseSchema] = None
    group: Optional[GroupResponseSchema] = None

    role: ResponseRoleSchema

    registration_date: str


class RequestUpdateProfileSchema(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    faculty: Optional[int] = None
    group: Optional[int] = None
    phone: Optional[str] = None
    login: Optional[str] = None
    password: Optional[str] = None


class AdminRequestUpdateProfileSchema(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    faculty: Optional[int] = None
    group: Optional[int] = None
    phone: Optional[str] = None
    user_id: Optional[int] = None
    role_id: Optional[int] = None
    login: Optional[str] = None
