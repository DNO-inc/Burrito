from peewee import ForeignKeyField, CompositeKey

from burrito.models.user_model import Users
from burrito.models.tickets_model import Tickets
from burrito.models.basic_model import BurritoBasicModel


class Subscriptions(BurritoBasicModel):
    user_id = ForeignKeyField(
        Users,
        field="user_id",
        on_delete="NO ACTION"
    )

    ticket_id = ForeignKeyField(
        Tickets,
        field="ticket_id",
        on_delete="CASCADE"
    )

    class Meta:
        depends_on = [Tickets, Users]
        primary_key = CompositeKey('user_id', 'ticket_id')
