from peewee import (
    Model, CharField, PrimaryKeyField
)

from burrito.utils.db_cursor_object import get_database_cursor


class ActionTypes(Model):
    action_type_id = PrimaryKeyField()
    name = CharField(255)

    class Meta:
        database = get_database_cursor()
