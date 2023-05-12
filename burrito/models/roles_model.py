from peewee import Model, AutoField, CharField

from burrito.utils.db_cursor_object import get_database_cursor


class Roles(Model):
    role_id = AutoField()
    name = CharField(32)

    class Meta:
        database = get_database_cursor()
