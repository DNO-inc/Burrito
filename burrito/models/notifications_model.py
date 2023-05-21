from peewee import (
    Model, BooleanField, AutoField,
    ForeignKeyField, TextField
)

from burrito.models.tickets_model import Tickets
from burrito.models.user_model import Users

from burrito.utils.db_cursor_object import get_database_cursor


class Notifications(Model):
    notification_id = AutoField()

    ticket_id = ForeignKeyField(
        Tickets,
        field="ticket_id",
        on_delete="NO ACTION"
    )
    user_id = ForeignKeyField(Users, field="user_id", on_delete="NO ACTION")
    body = TextField()
    read = BooleanField(default=False)

    class Meta:
        database = get_database_cursor()
        depends_on = [Tickets, Users]
