from typing import Union
from datetime import datetime


def to_date(date_str: str = None, current_format: str = "%Y-%m-%d"):
    if date_str is None:
        return None
    if isinstance(date_str, datetime):
        return date_str

    return datetime.strptime(str(date_str), current_format)


def format_date(date_str: str = None, current_format: str = "%Y-%m-%d"):
    date = to_date(date_str, current_format)
    if date is None:
        return None
    return date.strftime("%Y-%m-%d")


def format_datetime(date_str: str = None, current_format: str = "%Y-%m-%d %H:%M:%S"):
    date = to_date(date_str, current_format)
    if date is None:
        return None
    return date.strftime("%Y-%m-%d %H:%M:%S")


def format_time(time_str: str, current_format: str = "%H:%M:%S", output_format: str = "%H:%M"):
    time = to_date(time_str, current_format)
    if time is None:
        return None
    return time.strftime(output_format)


def format_timestamp(timestamp: Union[str, int] = None):
    if timestamp is None:
        return None
    return datetime.utcfromtimestamp(int(timestamp)).strftime("%H:%M")
