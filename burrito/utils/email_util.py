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
        super().__init__(host)

        self.login(login, password)

    def send_email(self, message: EmailMessage) -> None:
        self.send_message(message)


_BURRITO_EMAIL_LOGIN = get_config().BURRITO_EMAIL_LOGIN
_BURRITO_EMAIL: smtplib.SMTP_SSL = BurritoEmail(
    get_config().BURRITO_SMTP_SERVER,
    _BURRITO_EMAIL_LOGIN,
    get_config().BURRITO_EMAIL_PASSWORD
)


def send_email(to: int, subject: str, content: str) -> None:
    current_user: Users = get_user_by_id_or_none(to)

    if current_user is None:
        return

    if not current_user.email:
        return

    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = subject
    msg["From"] = _BURRITO_EMAIL_LOGIN
    msg["To"] = current_user.email

    try:
        _BURRITO_EMAIL.send_email(msg)
        get_logger().info(f"Email successfully sent to {to} ({current_user.email})")
    except Exception:
        get_logger().warning(f"Failed to send email to user {to} ({current_user.email})")


def publish_email(receivers: set[int] | list[int], subject: str, content: str) -> None:
    get_redis_connector().publish(
        "email",
        orjson.dumps(
            {
                "receivers": list(receivers),
                "subject": subject,
                "content": content
            }
        )
    )
