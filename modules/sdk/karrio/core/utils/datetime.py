import typing
from datetime import datetime, timedelta, timezone


class DATEFORMAT:
    @staticmethod
    def date(
        date_value: typing.Union[str, int, datetime] = None,
        current_format: str = "%Y-%m-%d",
        try_formats: typing.List[str] = None,
    ) -> typing.Optional[datetime]:
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
    def next_business_datetime(
        date_value: typing.Union[str, datetime] = None,
        current_format: str = "%Y-%m-%d %H:%M:%S",
        try_formats: typing.List[str] = None,
        start_hour: int = 10,
        end_hour: int = 17,
    ) -> typing.Optional[datetime]:
        date = DATEFORMAT.date(
            date_value, current_format=current_format, try_formats=try_formats
        )
        if date is None:
            return None

        # Define business hours
        _start_hour = start_hour
        _end_hour = end_hour

        # If date has no time component, set it to current time
        if date.hour == 0 and date.minute == 0 and date.second == 0:
            now = datetime.now()
            date = date.replace(hour=now.hour, minute=now.minute, second=now.second)

        # If the given datetime is within business hours, return it
        if DATEFORMAT.is_business_hour(date):
            return date

        # If it's outside business hours, calculate the next business datetime
        if date.weekday() >= 5:  # If it's Saturday or Sunday
            # Move to the next Monday
            days_to_add = 7 - date.weekday()
            next_business_day = date + timedelta(days=days_to_add)
            return next_business_day.replace(
                hour=_start_hour, minute=0, second=0, microsecond=0
            )
        elif date.hour >= _end_hour:  # If it's after business hours
            # Move to the next business day
            next_business_day = date + timedelta(days=1)
            if next_business_day.weekday() >= 5:  # If it's Saturday or Sunday
                days_to_add = 7 - next_business_day.weekday()
                next_business_day += timedelta(days=days_to_add)
            return next_business_day.replace(
                hour=_start_hour, minute=0, second=0, microsecond=0
            )
        else:  # If it's before business hours
            return date.replace(hour=_start_hour, minute=0, second=0, microsecond=0)

    @staticmethod
    def fdate(
        date_str: typing.Union[str, int, datetime] = None,
        current_format: str = "%Y-%m-%d",
        try_formats: typing.List[str] = None,
    ):
        date = DATEFORMAT.date(
            date_str, current_format=current_format, try_formats=try_formats
        )
        if date is None:
            return None
        return date.strftime("%Y-%m-%d")

    @staticmethod
    def fdatetime(
        date_str: typing.Union[str, int, datetime] = None,
        current_format: str = "%Y-%m-%d %H:%M:%S",
        output_format: str = "%Y-%m-%d %H:%M:%S",
        try_formats: typing.List[str] = None,
    ):
        date = DATEFORMAT.date(
            date_str,
            current_format=current_format,
            try_formats=try_formats,
        )
        if date is None:
            return None
        return date.strftime(output_format)

    @staticmethod
    def ftime(
        time_str: str,
        current_format: str = "%H:%M:%S",
        output_format: str = "%H:%M",
        try_formats: typing.List[str] = None,
    ):
        time = DATEFORMAT.date(
            time_str, current_format=current_format, try_formats=try_formats
        )
        if time is None:
            return None
        return time.strftime(output_format)

    @staticmethod
    def ftimestamp(timestamp: typing.Union[str, int] = None):
        if timestamp is None:
            return None
        return datetime.fromtimestamp(float(timestamp), timezone.utc).strftime("%H:%M")

    @staticmethod
    def is_business_hour(dt: datetime):
        # Define business hours
        start_hour = 9
        end_hour = 17

        # Check if the given datetime is within business hours
        if dt.weekday() >= 5:  # 5 and 6 correspond to Saturday and Sunday
            return False
        if dt.hour < start_hour or dt.hour >= end_hour:
            return False
        return True
