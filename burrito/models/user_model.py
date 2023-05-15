import datetime

from peewee import (
    Model, CharField, TextField, AutoField,
    DateTimeField, ForeignKeyField
)

from burrito.models.roles_model import Roles
from burrito.models.faculty_model import Faculties
from burrito.models.group_model import Groups

from burrito.utils.db_cursor_object import get_database_cursor


class Users(Model):
    user_id = AutoField()

    firstname = CharField(60, null=True)
    lastname = CharField(60, null=True)

    login = CharField(25)

    faculty = ForeignKeyField(
        Faculties,
        field="faculty_id",
        on_delete="NO ACTION",
        null=True
    )
    group_id = ForeignKeyField(
        Groups,
        field="group_id",
        on_delete="NO ACTION",
        null=True
    )

    password = TextField()

    email = CharField(255, null=True)
    phone = CharField(15, null=True)

    registration_date = DateTimeField(default=datetime.datetime.now)

    role_id = ForeignKeyField(
        Roles,
        field="role_id",
        on_delete="NO ACTION",
        null=True
    )

    class Meta:
        database = get_database_cursor()
        depends_on = [Roles, Groups, Faculties]
