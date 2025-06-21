from peewee import CompositeKey, ForeignKeyField

from burrito.models.basic_model import BurritoBasicModel
from burrito.models.group_model import Groups
from burrito.models.user_model import Users


class UserGroups(BurritoBasicModel):
    user = ForeignKeyField(
        Users,
        field="user_id",
        on_delete="CASCADE"
    )

    group = ForeignKeyField(
        Groups,
        field="group_id",
        on_delete="CASCADE"
    )

    class Meta:
        depends_on = [Users, Groups]
        primary_key = CompositeKey('user', 'group')
