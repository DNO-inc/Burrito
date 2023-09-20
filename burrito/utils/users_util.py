from random import randint

from fastapi import HTTPException, status

from burrito.utils.logger import get_logger
from burrito.utils.transliteration import transliterate

from burrito.models.roles_model import Roles
from burrito.models.user_model import Users
from burrito.models.group_model import Groups
from burrito.models.faculty_model import Faculties


def create_user_tmp_foo(
        login: str, hashed_password: str,
        group: Groups, faculty: Faculties
) -> Users | None:
    """_summary_

    Create user with default fields: (login, hashed_password)

    Args:
        login (str): user login
        hashed_password (str): user hashed password

    Returns:
        bool: status creating new user
    """

    role_object: Roles = Roles.get(Roles.name == "USER_ALL")

    try:
        user: Users = Users.create(
            login=login, password=hashed_password,
            group=group,
            faculty=faculty,
            role=role_object
        )
        return user

    except Exception as e:  # pylint: disable=broad-except, invalid-name
        get_logger().info(
            f"""
                login: {login}
                group: {group.name}
                faculty: {faculty.name}
                role: {role_object.name}

            """
        )
        get_logger().error(e)


# TODO: delete this function
def create_user(login: str, hashed_password: str) -> int | None:
    """_summary_

    Create user with default fields: (login, hashed_password)

    Args:
        login (str): user login
        hashed_password (str): user hashed password

    Returns:
        bool: status creating new user
    """

    try:
        user: Users = Users.create(
            login=login, password=hashed_password
        )
        return user.user_id

    except Exception as e:  # pylint: disable=broad-except, invalid-name
        get_logger().error(e)


def create_user_with_cabinet(
        user_id: int,
        firstname: str,
        lastname: str,
        faculty: int,
        group: int,
        email: int,
) -> Users | None:

    role_object: Roles = Roles.get(Roles.name == "USER_ALL")

    tmp_user_login = transliterate(f"{lastname} {firstname}")
    while get_user_by_login(tmp_user_login):
        tmp_user_login = transliterate(f"{lastname} {firstname} {randint(1, 1000)}")

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
