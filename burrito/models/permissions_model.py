from peewee import Model, PrimaryKeyField, CharField

from burrito.utils.db_cursor_object import get_database_cursor


class Permissions(Model):
    permission_id = PrimaryKeyField()
    name = CharField(max_length=20)

    class Meta:
        database = get_database_cursor()
