from fastapi import HTTPException, status

from burrito.utils.logger import get_logger
from burrito.utils.transliteration import transliterate
from burrito.utils.converter import GroupConverter, FacultyConverter
from burrito.utils.query_util import ADMIN_ROLES

from burrito.schemas.registration_schema import RegistrationSchema

from burrito.models.roles_model import Roles
from burrito.models.user_model import Users


def create_user(
    user_data: RegistrationSchema
) -> Users:
    """_summary_

    Create user with default fields: (login, hashed_password)

    Args:
        login (str): user login
        hashed_password (str): user hashed password

    Returns:
        bool: status creating new user
    """

    role_object: Roles = Roles.get(Roles.name == "USER_ALL")

    # check if provided group/faculty is exist
    if user_data.group is not None:
        GroupConverter.convert(user_data.group)
    FacultyConverter.convert(user_data.faculty)

    try:
        user: Users = Users.create(
            firstname=user_data.firstname,
            lastname=user_data.lastname,
            login=user_data.login,
            password=user_data.password,  # password already hashed by argon2
            group=user_data.group,
            faculty=user_data.faculty,
            phone=user_data.phone,
            email=user_data.email,
            role=role_object
        )
        return user

    except Exception as e:  # pylint: disable=broad-except, invalid-name
        get_logger().info(
            f"""
                login: {user_data.login}
                group: {user_data.group}
                faculty: {user_data.faculty}
                role: {role_object.name}

            """
        )
        get_logger().error(e, exc_info=True)


def create_user_with_cabinet(
        user_id: int,
        firstname: str,
        lastname: str,
        faculty: int,
        group: int,
        email: int,
) -> Users | None:

    role_object: Roles = Roles.get(Roles.name == "USER_ALL")

    tmp_user_login = transliterate(f"{firstname} {lastname} {user_id}")

    try:
        user: Users = Users.create(
            user_id=user_id,
            firstname=firstname,
            lastname=lastname,
            login=tmp_user_login,
            faculty=faculty,
            group=group,
            email=email,
            role=role_object
        )
        return user

    except Exception as e:
        get_logger().error(e)


def get_user_by_login(login: str) -> Users | None:
    """_summary_

    Get user if exist or return None

    Args:
        login (str): user login

    Returns:
        Users | None: return None if user is not exist
    """

    return Users.get_or_none(Users.login == login)


def get_user_by_email_or_none(email: str) -> Users | None:
    """
    Get user if exist or return None

    Args:
        email (str): user email

    Returns:
        Users | None: return None if user is not exist
    """

    return Users.get_or_none(Users.email == email)


def get_user_by_id(user_id: int) -> Users | None:
    """_summary_

    Get user if exist or return None

    Args:
        user_id (int): user id

    Returns:
        Users | None: return None if user is not exist
    """

    _current_user = Users.get_or_none(Users.user_id == user_id)

    if not _current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID ({user_id}) is not exist"
        )

    return _current_user


def get_user_by_id_or_none(user_id: int) -> Users | None:
    """_summary_

    Get user if exist or return None

    Args:
        user_id (int): user id

    Returns:
        Users | None: return None if user is not exist
    """

    _current_user = Users.get_or_none(Users.user_id == user_id)

    return _current_user


def is_admin(user_id: int) -> bool:
    return get_user_by_id(user_id).role.role_id in ADMIN_ROLES
