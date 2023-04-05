from burrito.utils.logger import get_logger
from burrito.utils.redis_utils import get_redis_cursor


async def send_test_email_via_redis(chanel_name: str, message: str) -> None:
    """_summary_

    Send test messages via redis pubsub system

    Args:
        chanel_name (str): redis chanel name
        message (str): message
    """

    await get_redis_cursor().publish(chanel_name, message)
    get_logger().warning("Email was sended via redis pubsub")
