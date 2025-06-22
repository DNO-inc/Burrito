import datetime


def get_datetime_now() -> str:
    """
    Returns the current date and time in the current time zone.
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_timestamp_now() -> int:
    """
    This function is used to get timestamp of current time in system time zone.
    """
    return int(datetime.datetime.now().timestamp())
