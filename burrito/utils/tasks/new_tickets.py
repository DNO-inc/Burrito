import datetime

from burrito.utils.email_util import publish_email
from burrito.utils.email_templates import TEMPLATE__EMAIL_NOTIFICATION_FOR_ADMIN
from burrito.utils.query_util import STATUS_NEW
from burrito.utils.logger import get_logger

from burrito.models.tickets_model import Tickets
from burrito.models.user_model import Users


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
    tickets_info: list[str] = []

    for ticket_item in tickets_list:
        ticket_created = datetime.datetime.strptime(str(ticket_item.created), "%Y-%m-%d %H:%M:%S")

        if (datetime.datetime.now() - ticket_created).days > MAX_UNCHANGED_DAYS:
            tickets_info.append(
                f"""
                #{ticket_item.ticket_id} "{ticket_item.subject}":
                    Дата створення: {ticket_item.created}
                """
            )

    if tickets_info:
        publish_email(
            admins_list,
            TEMPLATE__EMAIL_NOTIFICATION_FOR_ADMIN["subject"].format(days_count=MAX_UNCHANGED_DAYS),
            TEMPLATE__EMAIL_NOTIFICATION_FOR_ADMIN["content"].format(
                days_count=MAX_UNCHANGED_DAYS,
                data="".join(tickets_info)
            )
        )
        get_logger().info(f"Found {len(tickets_list)} tickets with status NEW")
