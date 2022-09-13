from typing import Union, List
from datetime import datetime


class DATEFORMAT:
    @staticmethod
    def date(
        date_value: Union[str, int, datetime] = None,
        current_format: str = "%Y-%m-%d",
        try_formats: List[str] = None,
    ) -> datetime:
        if date_value is None:
            return None

        if isinstance(date_value, str) and not any(date_value.split(" ")):
            return None

        if isinstance(date_value, int):
            return datetime.fromtimestamp(date_value)

        if isinstance(date_value, datetime):
            return date_value

        if any(try_formats or []):
            for format in try_formats:
                try:
                    return datetime.strptime(date_value, format)
                except ValueError:
                    pass

        return datetime.strptime(str(date_value), current_format)

    @staticmethod
    def fdate(
        date_str: Union[str, int, datetime] = None,
        current_format: str = "%Y-%m-%d",
        try_formats: List[str] = None,
    ):
        date = DATEFORMAT.date(
            date_str, current_format=current_format, try_formats=try_formats
        )
        if date is None:
            return None
        return date.strftime("%Y-%m-%d")

    @staticmethod
    def fdatetime(
        date_str: Union[str, int, datetime] = None,
        current_format: str = "%Y-%m-%d %H:%M:%S",
        output_format: str = "%Y-%m-%d %H:%M:%S",
        try_formats: List[str] = None,
    ):
        date = DATEFORMAT.date(
            date_str, current_format=current_format, try_formats=try_formats
        )
        if date is None:
            return None
        return date.strftime(output_format)

    @staticmethod
    def ftime(
        time_str: str,
        current_format: str = "%H:%M:%S",
        output_format: str = "%H:%M",
        try_formats: List[str] = None,
    ):
        time = DATEFORMAT.date(
            time_str, current_format=current_format, try_formats=try_formats
        )
        if time is None:
            return None
        return time.strftime(output_format)

    @staticmethod
    def ftimestamp(timestamp: Union[str, int] = None):
        if timestamp is None:
            return None
        return datetime.utcfromtimestamp(int(timestamp)).strftime("%H:%M")
