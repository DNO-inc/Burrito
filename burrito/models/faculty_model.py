from peewee import Model, PrimaryKeyField, CharField

from burrito.utils.db_cursor_object import postgresql_cursor


class Faculties(Model):
    faculty_id = PrimaryKeyField()
    name = CharField(32)

    class Meta:
        database = postgresql_cursor
