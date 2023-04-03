from pydantic import BaseModel


class UpdateProfileSchema(BaseModel):
    """_summary_

    This data must be transferred by user to update profile

    Args:
        firstname (str): user firstname
        lastname (str): user lastname
        phone (str): phone
        email (str): email
    """

    firstname: str | None
    lastname: str | None
    phone: str | None
    email: str | None
