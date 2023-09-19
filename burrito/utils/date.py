import datetime

from burrito import CURRENT_TIME_ZONE


def get_datetime_now() -> str:
    return datetime.datetime.now(CURRENT_TIME_ZONE).strftime("%Y-%m-%d %H:%M:%S")


def get_timestamp_now() -> int:
    return int(datetime.datetime.now(CURRENT_TIME_ZONE).timestamp())
