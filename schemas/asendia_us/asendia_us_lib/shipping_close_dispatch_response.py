from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class ReportElement:
    name: Optional[str] = None
    type: Optional[str] = None
    content: Optional[str] = None


@s(auto_attribs=True)
class ShippingCloseDispatchResponseReport:
    reports: List[ReportElement] = JList[ReportElement]


@s(auto_attribs=True)
class ResponseStatus:
    responseStatusCode: Optional[str] = None
    responseStatusMessage: Optional[str] = None


@s(auto_attribs=True)
class ShippingCloseDispatchResponse:
    report: Optional[ShippingCloseDispatchResponseReport] = JStruct[ShippingCloseDispatchResponseReport]
    responseStatus: Optional[ResponseStatus] = JStruct[ResponseStatus]
