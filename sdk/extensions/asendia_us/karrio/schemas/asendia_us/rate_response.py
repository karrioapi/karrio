from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class ResponseStatusType:
    responseStatusCode: Optional[str] = None
    responseStatusMessage: Optional[str] = None


@s(auto_attribs=True)
class ShippingRateType:
    productCode: Optional[str] = None
    rate: Optional[float] = None
    currencyType: Optional[str] = None


@s(auto_attribs=True)
class RateResponseType:
    shippingRates: List[ShippingRateType] = JList[ShippingRateType]
    responseStatus: Optional[ResponseStatusType] = JStruct[ResponseStatusType]
