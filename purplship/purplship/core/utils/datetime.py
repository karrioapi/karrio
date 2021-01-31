from typing import Union
from datetime import datetime


class DATEFORMAT:
    @staticmethod
    def date(date_str: str = None, current_format: str = "%Y-%m-%d"):
        if date_str is None:
            return None
        if isinstance(date_str, datetime):
            return date_str

        return datetime.strptime(str(date_str), current_format)

    @staticmethod
    def fdate(date_str: str = None, current_format: str = "%Y-%m-%d"):
        date = DATEFORMAT.date(date_str, current_format)
        if date is None:
            return None
        return date.strftime("%Y-%m-%d")

    @staticmethod
    def fdatetime(
        date_str: str = None, current_format: str = "%Y-%m-%d %H:%M:%S", output_format: str = "%Y-%m-%d %H:%M:%S"
    ):
        date = DATEFORMAT.date(date_str, current_format)
        if date is None:
            return None
        return date.strftime(output_format)

    @staticmethod
    def ftime(
        time_str: str, current_format: str = "%H:%M:%S", output_format: str = "%H:%M"
    ):
        time = DATEFORMAT.date(time_str, current_format)
        if time is None:
            return None
        return time.strftime(output_format)

    @staticmethod
    def ftimestamp(timestamp: Union[str, int] = None):
        if timestamp is None:
            return None
        return datetime.utcfromtimestamp(int(timestamp)).strftime("%H:%M")
