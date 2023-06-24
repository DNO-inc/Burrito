from peewee import ForeignKeyField

from burrito.models.roles_model import Roles
from burrito.models.permissions_model import Permissions

from burrito.models.basic_model import BurritoBasicModel


class RolePermissions(BurritoBasicModel):
    role = ForeignKeyField(
        Roles,
        field="role_id",
        on_delete="CASCADE"
    )

    permission = ForeignKeyField(
        Permissions,
        field="permission_id",
        on_delete="CASCADE"
    )

    class Meta:
        depends_on = [Roles, Permissions]
