from typing import Union, Optional


def decimal(value: Union[str, float] = None) -> Optional[float]:
    if value is None:
        return None
    return round(float(value), 2)
