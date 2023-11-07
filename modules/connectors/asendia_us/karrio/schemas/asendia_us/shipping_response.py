from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class LabelType:
    name: Optional[str] = None
    type: Optional[str] = None
    content: Optional[str] = None


@s(auto_attribs=True)
class PackageLabelType:
    packageId: Optional[str] = None
    trackingNumber: Optional[str] = None
    labels: List[LabelType] = JList[LabelType]


@s(auto_attribs=True)
class ResponseStatusType:
    responseStatusCode: Optional[str] = None
    responseStatusMessage: Optional[str] = None


@s(auto_attribs=True)
class ShippingRateType:
    productCode: Optional[str] = None
    rate: Optional[int] = None
    currencyType: Optional[str] = None


@s(auto_attribs=True)
class ShippingResponseType:
    shippingRates: List[ShippingRateType] = JList[ShippingRateType]
    packageLabel: Optional[PackageLabelType] = JStruct[PackageLabelType]
    responseStatus: Optional[ResponseStatusType] = JStruct[ResponseStatusType]
