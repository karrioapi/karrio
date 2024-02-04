from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class LabelType:
    url: Optional[str] = None
    format: Optional[str] = None


@s(auto_attribs=True)
class SstatusType:
    title: Optional[str] = None
    status: Optional[int] = None


@s(auto_attribs=True)
class ItemType:
    shipmentNo: Optional[int] = None
    sstatus: Optional[SstatusType] = JStruct[SstatusType]
    label: Optional[LabelType] = JStruct[LabelType]


@s(auto_attribs=True)
class StatusType:
    title: Optional[str] = None
    statusCode: Optional[int] = None
    instance: Optional[str] = None
    detail: Optional[str] = None


@s(auto_attribs=True)
class CancelResponseType:
    status: Optional[StatusType] = JStruct[StatusType]
    items: List[ItemType] = JList[ItemType]
