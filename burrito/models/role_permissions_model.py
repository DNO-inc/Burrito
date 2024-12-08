from peewee import CompositeKey, ForeignKeyField

from burrito.models.basic_model import BurritoBasicModel
from burrito.models.permissions_model import Permissions
from burrito.models.roles_model import Roles


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
        primary_key = CompositeKey('role', 'permission')
