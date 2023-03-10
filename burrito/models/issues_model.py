from peewee import PostgresqlDatabase
from peewee import (
    Model, PrimaryKeyField,
    IntegerField, TextField,
    DateTimeField, SmallIntegerField,
    CharField, ForeignKeyField
)

from burrito.models.tags_model import Tags
from burrito.models.statuses_model import Statuses

pg_issues_db = PostgresqlDatabase(
    "ramee",
    user="postgres", password="root",
    host="localhost", port=5432
)


class Issues(Model):
    issue_id = PrimaryKeyField()
    issuer_id = IntegerField()
    assignee_id = IntegerField()

    subject = CharField(255)
    body = TextField()
    priority = SmallIntegerField()

    creation_date = DateTimeField()

    tag_id = ForeignKeyField(Tags, to_field="tag_id", on_delete="NO ACTION")
    status_id = ForeignKeyField(Statuses, to_field="status_id", on_delete="NO ACTION")

    class Meta:
        database = pg_issues_db
