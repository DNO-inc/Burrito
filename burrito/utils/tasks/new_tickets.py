import datetime

from burrito.models.tickets_model import Tickets
from burrito.models.user_model import Users
from burrito.utils.email_util import load_email_template, publish_email
from burrito.utils.logger import get_logger
from burrito.utils.query_util import STATUS_NEW

MAX_UNCHANGED_DAYS = 2


def check_for_new_tickets():
    tickets_list: list[Tickets] = Tickets.select(Tickets.ticket_id, Tickets.subject, Tickets.created).where(
        Tickets.status == STATUS_NEW
    )
    admins_list = [
        item.user_id for item in Users.select(Users.user_id).where(
            Users.role.in_((9, 10))
        )
    ]
    tickets_info: list[dict] = []

    for ticket_item in tickets_list:
        ticket_created = datetime.datetime.strptime(str(ticket_item.created), "%Y-%m-%d %H:%M:%S")

        if (datetime.datetime.now() - ticket_created).days > MAX_UNCHANGED_DAYS:
            tickets_info.append(
                {
                    "ticket_id": ticket_item.ticket_id,
                    "subject": ticket_item.subject,
                    "created": ticket_item.created
                }
            )

    if tickets_info:
        publish_email(
            admins_list,
            "Тікети в статусі NEW вже кілька днів",
            load_email_template(
                "email/new_tickets.html",
                {
                    "days_count": MAX_UNCHANGED_DAYS,
                    "tickets_data": tickets_info
                }
            )
        )
        get_logger().info(f"Found {len(tickets_list)} tickets with status NEW")
