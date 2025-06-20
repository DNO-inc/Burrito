from pydantic import BaseModel

from burrito.schemas.division_schema import DivisionResponseSchema
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

        division (str): division name
        group (str): group name

        phone (str | None): phone
        email (str | None): email
    """

    firstname: str | None
    lastname: str | None

    login: str

    division_id: int | None
    group: int | None

    phone: str | None
    email: str | None


class ResponseProfileSchema(BaseProfile):
    """
    This data must be transferred by user to update profile

    Args:
        registration_date (str): date when user registered account
    """

    division: DivisionResponseSchema | None
    group: GroupResponseSchema | None

    role: ResponseRoleSchema

    registration_date: str


class RequestUpdateProfileSchema(BaseModel):
    firstname: str | None
    lastname: str | None
    division_id: int | None
    group: int | None
    phone: str | None
    login: str | None
    password: str | None


class AdminRequestUpdateProfileSchema(BaseModel):
    firstname: str | None
    lastname: str | None
    division_id: int | None
    group: int | None
    phone: str | None
    user_id: int | None
    role_id: int | None
    login: str | None
