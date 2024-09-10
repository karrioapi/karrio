from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ArrivedAtOriginHubInformationType:
    country: Optional[str] = None
    city: Optional[str] = None
    hub: Optional[str] = None


@s(auto_attribs=True)
class EventType:
    shipperid: Optional[int] = None
    trackingnumber: Optional[str] = None
    shipperorderrefno: Optional[str] = None
    timestamp: Optional[str] = None
    status: Optional[str] = None
    isparcelonrtsleg: Optional[bool] = None
    comments: Optional[str] = None
    arrivedatoriginhubinformation: Optional[ArrivedAtOriginHubInformationType] = JStruct[ArrivedAtOriginHubInformationType]


@s(auto_attribs=True)
class DatumType:
    trackingnumber: Optional[str] = None
    isfullhistoryavailable: Optional[bool] = None
    events: List[EventType] = JList[EventType]


@s(auto_attribs=True)
class TrackingResponseType:
    data: List[DatumType] = JList[DatumType]
