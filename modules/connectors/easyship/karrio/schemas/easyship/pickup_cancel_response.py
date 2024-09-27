from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class MetaType:
    request_id: Optional[str] = None


@s(auto_attribs=True)
class SuccessType:
    message: Optional[str] = None


@s(auto_attribs=True)
class PickupCancelResponseType:
    meta: Optional[MetaType] = JStruct[MetaType]
    success: Optional[SuccessType] = JStruct[SuccessType]
