from burrito.models.bookmarks_model import Bookmarks
from burrito.models.deleted_model import Deleted
from burrito.models.division_model import Divisions
from burrito.models.group_model import Groups
from burrito.models.liked_model import Liked
from burrito.models.participants_model import Participants
from burrito.models.permissions_model import Permissions
from burrito.models.queues_model import Queues
from burrito.models.role_permissions_model import RolePermissions
from burrito.models.roles_model import Roles
from burrito.models.statuses_model import Statuses
from burrito.models.subscriptions_model import Subscriptions
from burrito.models.tickets_model import Tickets
from burrito.models.user_model import Users
from burrito.utils.db_cursor_object import get_database_cursor
from burrito.utils.logger import get_logger


def create_tables():
    """
    Create all tables using models in burrito/models
    """

    all_models = [
        Permissions,
        Roles,
        RolePermissions,
        Users, Divisions, Groups,
        Statuses, Deleted, Liked,
        Tickets, Participants,
        Subscriptions, Queues, Bookmarks
    ]

    try:
        get_database_cursor().create_tables(all_models)
    except Exception as e:
        get_logger().warning(f"{e}", exc_info=True)
    else:
        get_logger().info("All tables was created")


def drop_tables(use: bool = False):
    """
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
            Users, Divisions, Groups,
            Statuses, Deleted, Liked,
            Tickets, Participants,
            Subscriptions, Queues, Bookmarks
        )
    )
    get_logger().warning("All tables was dropped", exc_info=True)
