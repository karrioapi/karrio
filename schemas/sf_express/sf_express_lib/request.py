import attr
from typing import Any
from jstruct import JList, JStruct
from typing import Optional, List


@attr.s(auto_attribs=True)
class Request:
    partnerID: Optional[str] = None
    requestID: Optional[str] = None
    serviceCode: Optional[str] = None
    timestamp: Optional[str] = None
    msgDigest: Optional[str] = None
    msgData: Optional[Any] = None
