from peewee import ForeignKeyField, DateTimeField, CompositeKey

from burrito.utils.date import get_datetime_now
from burrito.models.user_model import Users
from burrito.models.tickets_model import Tickets
from burrito.models.basic_model import BurritoBasicModel


class Bookmarks(BurritoBasicModel):
    user = ForeignKeyField(
        Users,
        field="user_id",
        on_delete="NO ACTION"
    )

    ticket = ForeignKeyField(
        Tickets,
        field="ticket_id",
        on_delete="CASCADE"
    )
    created = DateTimeField(default=get_datetime_now)

    class Meta:
        depends_on = [Users, Tickets]
        primary_key = CompositeKey('user', 'ticket')
