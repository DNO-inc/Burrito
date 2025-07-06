import datetime
from collections import defaultdict

from burrito.models.tickets_model import Tickets
from burrito.utils.email_util import publish_email
from burrito.utils.query_util import STATUS_ACCEPTED

MAX_UNCHANGED_DAYS = 2


def check_for_accepted_tickets():
    tickets_list: list[Tickets] = Tickets.select(Tickets.ticket_id, Tickets.subject, Tickets.created, Tickets.assignee).where(
        Tickets.status == STATUS_ACCEPTED
    )

    email_dict = defaultdict(list)

    for ticket_item in tickets_list:
        ticket_created = datetime.datetime.strptime(str(ticket_item.created), "%Y-%m-%d %H:%M:%S")

        if (datetime.datetime.now() - ticket_created).days > MAX_UNCHANGED_DAYS:
            email_dict[ticket_item.assignee.user_id].append(
                {
                    "ticket_id": ticket_item.ticket_id,
                    "subject": ticket_item.subject,
                    "created": ticket_item.created
                }
            )

    for assignee, desc in email_dict.items():
        publish_email(
            [assignee],
            "Тікети в статусі ACCEPTED вже кілька днів",
            "accepted_tickets",
            {
                "days_count": MAX_UNCHANGED_DAYS,
                "tickets_data": desc
            }
        )
