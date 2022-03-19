from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class Destination:
    CountryCode: Optional[str] = None
    ZIPCode: Optional[int] = None


@s(auto_attribs=True)
class AvailableServiceRequest:
    ContactID: Optional[int] = None
    Source: Optional[Destination] = JStruct[Destination]
    Destination: Optional[Destination] = JStruct[Destination]
