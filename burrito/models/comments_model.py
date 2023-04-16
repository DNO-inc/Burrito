import datetime

from peewee import (
    Model, PrimaryKeyField, ForeignKeyField,
    DateTimeField, TextField
)

from burrito.models.user_model import Users
from burrito.models.tickets_model import Tickets

from burrito.utils.db_cursor_object import get_database_cursor


class Comments(Model):
    comment_id = PrimaryKeyField()
    ticket_id = ForeignKeyField(
        Tickets,
        to_field="ticket_id",
        on_delete="NO ACTION"
    )
    user_id = ForeignKeyField(Users, to_field="user_id", on_delete="NO ACTION")

    comment_date = DateTimeField(default=datetime.datetime.now)
    body = TextField()

    class Meta:
        database = get_database_cursor()