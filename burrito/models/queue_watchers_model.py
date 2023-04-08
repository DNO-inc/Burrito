from peewee import Model, PrimaryKeyField, ForeignKeyField

from burrito.models.user_model import Users

from burrito.utils.db_cursor_object import get_database_cursor


class QueueWatchers(Model):
    comment_id = PrimaryKeyField()
    user_id = ForeignKeyField(Users, to_field="user_id", on_delete="NO ACTION")

    class Meta:
        database = get_database_cursor()
