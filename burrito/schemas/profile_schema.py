from pydantic import BaseModel


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

    faculty: str | None
    group: str | None

    phone: str | None
    email: str | None


class ProfileSchema(BaseProfile):
    """_summary_

    This data must be transferred by user to update profile

    Args:
        registration_date (str): date when user registred account
    """

    registration_date: str


class UpdateProfileSchema(BaseProfile):
    login: str | None
