from peewee import Model, PrimaryKeyField, ForeignKeyField

from burrito.models.user_model import Users
from burrito.models.issues_model import Issues

from burrito.utils.db_cursor_object import postgresql_cursor


class Subscriptions(Model):
    subscription_id = PrimaryKeyField()
    issue_id = ForeignKeyField(
        Issues,
        to_field="issue_id",
        on_delete="NO ACTION"
    )
    user_id = ForeignKeyField(Users, to_field="user_id", on_delete="NO ACTION")

    class Meta:
        database = postgresql_cursor
