from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class AllowedService:
    ProductName: Optional[str] = None
    ServiceName: Optional[str] = None


@s(auto_attribs=True)
class AvailableServiceResponse:
    AllowedServices: List[AllowedService] = JList[AllowedService]
