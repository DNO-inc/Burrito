import secrets
import string

from fastapi import HTTPException, status

from burrito.models.group_model import Groups
from burrito.models.roles_model import Roles
from burrito.models.user_groups_model import UserGroups
from burrito.models.user_model import Users
from burrito.schemas.registration_schema import RegistrationSchema
from burrito.utils.converter import DivisionConverter, GroupConverter
from burrito.utils.logger import get_logger
from burrito.utils.query_util import MIN_ADMIN_PRIORITY, MIN_CHIEF_ADMIN_PRIORITY
from burrito.utils.transliteration import transliterate


def create_user(
    user_data: RegistrationSchema
) -> Users:
    """
    Create user with default fields: (login, hashed_password)

    Args:
        login (str): user login
        hashed_password (str): user hashed password

    Returns:
        bool: status creating new user
    """

    role_object: Roles = Roles.get(Roles.name == "USER_ALL")

    # check if provided group/division is exist
    valid_groups: list[Groups] = []
    for group_id in user_data.group_ids:
        valid_groups.append(GroupConverter.convert(group_id))
    DivisionConverter.convert(user_data.division_id)

    try:
        user: Users = Users.create(
            firstname=user_data.firstname,
            lastname=user_data.lastname,
            login=user_data.login,
            password=user_data.password,  # password already hashed by argon2
            division=user_data.division_id,
            phone=user_data.phone,
            email=user_data.email,
            role=role_object
        )
        for group in valid_groups:
            UserGroups.create(
                user=user,
                group=group
            )
        return user

    except Exception as e:  # pylint: disable=broad-except, invalid-name
        get_logger().info(
            f"""
                login: {user_data.login}
                groups: {user_data.group_ids}
                division: {user_data.division_id}
                role: {role_object.name}

            """
        )
        get_logger().error(e, exc_info=True)


def create_user_with_cabinet(
    cabinet_id: str,
    firstname: str,
    lastname: str,
    division_id: int,
    group_ids: list[int],
    email: int,
) -> Users | None:

    role_object: Roles = Roles.get(Roles.name == "USER_ALL")

    salt = "".join([secrets.choice(string.digits) for i in range(6)])
    tmp_user_login = transliterate(f"{firstname} {salt}")

    try:
        DivisionConverter.convert(division_id)

    except Exception:
        get_logger().critical(f"Division is invalid: {division_id}")
        division_id = 1

    valid_groups: list[Groups] = []
    try:
        for group_id in group_ids:
            valid_groups.append(GroupConverter.convert(group_id))

    except Exception:
        get_logger().critical(f"Group is invalid: {group_ids}")
        group_ids = None

    try:
        user: Users = Users.create(
            cabinet_id=cabinet_id,
            firstname=firstname,
            lastname=lastname,
            login=tmp_user_login,
            division=division_id,
            email=email,
            role=role_object
        )
        for group in valid_groups:
            UserGroups.create(
                user=user,
                group=group
            )
        return user

    except Exception as e:
        get_logger().error(e)
        get_logger().warning(
            f"""
            Firstname {firstname}
            Lastname {lastname}
            Email {email}
            Login {tmp_user_login}
            Division {division}
            Group {group}

            """
        )


def get_user_by_login(login: str) -> Users | None:
    """
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
    """
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
    """
    Get user if exist or return None

    Args:
        user_id (int): user id

    Returns:
        Users | None: return None if user is not exist
    """

    return Users.get_or_none(Users.user_id == user_id)


def get_user_by_cabinet_id(cabinet_id: int) -> Users | None:
    """
    Get user by cabinet ID

    Args:
        cabinet_id (int): user's ID in SSU cabinet

    Returns:
        Users | None: return None if user is not exist
    """

    return Users.get_or_none(Users.cabinet_id == cabinet_id)


def is_admin(user: int | Users) -> bool:
    if isinstance(user, int):
        user = get_user_by_id(user)

    return user.role.priority >= MIN_ADMIN_PRIORITY


def is_chief_admin(user: int | Users) -> bool:
    if isinstance(user, int):
        user = get_user_by_id(user)

    return user.role.priority >= MIN_CHIEF_ADMIN_PRIORITY
