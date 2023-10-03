import datetime

from burrito import CURRENT_TIME_ZONE


def get_datetime_now() -> str:
    """
    Returns the current date and time in the current time zone.
    """
    return datetime.datetime.now(CURRENT_TIME_ZONE).strftime("%Y-%m-%d %H:%M:%S")


def get_timestamp_now() -> int:
    """
    This function is used to get timestamp of current time in system time zone.
    """
    return int(datetime.datetime.now(CURRENT_TIME_ZONE).timestamp())
