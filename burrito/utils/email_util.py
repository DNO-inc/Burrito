import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import jinja2
import orjson

from burrito.models.user_model import Users
from burrito.utils.config_reader import get_config
from burrito.utils.logger import get_logger
from burrito.utils.redis_utils import get_redis_connector
from burrito.utils.users_util import get_user_by_id_or_none

_jinja2_env = jinja2.Environment(
    loader=jinja2.PackageLoader("burrito", "templates"),
    autoescape=jinja2.select_autoescape()
)


class JinjaEmailTemplateData:
    def __init__(self, template_name: str, template_variables: dict, **kwargs) -> None:
        self.template_name = template_name
        self.template_variables = template_variables

    @property
    def html_template(self) -> str:
        return f"email/html/{self.template_name}.html"

    @property
    def text_template(self) -> str:
        return f"email/text/{self.template_name}.txt"

    def load_template(self, html: bool = True):
        template = _jinja2_env.get_template(
            self.html_template if html else self.text_template
        )
        return template.render(self.template_variables)


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


def _send_email(email_message: MIMEMultipart):
    try:
        get_logger().info("Creating SMTP client...")

        with get_burrito_email() as smtp_client:
            get_logger().info("Trying to login...")
            smtp_client.login(
                get_config().BURRITO_EMAIL_LOGIN,
                get_config().BURRITO_EMAIL_PASSWORD
            )

            get_logger().info("Sending message...")
            smtp_client.send_message(email_message)

        get_logger().info(f"Email successfully sent to [{email_message['Bcc']}]")

    except Exception:
        traceback.print_exc()
        get_logger().info(
            f"""
                SMTP host: {get_config().BURRITO_SMTP_SERVER}
                Login: {get_config().BURRITO_EMAIL_LOGIN}

            """
        )
        get_logger().critical(f"Failed to send email to {email_message['Bcc']}")


def _create_email_message(
    subject: str,
    sender: str,
    receivers: str,
    jinja_template_metadata: JinjaEmailTemplateData
) -> MIMEMultipart:
    msg = MIMEMultipart('alternative')
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = sender
    msg["Bcc"] = receivers
    msg.attach(MIMEText(jinja_template_metadata.load_template(html=False), 'plain'))
    msg.attach(MIMEText(jinja_template_metadata.load_template(html=True), 'html'))
    return msg


def send_email(
    receivers: list[int],
    subject: str,
    jinja_template_metadata: JinjaEmailTemplateData
) -> None:
    """
    Send email to receivers. This will try to resend email if sending fails.

    Args:
        receivers: List of receivers to send email to
        subject: Subject of the email to send
        template_name: The template name of the email to send
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

    msg = _create_email_message(
        subject,
        get_config().BURRITO_EMAIL_LOGIN,
        ", ".join(receivers_email),
        jinja_template_metadata
    )
    _send_email(msg)


def send_registration_email(
    to: str,
    subject: str,
    template_name: str,
    template_variables: dict
) -> None:
    msg = _create_email_message(
        subject,
        get_config().BURRITO_EMAIL_LOGIN,
        to,
        JinjaEmailTemplateData(
            template_name=template_name,
            template_variables=template_variables
        )
    )
    _send_email(msg)


def publish_email(
    receivers: set[int] | list[int],
    subject: str,
    template_name: str,
    template_variables: dict
) -> None:
    """
    Publish an email to Redis pubsub.

    Args:
        receivers: A list of receivers to send email
        subject: The subject of the email
        template_name: Short name of the jinja template for email
        template_variables: Parameters for the jinja template
    """
    clear_receivers = list(set(receivers))
    get_redis_connector().publish(
        "email",
        orjson.dumps(
            {
                "receivers": clear_receivers,
                "subject": subject,
                "template_name": template_name,
                "template_variables": template_variables
            }
        )
    )
    get_logger().info(
        f"""
            New email was published to chanel (
                "receivers": {clear_receivers},
                "subject": {subject},
                "template_name": {template_name}
            )

        """
    )
