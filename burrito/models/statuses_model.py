from peewee import PostgresqlDatabase
from peewee import Model, PrimaryKeyField, CharField

pg_statuses_db = PostgresqlDatabase(
    "ramee",
    user="postgres", password="root",
    host="localhost", port=5432
)


class Statuses(Model):
    status_id = PrimaryKeyField()
    name = CharField(10)

    class Meta:
        database = pg_statuses_db
