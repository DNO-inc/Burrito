import orjson
import smtplib
from email.message import EmailMessage

from burrito.utils.config_reader import get_config
from burrito.utils.singleton_pattern import singleton
from burrito.utils.redis_utils import get_redis_connector
from burrito.utils.users_util import get_user_by_id_or_none
from burrito.utils.logger import get_logger

from burrito.models.user_model import Users


EMAIL_NOTIFICATION_TEMPLATE = """
Шановн(-ий/-а) студент(-ко),

Ми хочемо вас проінформувати, що були внесені важливі зміни до тікетів на платформі TreS. Нижче наведено деталізація цих змін:

{}

Дякуємо за увагу!
"""


@singleton
class BurritoEmail(smtplib.SMTP_SSL):
    def __init__(self, host: str, login: str, password: str):
        """
        Initialize the connection to SMTP server.

        Args:
            host: The host to connect to.
            login: The login to use.
            password: The password to use.
        """
        super().__init__(host)

        self.login(login, password)


def get_burrito_email() -> BurritoEmail:
    """
    Get BurritoEmail instance
    """
    return BurritoEmail(
        get_config().BURRITO_SMTP_SERVER,
        get_config().BURRITO_EMAIL_LOGIN,
        get_config().BURRITO_EMAIL_PASSWORD
    )


def send_email(receivers: list[int], subject: str, content: str) -> None:
    """
    Send email to receivers. This will try to resend email if sending fails.

    Args:
        receivers: List of receivers to send email to
        subject: Subject of the email to send
        content: Content of the email to send
    """
    receivers_email: list[str] = []

    for id_ in receivers:
        current_user: Users = get_user_by_id_or_none(id_)

        # if current_user is not exist
        if current_user is None:
            continue
        # skip user if email is empty
        if not current_user.email:
            continue

        receivers_email.append(current_user.email)

    if not receivers_email:
        return

    sender = get_config().BURRITO_EMAIL_LOGIN
    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = sender
    msg["Bcc"] = ", ".join(receivers_email)

    # try to resend email if sending is failed
    for i in range(3):
        try:
            get_burrito_email().send_message(msg)
            get_logger().info(f"Email successfully sent to {receivers_email}")
            break
        except Exception:
            get_logger().warning(f"Failed to send email to {receivers_email}", exc_info=True)
            get_logger().info("Try to re-login")


def publish_email(receivers: set[int] | list[int], subject: str, content: str) -> None:
    """
    Publish an email to Redis pubsub.

    Args:
        receivers: A list of receivers to send email
        subject: The subject of the email
        content: The content of the email
    """
    get_redis_connector().publish(
        "email",
        orjson.dumps(
            {
                "receivers": list(set(receivers)),
                "subject": subject,
                "content": content
            }
        )
    )
