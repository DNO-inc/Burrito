from burrito.models.issues_model import Issues
from burrito.models.roles_model import Roles
from burrito.models.statuses_model import Statuses
from burrito.models.tags_model import Tags
from burrito.models.user_model import Users
from burrito.models.faculty_model import Faculties
from burrito.models.group_model import Groups

from burrito.models.actions_model import Actions
from burrito.models.action_types_model import ActionTypes
from burrito.models.notifications_model import Notifications
from burrito.models.subscriptions_model import Subscriptions

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
            Roles, Tags, Statuses,
            Issues, Users, ActionTypes,
            Subscriptions, Actions, Notifications,
            Groups, Faculties
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
            Roles, Tags, Statuses,
            Issues, Users, ActionTypes,
            Subscriptions, Actions, Notifications,
            Groups, Faculties
        )
    )
    get_logger().warning("All tables was dropped")


def create_user(login: str, hashed_password: str) -> bool:
    """_summary_

    Create user with default fields: (login, hashed_password)

    Args:
        login (str): user login
        hashed_password (str): user hashed password

    Returns:
        bool: status creating new user
    """

    try:
        Users.create(login=login, password=hashed_password)
    except Exception as e:
        get_logger().error(str(e))
        return False

    return True


def get_user_by_login(login: str) -> Users | bool:
    """_summary_

    Get user if exist or return False

    Args:
        login (str): user login

    Returns:
        Users | bool: return False if user is not exist
    """

    try:
        return Users.get(Users.login == login)
    except Exception as e:
        return False
