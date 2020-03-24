from typing import Union
from datetime import datetime


def format_date(date_str: str = None, current_format: str = '%Y-%m-%d'):
    if date_str is None:
        return None
    return datetime.strptime(str(date_str), current_format).strftime('%Y-%m-%d')


def format_datetime(date_str: str = None, current_format: str = '%Y-%m-%d'):
    if date_str is None:
        return None
    return datetime.strptime(str(date_str), current_format).strftime('%Y-%m-%d %H:%M:%S')


def format_time(time_str: str, current_format: str = '%H:%M:%S'):
    if time_str is None:
        return None
    return datetime.strptime(str(time_str), current_format).strftime('%H:%M')


def format_timestamp(timestamp: Union[str, int] = None):
    if timestamp is None:
        return None
    return datetime.utcfromtimestamp(int(timestamp)).strftime('%H:%M')
