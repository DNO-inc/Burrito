import datetime

from peewee import (
    CharField, AutoField,
    DateTimeField, ForeignKeyField
)

from burrito.models.tickets_model import Tickets
from burrito.models.user_model import Users
from burrito.models.basic_model import BurritoBasicModel


class Actions(BurritoBasicModel):
    action_id = AutoField()
    ticket = ForeignKeyField(
        Tickets,
        field="ticket_id",
        on_delete="NO ACTION"
    )

    user = ForeignKeyField(
        Users,
        field="user_id",
        on_delete="NO ACTION"
    )

    creation_date = DateTimeField(default=datetime.datetime.now)

    field_name = CharField(max_length=255)
    old_value = CharField(max_length=255)
    new_value = CharField(max_length=255)

    class Meta:
        depends_on = [Tickets, Users]
