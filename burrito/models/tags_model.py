from peewee import Model, PrimaryKeyField, CharField

from burrito.utils.db_cursor_object import get_database_cursor


class Tags(Model):
    tag_id = PrimaryKeyField()
    name = CharField(255)

    class Meta:
        database = get_database_cursor()
