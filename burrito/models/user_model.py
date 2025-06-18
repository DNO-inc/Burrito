from peewee import AutoField, CharField, DateTimeField, ForeignKeyField, TextField

from burrito.models.basic_model import BurritoBasicModel
from burrito.models.division_model import Divisions
from burrito.models.group_model import Groups
from burrito.models.roles_model import Roles
from burrito.utils.date import get_datetime_now


class Users(BurritoBasicModel):
    user_id = AutoField()
    cabinet_id = CharField(
        max_length=36,
        null=True,
        unique=True,
        default=None,
        index=True
    )

    firstname = CharField(60)
    lastname = CharField(60)

    login = CharField(50, unique=True)

    division = ForeignKeyField(
        Divisions,
        field="division_id",
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
        depends_on = [Roles, Groups, Divisions]
