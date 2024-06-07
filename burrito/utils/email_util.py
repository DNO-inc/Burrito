import orjson
import smtplib
from email.message import EmailMessage
import traceback

from burrito.utils.config_reader import get_config
from burrito.utils.redis_utils import get_redis_connector
from burrito.utils.users_util import get_user_by_id_or_none
from burrito.utils.logger import get_logger

from burrito.models.user_model import Users


class BurritoEmail(smtplib.SMTP_SSL):
    def __init__(self, host: str):
        """
        Initialize the connection to SMTP server.

        Args:
            host: The host to connect to.
            login: The login to use.
            password: The password to use.
        """
        super().__init__(host)


def get_burrito_email() -> BurritoEmail:
    """
    Get BurritoEmail instance
    """
    return BurritoEmail(get_config().BURRITO_SMTP_SERVER)


def send_email(receivers: list[int], subject: str, content: str) -> None:
    """
    Send email to receivers. This will try to resend email if sending fails.

    Args:
        receivers: List of receivers to send email to
        subject: Subject of the email to send
        content: Content of the email to send
    """
    receivers_email: list[str] = []

    get_logger().info("Preparing for sending email")
    for id_ in receivers:
        current_user: Users = get_user_by_id_or_none(id_)

        # if current_user is not exist
        if current_user is None:
            get_logger().warning(f"Unexistent user ID ({id_})")
            continue
        # skip user if email is empty
        if not current_user.email:
            get_logger().warning(f"Empty email for user ({current_user.user_id})")
            continue

        receivers_email.append(current_user.email)

    if not receivers_email:
        get_logger().warning("No email recipients provided")
        get_logger().info(f"Receivers IDs list: {receivers}")
        return

    sender = get_config().BURRITO_EMAIL_LOGIN
    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = sender
    msg["Bcc"] = ", ".join(receivers_email)

    try:
        get_logger().info("Creating SMTP client...")

        with get_burrito_email() as smtp_client:
            get_logger().info("Connecting to SMTP server...")
            smtp_client.connect(get_config().BURRITO_SMTP_SERVER)
            smtp_client.noop()

            get_logger().info("Trying to login...")
            smtp_client.login(
                get_config().BURRITO_EMAIL_LOGIN,
                get_config().BURRITO_EMAIL_PASSWORD
            )

            get_logger().info("Sending message...")
            smtp_client.send_message(msg)

        get_logger().info(f"Email successfully sent to {receivers_email}")

    except Exception:
        traceback.print_exc()
        get_logger().info(
            f"""
                SMTP host: {get_config().BURRITO_SMTP_SERVER}
                Login: {get_config().BURRITO_EMAIL_LOGIN}

            """
        )
        get_logger().critical(f"Failed to send email to {receivers_email}")


# TODO: delete this function after public tests
def tmp_send_email(to: str, subject: str, content: str) -> None:
    sender = get_config().BURRITO_EMAIL_LOGIN
    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = sender
    msg["Bcc"] = to

    try:
        with get_burrito_email() as smtp_client:
            smtp_client.connect(get_config().BURRITO_SMTP_SERVER)
            smtp_client.noop()
            smtp_client.login(
                get_config().BURRITO_EMAIL_LOGIN,
                get_config().BURRITO_EMAIL_PASSWORD
            )
            smtp_client.send_message(msg)

        get_logger().info(f"Email successfully sent to {to}")

    except Exception as exc:
        get_logger().warning(f"{exc} Failed to send email to {to}")


def publish_email(receivers: set[int] | list[int], subject: str, content: str) -> None:
    """
    Publish an email to Redis pubsub.

    Args:
        receivers: A list of receivers to send email
        subject: The subject of the email
        content: The content of the email
    """
    clear_receivers = list(set(receivers))
    get_redis_connector().publish(
        "email",
        orjson.dumps(
            {
                "receivers": clear_receivers,
                "subject": subject,
                "content": content
            }
        )
    )
    get_logger().info(
        f"""
            New email was published to chanel (
                "receivers": {clear_receivers},
                "subject": {subject},
            )

        """
    )
