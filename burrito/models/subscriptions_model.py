from peewee import Model, AutoField, ForeignKeyField

from burrito.models.user_model import Users
from burrito.models.tickets_model import Tickets

from burrito.utils.db_cursor_object import get_database_cursor


class Subscriptions(Model):
    ticket_id = ForeignKeyField(
        Tickets,
        field="ticket_id",
        on_delete="NO ACTION"
    )
    user_id = ForeignKeyField(Users, field="user_id", on_delete="NO ACTION")

    class Meta:
        database = get_database_cursor()
        depends_on = [Tickets, Users]
