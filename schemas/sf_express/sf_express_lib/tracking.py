import attr
from jstruct import JList, JStruct
from typing import Optional, List


@attr.s(auto_attribs=True)
class TrackingRequest:
    language: Optional[str] = None
    trackingType: Optional[str] = None
    methodType: Optional[str] = None
    trackingNumber: Optional[List[str]] = None
    checkPhoneNo: Optional[str] = None


@attr.s(auto_attribs=True)
class Route:
    opCode: Optional[str] = None
    acceptTime: Optional[str] = None
    acceptAddress: Optional[str] = None
    remark: Optional[str] = None


@attr.s(auto_attribs=True)
class RouteResp:
    mailNo: Optional[str] = None
    routes: Optional[List[Route]] = JList[Route]


@attr.s(auto_attribs=True)
class MsgData:
    routeResps: Optional[List[RouteResp]] = JList[RouteResp]


@attr.s(auto_attribs=True)
class TrackingResponse:
    errorMsg: Optional[str] = None
    success: Optional[bool] = None
    errorCode: Optional[str] = None
    msgData: Optional[MsgData] = JStruct[MsgData]
