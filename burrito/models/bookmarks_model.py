from peewee import ForeignKeyField, DateTimeField, CompositeKey

from burrito.utils.date import get_datetime_now
from burrito.models.user_model import Users
from burrito.models.tickets_model import Tickets
from burrito.models.basic_model import BurritoBasicModel


class Bookmarks(BurritoBasicModel):
    # TODO: replace user_id with user and ticket_id with ticket

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
    created = DateTimeField(default=get_datetime_now)

    class Meta:
        depends_on = [Users, Tickets]
        primary_key = CompositeKey('user_id', 'ticket_id')
