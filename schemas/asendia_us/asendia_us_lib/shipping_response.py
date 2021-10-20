from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class Label:
    name: Optional[str] = None
    type: Optional[str] = None
    content: Optional[str] = None


@s(auto_attribs=True)
class PackageLabel:
    packageId: Optional[str] = None
    trackingNumber: Optional[str] = None
    labels: List[Label] = JList[Label]


@s(auto_attribs=True)
class ResponseStatus:
    responseStatusCode: Optional[str] = None
    responseStatusMessage: Optional[str] = None


@s(auto_attribs=True)
class ShippingResponse:
    packageLabel: Optional[PackageLabel] = JStruct[PackageLabel]
    responseStatus: Optional[ResponseStatus] = JStruct[ResponseStatus]
