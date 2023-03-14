import datetime

from peewee import (
    Model, TextField, PrimaryKeyField,
    DateTimeField, ForeignKeyField
)

from burrito.models.issues_model import Issues
from burrito.models.user_model import Users
from burrito.models.action_types_model import ActionTypes

from burrito.utils.db_cursor_object import postgresql_cursor


class Actions(Model):
    action_id = PrimaryKeyField()
    issue_id = ForeignKeyField(
        Issues,
        to_field="issue_id",
        on_delete="NO ACTION"
    )
    user_id = ForeignKeyField(Users, to_field="user_id", on_delete="NO ACTION")
    action_type_id = ForeignKeyField(
        ActionTypes,
        to_field="action_type_id",
        on_delete="NO ACTION"
    )

    action_date = DateTimeField(default=datetime.datetime.now)
    body = TextField()

    class Meta:
        database = postgresql_cursor
