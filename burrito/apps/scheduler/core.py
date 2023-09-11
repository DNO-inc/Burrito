import schedule
import time

from .preprocessor.core import preprocessor_task


CURRENT_TZ = "Europe/Kyiv"


def start_scheduler():
    schedule.every().day.at("00:30", CURRENT_TZ).do(preprocessor_task)

    while True:
        schedule.run_pending()
        time.sleep(1)
