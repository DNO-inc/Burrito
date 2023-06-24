import datetime

from peewee import (
    AutoField, ForeignKeyField,
    DateTimeField, TextField
)

from burrito.models.user_model import Users
from burrito.models.tickets_model import Tickets
from burrito.models.basic_model import BurritoBasicModel


# TODO: add reply_to field to this model
class Comments(BurritoBasicModel):
    comment_id = AutoField()

    ticket = ForeignKeyField(
        Tickets,
        field="ticket_id",
        on_delete="NO ACTION"
    )

    author = ForeignKeyField(
        Users,
        field="user_id",
        on_delete="NO ACTION"
    )

    comment_date = DateTimeField(default=datetime.datetime.now)

    body = TextField()

    class Meta:
        depends_on = [Tickets, Users]
