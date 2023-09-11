import schedule
import time

from burrito.utils.config_reader import get_config
from .preprocessor.core import preprocessor_task
from .ping.pingger import burrito_ping


CURRENT_TZ = "Europe/Kyiv"


def start_scheduler():
    schedule.every().day.at("00:30", CURRENT_TZ).do(preprocessor_task)

    schedule.every().hours.do(burrito_ping, host=get_config().BURRITO_DB_HOST, port=get_config().BURRITO_DB_PORT)
    schedule.every().hours.do(burrito_ping, host=get_config().BURRITO_REDIS_HOST, port=get_config().BURRITO_REDIS_PORT)
    schedule.every().hours.do(burrito_ping, host=get_config().BURRITO_MONGO_HOST, port=get_config().BURRITO_MONGO_PORT)
    schedule.every().hours.do(burrito_ping, host="iis.sumdu.edu.ua", port=80)

    while True:
        schedule.run_pending()
        time.sleep(1)
