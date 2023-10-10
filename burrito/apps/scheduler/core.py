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

    # email services
    (get_config().BURRITO_SMTP_SERVER, 25),
    (get_config().BURRITO_SMTP_SERVER, 110),
    (get_config().BURRITO_SMTP_SERVER, 143),
    (get_config().BURRITO_SMTP_SERVER, 465),
    (get_config().BURRITO_SMTP_SERVER, 993),
    (get_config().BURRITO_SMTP_SERVER, 995)
)


def start_scheduler():
    get_logger().info("scheduler is started")

    schedule.every().day.at("00:30").do(preprocessor_task)

    for i in __HOST_TO_PING:
        schedule.every().hours.do(burrito_ping, *i)

    while True:
        schedule.run_pending()
        time.sleep(5)
