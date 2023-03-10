from peewee import PostgresqlDatabase
from peewee import Model, PrimaryKeyField, CharField

pg_roles_db = PostgresqlDatabase(
    "ramee",
    user="postgres", password="root",
    host="localhost", port=5432
)


class Roles(Model):
    role_id = PrimaryKeyField()
    name = CharField(10)

    class Meta:
        database = pg_roles_db
