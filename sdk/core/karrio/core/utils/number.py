from typing import Union, Optional
from decimal import Decimal


class NUMBERFORMAT:
    @staticmethod
    def decimal(
        value: Union[str, float, bytes] = None, quant: Optional[float] = None
    ) -> Optional[float]:
        """Parse a value into a valid decimal number.

        :param value: a value that can be parsed to float.
        :param quant: decimal places for rounding.
        :return: a valid decimal number or None.
        """
        if value is None or isinstance(value, bool):
            return None
        if quant is not None:
            return float(Decimal(str(value)).quantize(Decimal(str(quant))))

        return round(float(value), 2)

    @staticmethod
    def integer(
        value: Union[str, int, bytes] = None, base: int = None
    ) -> Optional[int]:
        """Parse a value into a valid integer number.

        :param value: a value that can be parsed into integer.
        :param base: a rounding base value.
        :return: a valid integer number or None.
        """
        if value is None or isinstance(value, bool):
            return None
        return int(value if base is None else base * round(float(value) / base))
