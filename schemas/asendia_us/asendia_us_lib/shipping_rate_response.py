from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class ResponseStatus:
    responseStatusCode: Optional[str] = None
    responseStatusMessage: Optional[str] = None


@s(auto_attribs=True)
class ShippingRate:
    productCode: Optional[str] = None
    rate: Optional[float] = None
    currencyType: Optional[str] = None


@s(auto_attribs=True)
class ShippingRateResponse:
    shippingRates: List[ShippingRate] = JList[ShippingRate]
    responseStatus: Optional[ResponseStatus] = JStruct[ResponseStatus]
