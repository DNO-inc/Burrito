from peewee import (
    Model, CharField, PrimaryKeyField
)

from burrito.utils.db_cursor_object import postgresql_cursor


class ActionTypes(Model):
    action_type_id = PrimaryKeyField()
    name = CharField(255)

    class Meta:
        database = postgresql_cursor
