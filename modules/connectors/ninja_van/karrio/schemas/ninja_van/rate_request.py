from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class FromType:
    l1_tier_code: Optional[str] = None
    l2_tier_code: Optional[str] = None


@s(auto_attribs=True)
class RateRequestType:
    weight: Optional[int] = None
    service_level: Optional[str] = None
    rate_request_from: Optional[FromType] = JStruct[FromType]
    rate_request_to: Optional[FromType] = JStruct[FromType]
