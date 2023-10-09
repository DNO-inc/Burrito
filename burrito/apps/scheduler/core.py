import schedule
import time

from burrito.utils.config_reader import get_config
from burrito.utils.logger import get_logger
from burrito.utils.tasks.preprocessor import preprocessor_task
from burrito.utils.tasks.ping import burrito_ping


__HOST_TO_PING = (
    (get_config().BURRITO_DB_HOST, get_config().BURRITO_DB_PORT),
    (get_config().BURRITO_REDIS_HOST, get_config().BURRITO_REDIS_PORT),
    (get_config().BURRITO_MONGO_HOST, get_config().BURRITO_MONGO_PORT),
    ("iis.sumdu.edu.ua", 80),
)


def start_scheduler():
    get_logger().info("scheduler is started")

    schedule.every().day.at("00:30").do(preprocessor_task)

    for i in __HOST_TO_PING:
        schedule.every().hours.do(burrito_ping, *i)

    while True:
        schedule.run_pending()
        time.sleep(5)
