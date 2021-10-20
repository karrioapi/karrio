from attr import s
from typing import Optional


@s(auto_attribs=True)
class ValidateAddressRequest:
    type: Optional[str] = None
    countryCode: Optional[str] = None
    postalCode: Optional[int] = None
    cityName: Optional[str] = None
    strictValidation: Optional[bool] = None
