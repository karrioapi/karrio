from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class TrackResponseType:
    pass


@s(auto_attribs=True)
class TrackingResponseType:
    TrackResponse: Optional[TrackResponseType] = JStruct[TrackResponseType]
