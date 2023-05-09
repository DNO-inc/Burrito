import datetime

from peewee import (
    Model, CharField, TextField, PrimaryKeyField,
    DateTimeField, ForeignKeyField
)

from burrito.models.roles_model import Roles
from burrito.models.faculty_model import Faculties
from burrito.models.group_model import Groups

from burrito.utils.db_cursor_object import get_database_cursor


class Users(Model):
    user_id = PrimaryKeyField()

    firstname = CharField(60, null=True)
    lastname = CharField(60, null=True)

    login = CharField(25)

    faculty_id = ForeignKeyField(
        Faculties,
        to_field="faculty_id",
        on_delete="NO ACTION",
        null=True
    )
    group_id = ForeignKeyField(
        Groups,
        to_field="group_id",
        on_delete="NO ACTION",
        null=True
    )

    password = TextField()

    email = CharField(255, null=True)
    phone = CharField(15, null=True)

    registration_date = DateTimeField(default=datetime.datetime.now)

    role_id = ForeignKeyField(
        Roles,
        to_field="role_id",
        on_delete="NO ACTION",
        null=True
    )

    class Meta:
        database = get_database_cursor()
        depends_on = [Roles, Groups, Faculties]
