import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from burrito.models.tickets_model import Tickets
from burrito.models.user_model import Users
from burrito.utils.email_templates import (
    TEMPLATE__NEW_TICKETS_EMAIL_NOTIFICATION_FOR_ADMIN,
)
from burrito.utils.email_util import publish_email
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
            TEMPLATE__NEW_TICKETS_EMAIL_NOTIFICATION_FOR_ADMIN["subject"].format(days_count=MAX_UNCHANGED_DAYS),
            TEMPLATE__NEW_TICKETS_EMAIL_NOTIFICATION_FOR_ADMIN["content"].format(
                days_count=MAX_UNCHANGED_DAYS,
                data="".join(tickets_info)
            )
        )
        get_logger().info(f"Found {len(tickets_list)} tickets with status NEW")


with DAG(
    dag_id="new_tickets_dag",
    description="Check if there is tickets with NEW status and send email if any",
    start_date=datetime.datetime.now() - datetime.timedelta(days=1),
    schedule_interval=datetime.timedelta(hours=3),
    catchup=False,
    is_paused_upon_creation=False
) as dag:
    PythonOperator(
        task_id="check_for_new_tickets",
        python_callable=check_for_new_tickets
    )
