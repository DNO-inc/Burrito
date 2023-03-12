from peewee import Model, PrimaryKeyField, CharField

from burrito.utils.db_cursor_object import postgresql_cursor


class Tags(Model):
    tag_id = PrimaryKeyField()
    name = CharField(25)

    class Meta:
        database = postgresql_cursor
