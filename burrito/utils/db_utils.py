from burrito.models.issues_model import Issues
from burrito.models.roles_model import Roles
from burrito.models.statuses_model import Statuses
from burrito.models.tags_model import Tags
from burrito.models.user_model import Users

from burrito.models.actions_model import Actions
from burrito.models.action_types_model import ActionTypes
from burrito.models.notifications_model import Notifications
from burrito.models.subscriptions_model import Subscriptions

from burrito.utils.db_cursor_object import postgresql_cursor


def create_tables():
    """Create all tables using models in burrito/models"""

    postgresql_cursor.create_tables(
        (
            Roles, Tags, Statuses,
            Issues, Users, ActionTypes,
            Subscriptions, Actions, Notifications
        )
    )


def create_user(login: str, hashed_password: str) -> bool:
    """Create user with default fields: (login, hashed_password)"""

    try:
        Users.create(login=login, hashed_password=hashed_password)
    except Exception as e:
        return False

    return True


def get_user_by_login(login: str) -> Users | bool:
    """Get user if exist or return False"""

    try:
        return Users.get(Users.login == login)
    except Exception as e:
        return False
