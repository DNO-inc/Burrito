from fastapi import Depends

from fastapi_jwt_auth import AuthJWT

from burrito.models.user_model import Users
from burrito.schemas.profile_schema import UpdateProfileSchema

from burrito.utils.db_utils import get_user_by_login


async def my_profile(Authorize: AuthJWT = Depends()):
    """Return some data to check profile setting"""

    Authorize.jwt_required()

    current_user: Users | bool = get_user_by_login(Authorize.get_jwt_subject())

    return {
        "login": current_user.login,
        "firstname": current_user.firstname,
        "lastname": current_user.lastname,
        "phone": current_user.phone,
        "email": current_user.email,
        "registration_date": current_user.registration_date
    }


async def update_my_profile(
        profile_updated_data: UpdateProfileSchema,
        Authorize: AuthJWT = Depends()
        ):
    """Update profile data"""

    Authorize.jwt_required()

    current_user: Users | bool = get_user_by_login(Authorize.get_jwt_subject())

    current_user.firstname = profile_updated_data.firstname
    current_user.lastname = profile_updated_data.lastname
    current_user.phone = profile_updated_data.phone
    current_user.email = profile_updated_data.email

    current_user.save()  # save updates

    return profile_updated_data.json()
