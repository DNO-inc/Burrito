from peewee import (
    CharField, TextField, AutoField,
    DateTimeField, ForeignKeyField,
    IntegerField
)

from burrito.utils.date import get_datetime_now

from burrito.models.roles_model import Roles
from burrito.models.faculty_model import Faculties
from burrito.models.group_model import Groups
from burrito.models.basic_model import BurritoBasicModel


class Users(BurritoBasicModel):
    user_id = AutoField()
    cabinet_id = IntegerField(null=True, unique=True, default=None)

    firstname = CharField(60)
    lastname = CharField(60)

    login = CharField(40, unique=True)

    faculty = ForeignKeyField(
        Faculties,
        field="faculty_id",
        on_delete="NO ACTION"
    )

    group = ForeignKeyField(
        Groups,
        field="group_id",
        on_delete="SET NULL",
        null=True
    )

    password = TextField()

    email = CharField(255, null=False, unique=True)
    phone = CharField(15, null=True)

    registration_date = DateTimeField(default=get_datetime_now)

    role = ForeignKeyField(
        Roles,
        field="role_id",
        on_delete="NO ACTION"
    )

    class Meta:
        depends_on = [Roles, Groups, Faculties]
