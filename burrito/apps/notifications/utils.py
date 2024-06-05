import time
import orjson
from redis.client import PubSub

from burrito.utils.redis_utils import get_redis_connector
from burrito.utils.email_util import send_email
from burrito.utils.task_manager import get_task_manager
from burrito.utils.logger import get_logger


def email_loop():
    email_subscriber: PubSub = get_redis_connector().pubsub()
    email_subscriber.subscribe("email")

    get_logger().info("Email loop is started")
    while True:
        try:
            email_subscriber.ping()
        except Exception:
            get_logger().critical("Redis server is unavailable, sleep for 10 seconds")
            time.sleep(10)
            continue

        message = email_subscriber.get_message()

        if message:
            raw_data = message.get("data")

            if raw_data and isinstance(raw_data, (str, bytes)):
                get_logger().info(f"Found such data in the chanel: {raw_data}")
                try:
                    data = orjson.loads(raw_data)
                except UnboundLocalError as exc:
                    get_logger().warning(exc)

                get_task_manager().add_task(
                    send_email,
                    **data
                )

        else:
            get_logger().info("No messages")

        time.sleep(1)

    get_logger().critical("Email loop is closed unexpectedly")
