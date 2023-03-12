import datetime

from peewee import (
    Model, CharField, TextField, PrimaryKeyField,
    DateTimeField, ForeignKeyField
)

from burrito.models.roles_model import Roles

from burrito.utils.db_cursor_object import postgresql_cursor


class Users(Model):
    user_id = PrimaryKeyField()
    firstname = CharField(60, null=True)
    lastname = CharField(60, null=True)

    login = CharField(25)
    hashed_password = TextField()

    phone = CharField(15, null=True)
    email = CharField(255, null=True)

    registration_date = DateTimeField(default=datetime.datetime.now)

    role_id = ForeignKeyField(
        Roles,
        to_field="role_id",
        on_delete="NO ACTION",
        null=True
    )

    class Meta:
        database = postgresql_cursor
