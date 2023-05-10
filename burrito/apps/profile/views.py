from fastapi import Depends
from fastapi.responses import JSONResponse

from fastapi_jwt_auth import AuthJWT

from burrito.models.group_model import Groups
from burrito.models.faculty_model import Faculties
from burrito.models.user_model import Users

from burrito.schemas.profile_schema import (
    ResponseProfileSchema,
    RequestUpdateProfileSchema,
    CheckProfileSchema
)

from .utils import (
    get_auth_core, get_user_by_id,
    BaseView,
    status,
    check_permission
)


class MyProfileView(BaseView):
    _permissions: list[str] = ["READ"]

    @staticmethod
    @check_permission
    async def post(
        profile: CheckProfileSchema,
        Authorize: AuthJWT = Depends(get_auth_core())
    ) -> ResponseProfileSchema:
        """Return some data to check user profile"""

        current_user_id = profile.user_id
        if profile.user_id is None:  # if user_id is not provided get user_id from token
            Authorize.jwt_required()
            current_user_id = Authorize.get_jwt_subject()

        current_user: Users | None = get_user_by_id(current_user_id)
        if not current_user:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"detail": f"User with {profile.user_id} is not exist"}
            )

        faculty_name = current_user.faculty_id
        group_name = current_user.group_id

        return ResponseProfileSchema(
            firstname=current_user.firstname,
            lastname=current_user.lastname,
            login=current_user.login,
            faculty=faculty_name.name if faculty_name else None,
            group=group_name.name if group_name else None,
            phone=current_user.phone,
            email=current_user.email,
            registration_date=str(current_user.registration_date)
        )


class UpdateMyProfile(BaseView):
    _permissions: list[str] = ["UPDATE"]

    @staticmethod
    async def post(
        profile_updated_data: RequestUpdateProfileSchema,
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

        if profile_updated_data.firstname:
            current_user.firstname = profile_updated_data.firstname

        if profile_updated_data.lastname:
            current_user.lastname = profile_updated_data.lastname

        if profile_updated_data.phone:
            current_user.phone = profile_updated_data.phone

        if profile_updated_data.email:
            current_user.email = profile_updated_data.email

        # check faculty
        faculty_id = Faculties.get_or_none(
            Faculties.faculty_id == profile_updated_data.faculty
        )

        if faculty_id and profile_updated_data.faculty:
            current_user.faculty_id = faculty_id

        # check group
        group_id = Groups.get_or_none(
            Groups.group_id == profile_updated_data.group
        )

        if group_id and profile_updated_data.group:
            current_user.group_id = group_id

        current_user.save()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": "Profile was updated"}
        )
