import math
import typing
import decimal


class NUMBERFORMAT:
    @staticmethod
    def decimal(
        value: typing.Union[str, float, bytes] = None,
        quant: typing.Optional[float] = None,
    ) -> typing.Optional[float]:
        """Parse a value into a valid decimal number.

        :param value: a value that can be parsed to float.
        :param quant: decimal places for rounding.
        :return: a valid decimal number or None.
        """
        if value is None or isinstance(value, bool):
            return None

        if quant is not None:
            _result = float(
                decimal.Decimal(str(value)).quantize(decimal.Decimal(str(quant)))
            )
            return _result if _result != 0 else float(decimal.Decimal(str(value)))

        _float = float(value)
        _rounded = round(_float, 2)

        return _rounded if _rounded != 0 else _float

    @staticmethod
    def numeric_decimal(
        value: typing.Union[str, float, bytes] = None,
        total_digits: int = 3,
        decimal_digits: int = 3,
    ) -> str:
        """Convert a float to a zero-padded string with customizable total length and decimal places.

        Args:
        value (float): A floating point number to be formatted.
        total_digits (int): The total length of the output string (including both numeric and decimal parts).
        decimal_digits (int): The number of decimal digits (d) in the final output.

        Returns:
        str: A zero-padded string of total_digits length, with the last decimal_digits as decimals.

        Examples:
        >>> format_to_custom_numeric_decimal(1.0, 7, 3)  # NNNNddd
        '0001000'

        >>> format_to_custom_numeric_decimal(1.0, 8, 3)  # NNNNNddd
        '00001000'

        >>> format_to_custom_numeric_decimal(1.0, 6, 3)  # NNNddd
        '001000'
        """
        if value is None or isinstance(value, bool):
            return None

        # Multiply the input float by 10^decimal_digits to scale the decimal part
        scaling_factor = 10**decimal_digits
        scaled_value = int(value * scaling_factor)

        # Format as a zero-padded string with the total number of digits
        return f"{scaled_value:0{total_digits}d}"

    @staticmethod
    def integer(
        value: typing.Union[str, int, bytes] = None, base: int = None
    ) -> typing.Optional[int]:
        """Parse a value into a valid integer number.

        :param value: a value that can be parsed into integer.
        :param base: a rounding base value.
        :return: a valid integer number or None.
        """
        if value is None or isinstance(value, bool):
            return None

        return math.ceil(
            float(value) if base is None else base * round(float(value) / base)
        )
