from peewee import Model, PrimaryKeyField, CharField

from burrito.utils.db_cursor_object import get_database_cursor


class Groups(Model):
    group_id = PrimaryKeyField()
    name = CharField(10)

    class Meta:
        database = get_database_cursor()
