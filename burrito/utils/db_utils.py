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

    all_models = [
        Permissions,
        Roles,
        RolePermissions,
        Users, Faculties, Groups,
        Statuses, Deleted, Liked,
        Tickets, Participants,
        Subscriptions, Actions, Notifications,
        Comments, Queues, Bookmarks
    ]

    get_database_cursor().create_tables(all_models)

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
