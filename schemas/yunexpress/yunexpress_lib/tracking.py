import attr
from jstruct import JStruct, JList
from typing import Optional, List


@attr.s(auto_attribs=True)
class OrderInfo:
    msg: Optional[str] = None
    OrderNumber: Optional[str] = None
    TrackingNumber: Optional[str] = None
    WayBillNumber: Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponse:
    ResultCode: Optional[str] = None
    ResultDesc: Optional[str] = None
    Items: Optional[List[OrderInfo]] = JList[OrderInfo]
