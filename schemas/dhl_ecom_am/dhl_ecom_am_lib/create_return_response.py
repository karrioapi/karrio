from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class Label:
    createdOn: Optional[str] = None
    authorizationNumber: Optional[int] = None
    dhlPackageId: Optional[str] = None
    trackingId: Optional[str] = None
    labelData: Optional[str] = None
    encodeType: Optional[str] = None
    format: Optional[str] = None
    link: Optional[str] = None


@s(auto_attribs=True)
class CreateReturnResponse:
    timestamp: Optional[str] = None
    pickup: Optional[int] = None
    orderedProductId: Optional[str] = None
    labels: List[Label] = JList[Label]
