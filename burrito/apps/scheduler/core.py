import schedule
import time

from .preprocessor.core import preprocessor_task


def start_scheduler():
    schedule.every().day.at("00:30").do(preprocessor_task)

    while True:
        schedule.run_pending()
        time.sleep(1)
