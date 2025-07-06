import time
from dataclasses import dataclass

import orjson
from redis.client import PubSub

from burrito.utils.email_util import JinjaEmailTemplateData, send_email
from burrito.utils.logger import get_logger
from burrito.utils.redis_utils import get_redis_connector
from burrito.utils.task_manager import get_task_manager


@dataclass
class PublishedEmailMeta:
    receivers: set[int] | list[int]
    subject: str
    template_name: str
    template_variables: dict


EMAIL_LOOP_DELAY = 1


def email_loop():
    email_subscriber: PubSub = get_redis_connector().pubsub()
    email_subscriber.subscribe("email")

    logger = get_logger()
    logger.info("Email loop is started")

    while True:
        time.sleep(EMAIL_LOOP_DELAY)

        try:
            email_subscriber.ping()
        except Exception:
            logger.critical("Redis server unavailable: %s. Sleeping 10 seconds...")
            time.sleep(10)
            continue

        message = email_subscriber.get_message()
        if not message:
            continue

        raw_data = message.get("data")
        if not raw_data or not isinstance(raw_data, (str, bytes)):
            continue

        try:
            data = orjson.loads(raw_data)
        except Exception as exc:
            logger.warning("Failed to parse message data: %s", exc)
            continue

        try:
            email_meta = PublishedEmailMeta(**data)
        except TypeError as exc:
            logger.error("Invalid data for PublishedEmailMeta: %s", exc)
            logger.info(data)
            continue

        task_args = {
            "receivers": email_meta.receivers,
            "subject": email_meta.subject,
            "jinja_template_metadata": JinjaEmailTemplateData(
                template_name=email_meta.template_name,
                template_variables=email_meta.template_variables
            )
        }

        get_task_manager().add_task(send_email, **task_args)
        logger.info("New task started...")
