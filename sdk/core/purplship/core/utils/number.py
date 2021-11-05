from typing import Union, Optional
from decimal import Decimal


class NUMBERFORMAT:
    @staticmethod
    def decimal(value: Union[str, float, bytes] = None, quant: Optional[float] = None) -> Optional[float]:
        if value is None:
            return None
        if quant is not None:
            return float(Decimal(str(value)).quantize(Decimal(str(quant))))

        return round(float(value), 2)

    @staticmethod
    def integer(value: Union[str, int, bytes] = None, base: int = None) -> Optional[int]:
        if value is None:
            return None
        return int(value if base is None else base * round(float(value)/base))
