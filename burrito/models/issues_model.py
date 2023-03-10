from peewee import PostgresqlDatabase
from peewee import Model, PrimaryKeyField, IntegerField, TextField, DateTimeField, SmallIntegerField, CharField

pg_issues_db = PostgresqlDatabase(
    "ramee",
    user="postgres", password="root",
    host="localhost", port=5432
)


class Issues(Model):
    issue_id = PrimaryKeyField()
    issuer_id = IntegerField()
    assignee_id = IntegerField()

    subject = TextField()
    body = TextField()
    priority = SmallIntegerField()

    status = CharField(10)

    creation_date = DateTimeField()

    class Meta:
        database = pg_issues_db
