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

from burrito.utils.db_cursor_object import postgresql_cursor
from burrito.utils.logger import logger


def create_tables():
    """Create all tables using models in burrito/models"""

    postgresql_cursor.create_tables(
        (
            Roles, Tags, Statuses,
            Issues, Users, ActionTypes,
            Subscriptions, Actions, Notifications,
            Groups, Faculties
        )
    )
    logger.info("All tables was created")


def drop_tables(use: bool = False):
    """Drop all tables in database"""

    if not use:
        return

    postgresql_cursor.drop_tables(
        (
            Roles, Tags, Statuses,
            Issues, Users, ActionTypes,
            Subscriptions, Actions, Notifications,
            Groups, Faculties
        )
    )
    logger.warning("All tables was dropped")



def create_user(login: str, hashed_password: str) -> bool:
    """Create user with default fields: (login, hashed_password)"""

    try:
        Users.create(login=login, password=hashed_password)
    except Exception as e:
        logger.error(str(e))
        return False

    return True


def get_user_by_login(login: str) -> Users | bool:
    """Get user if exist or return False"""

    try:
        return Users.get(Users.login == login)
    except Exception as e:
        return False
