from peewee import (
    Model, BooleanField, PrimaryKeyField,
    ForeignKeyField
)

from burrito.models.actions_model import Actions
from burrito.models.user_model import Users

from burrito.utils.db_cursor_object import postgresql_cursor


class Notifications(Model):
    notification_id = PrimaryKeyField()
    action_id = ForeignKeyField(
        Actions,
        to_field="action_id",
        on_delete="NO ACTION"
    )
    user_id = ForeignKeyField(Users, to_field="user_id", on_delete="NO ACTION")
    read = BooleanField(default=False)

    class Meta:
        database = postgresql_cursor
