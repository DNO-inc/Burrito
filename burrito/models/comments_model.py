import datetime

from peewee import (
    Model, AutoField, ForeignKeyField,
    DateTimeField, TextField, IntegerField
)

from burrito.models.user_model import Users
from burrito.models.tickets_model import Tickets

from burrito.utils.db_cursor_object import get_database_cursor


class Comments(Model):
    comment_id = AutoField()

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

    comment_date = DateTimeField(default=datetime.datetime.now)

    upvotes = IntegerField()

    body = TextField()

    class Meta:
        database = get_database_cursor()
        depends_on = [Tickets, Users]
