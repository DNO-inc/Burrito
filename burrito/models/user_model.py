import datetime

from peewee import PostgresqlDatabase
from peewee import (
    Model, CharField, TextField, PrimaryKeyField,
    DateTimeField, ForeignKeyField, SmallIntegerField
)

from burrito.models.roles_model import Roles

pg_users_db = PostgresqlDatabase(
    "ramee",
    user="postgres", password="root",
    host="localhost", port=5432
)


class Users(Model):
    user_id = PrimaryKeyField()
    firstname = CharField(60, null=True)
    lastname = CharField(60, null=True)

    login = CharField(25)
    hashed_password = TextField()

    phone = CharField(15, null=True)
    email = CharField(255, null=True)

    registration_date = DateTimeField(default=datetime.datetime.now)

    role_id = ForeignKeyField(Roles, to_field="role_id", on_delete="NO ACTION", null=True)


    class Meta:
        database = pg_users_db
