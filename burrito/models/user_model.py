from peewee import PostgresqlDatabase
from peewee import (
    Model, CharField, TextField, PrimaryKeyField,
    DateTimeField, ForeignKeyField, SmallIntegerField
)

from burrito.models.roles_model import Roles

pg_users_db = PostgresqlDatabase(
    "postgres",
    user="postgres", password="root",
    host="localhost", port=5432
)


class Users(Model):
    user_id = PrimaryKeyField()
    firstname = CharField(60)
    lastname = CharField(60)

    login = CharField(25)
    hashed_password = TextField()

    phone = CharField(15)
    email = CharField(255)

    registration_date = DateTimeField()

    role_id = ForeignKeyField(Roles, to_field="role_id", on_delete="NO ACTION")

    class Meta:
        database = pg_users_db
