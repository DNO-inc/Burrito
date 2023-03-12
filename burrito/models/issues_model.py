from peewee import (
    Model, PrimaryKeyField,
    IntegerField, TextField,
    DateTimeField, SmallIntegerField,
    CharField, ForeignKeyField
)

from burrito.models.tags_model import Tags
from burrito.models.statuses_model import Statuses

from burrito.utils.db_cursor_object import postgresql_cursor


class Issues(Model):
    issue_id = PrimaryKeyField()
    issuer_id = IntegerField()
    assignee_id = IntegerField()

    subject = CharField(255)
    body = TextField()
    priority = SmallIntegerField()

    creation_date = DateTimeField()

    tag_id = ForeignKeyField(Tags, to_field="tag_id", on_delete="NO ACTION")
    status_id = ForeignKeyField(
        Statuses,
        to_field="status_id",
        on_delete="NO ACTION"
    )

    class Meta:
        database = postgresql_cursor
