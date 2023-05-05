from fastapi import Depends
from fastapi.responses import JSONResponse

from fastapi_jwt_auth import AuthJWT

from burrito.models.user_model import Users
from burrito.schemas.profile_schema import (
    ProfileSchema,
    UpdateProfileSchema,
    CheckProfileSchema
)

from .utils import (
    get_auth_core, get_user_by_id, update_user,
    BaseView,
    status,
    check_permission
)


class MyProfileView(BaseView):
    _permissions: list[str] = ["READ"]

    @staticmethod
    @check_permission
    async def post(profile: CheckProfileSchema) -> ProfileSchema:
        """Return some data to check user profile"""

        current_user: Users | None = get_user_by_id(profile.user_id)

        if not current_user:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"detail": f"User with {profile.user_id} is not exist"}
            )

        return ProfileSchema(
            firstname=current_user.firstname,
            lastname=current_user.lastname,
            login=current_user.login,
            faculty=str(current_user.faculty_id),  # TODO: get faculty name from DB
            group=str(current_user.group_id),      # TODO: get group name from DB
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
    ):
        """Update profile data"""

        Authorize.jwt_required()

        user_id = Authorize.get_jwt_subject()
        current_user: Users | None = get_user_by_id(user_id)
        if not current_user:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "detail": f"User with {user_id} is not exist"
                }
            )

        update_user(current_user, profile_updated_data)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": "Profile was updated"}
        )
