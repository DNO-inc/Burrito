from peewee import Model, ForeignKeyField

from burrito.models.roles_model import Roles
from burrito.models.permissions_model import Permissions

from burrito.utils.db_cursor_object import get_database_cursor


class RolePermissions(Model):
    role_id = ForeignKeyField(
        Roles,
        field="role_id",
        on_delete="NO ACTIONS"
    )
    permission_id = ForeignKeyField(
        Permissions,
        field="permission_id",
        on_delete="NO ACTIONS"
    )

    class Meta:
        database = get_database_cursor()
        depends_on = [Roles, Permissions]
