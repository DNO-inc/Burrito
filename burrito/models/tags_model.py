from peewee import PostgresqlDatabase
from peewee import Model, PrimaryKeyField, CharField

pg_tags_db = PostgresqlDatabase(
    "ramee",
    user="postgres", password="root",
    host="localhost", port=5432
)


class Tags(Model):
    tag_id = PrimaryKeyField()
    name = CharField(25)

    class Meta:
        database = pg_tags_db
