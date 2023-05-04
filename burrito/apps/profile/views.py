from fastapi import Depends

from fastapi_jwt_auth import AuthJWT

from burrito.models.user_model import Users
from burrito.schemas.profile_schema import ProfileSchema, UpdateProfileSchema

from .utils import (
    get_auth_core, get_user_by_id, update_user,
    BaseView
)


class MyProfileView(BaseView):
    _permissions: list[str] = ["READ"]

    @staticmethod
    async def post(Authorize: AuthJWT = Depends(get_auth_core())) -> ProfileSchema:
        """Return some data to check user profile"""

        Authorize.jwt_required()

        current_user: Users | bool = get_user_by_id(
            Authorize.get_jwt_subject()
        )

        return ProfileSchema(
            firstname=current_user.firstname,
            lastname=current_user.lastname,
            login=current_user.login,
            faculty=str(current_user.faculty_id),
            group=str(current_user.group_id),
            phone=current_user.phone,
            email=current_user.email,
            registration_date=str(current_user.registration_date)
        )


class UpdateMyProfile(BaseView):
    _permissions: list[str] = ["UPDATE"]

    @staticmethod
    async def post(
        profile_updated_data: UpdateProfileSchema,
        Authorize: AuthJWT = Depends(get_auth_core())
    ) -> object:
        """Update profile data"""

        Authorize.jwt_required()

        current_user: Users | bool = get_user_by_id(Authorize.get_jwt_subject())
        update_user(current_user, profile_updated_data)

        return profile_updated_data.json()
