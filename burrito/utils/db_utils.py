from fastapi import HTTPException, status

from burrito.models.tickets_model import Tickets
from burrito.models.roles_model import Roles
from burrito.models.statuses_model import Statuses
from burrito.models.user_model import Users
from burrito.models.faculty_model import Faculties
from burrito.models.group_model import Groups
from burrito.models.deleted_model import Deleted
from burrito.models.liked_model import Liked

from burrito.models.comments_model import Comments
from burrito.models.actions_model import Actions
from burrito.models.participants_model import Participants
from burrito.models.queues_model import Queues
from burrito.models.notifications_model import Notifications
from burrito.models.subscriptions_model import Subscriptions

from burrito.models.bookmarks_model import Bookmarks

from burrito.models.permissions_model import Permissions
from burrito.models.role_permissions_model import RolePermissions

from burrito.utils.converter import GroupStrToInt, FacultyStrToInt
from burrito.utils.db_cursor_object import get_database_cursor
from burrito.utils.logger import get_logger


def setup_database():
    """_summary_

    Setup database. Insert base roles, etc
    """


def create_tables():
    """_summary_

    Create all tables using models in burrito/models
    """

    get_database_cursor().create_tables(
        (
            Permissions,
            Roles,
            RolePermissions,
            Users, Faculties, Groups,
            Statuses, Deleted, Liked,
            Tickets, Participants,
            Subscriptions, Actions, Notifications,
            Comments, Queues, Bookmarks
        )
    )
    get_logger().info("All tables was created")


def drop_tables(use: bool = False):
    """_summary_

    Drop all tables in database

    Args:
        use (bool, optional): To confirm the reset of the table . Defaults to False.
    """

    if not use:
        return

    get_database_cursor().drop_tables(
        (
            Permissions,
            Roles,
            RolePermissions,
            Users, Faculties, Groups,
            Statuses, Deleted, Liked,
            Tickets, Participants,
            Subscriptions, Actions, Notifications,
            Comments, Queues, Bookmarks
        )
    )
    get_logger().warning("All tables was dropped")


def create_user_tmp_foo(
        login: str, hashed_password: str,
        group: str, faculty: str
) -> int | None:
    """_summary_

    Create user with default fields: (login, hashed_password)

    Args:
        login (str): user login
        hashed_password (str): user hashed password

    Returns:
        bool: status creating new user
    """

    try:
        group_id = GroupStrToInt.convert(group)
        faculty_id = FacultyStrToInt.convert(faculty)

        if not (group_id and faculty_id):
            return

        user: Users = Users.create(
            login=login, password=hashed_password,
            group=group_id,
            faculty=faculty_id,
            role=Roles.get(Roles.name == "ALL")
        )
        return user.user_id

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
            detail=f"User with {user_id} is not exist"
        )

    return _current_user
