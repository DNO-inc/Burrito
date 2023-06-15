from fastapi import HTTPException, status

from burrito.utils.converter import GroupStrToModel, FacultyStrToModel
from burrito.utils.logger import get_logger

from burrito.models.roles_model import Roles
from burrito.models.user_model import Users


def create_user_tmp_foo(
    login: str, hashed_password: str,
    group: str, faculty: str
) -> Users | None:
    """_summary_

    Create user with default fields: (login, hashed_password)

    Args:
        login (str): user login
        hashed_password (str): user hashed password

    Returns:
        bool: status creating new user
    """

    try:
        group_id = GroupStrToModel.convert(group)
        faculty_id = FacultyStrToModel.convert(faculty)

        if not (group_id and faculty_id):
            return

        user: Users = Users.create(
            login=login, password=hashed_password,
            group=group_id,
            faculty=faculty_id,
            role=Roles.get(Roles.name == "ALL")
        )
        return user

    except Exception as e:  # pylint: disable=broad-except, invalid-name
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
