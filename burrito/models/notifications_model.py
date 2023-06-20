from peewee import (
    BooleanField, AutoField,
    ForeignKeyField, TextField
)

from burrito.models.tickets_model import Tickets
from burrito.models.user_model import Users
from burrito.models.basic_model import BurritoBasicModel


class Notifications(BurritoBasicModel):
    notification_id = AutoField()

    ticket_id = ForeignKeyField(
        Tickets,
        field="ticket_id",
        on_delete="NO ACTION"
    )

    user_id = ForeignKeyField(
        Users,
        field="user_id",
        on_delete="NO ACTION"
    )

    body = TextField()
    read = BooleanField(default=False)

    class Meta:
        depends_on = [Tickets, Users]
