from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class DestinationType:
    CountryCode: Optional[str] = None
    ZIPCode: Optional[int] = None


@s(auto_attribs=True)
class RatingRequestType:
    ContactID: Optional[int] = None
    Source: Optional[DestinationType] = JStruct[DestinationType]
    Destination: Optional[DestinationType] = JStruct[DestinationType]
