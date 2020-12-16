from typing import Union, Optional


class NUMBERFORMAT:
    @staticmethod
    def decimal(value: Union[str, float, bytes] = None) -> Optional[float]:
        if value is None:
            return None
        return round(float(value), 2)

    @staticmethod
    def integer(value: Union[str, int, bytes] = None) -> Optional[int]:
        if value is None:
            return None
        return int(value)
