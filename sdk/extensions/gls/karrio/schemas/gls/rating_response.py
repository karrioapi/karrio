from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class AllowedServiceType:
    ProductName: Optional[str] = None
    ServiceName: Optional[str] = None


@s(auto_attribs=True)
class RatingResponseType:
    AllowedServices: List[AllowedServiceType] = JList[AllowedServiceType]
