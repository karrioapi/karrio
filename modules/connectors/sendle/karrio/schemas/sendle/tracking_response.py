from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class DestinationType:
    country: Optional[str] = None


@s(auto_attribs=True)
class SchedulingType:
    pickupdate: Optional[str] = None
    pickedupon: Optional[str] = None
    deliveredon: Optional[str] = None
    estimateddeliverydateminimum: Optional[str] = None
    estimateddeliverydatemaximum: Optional[str] = None
    status: Optional[str] = None


@s(auto_attribs=True)
class StatusType:
    description: Optional[str] = None
    lastchangedat: Optional[str] = None


@s(auto_attribs=True)
class TrackingEventType:
    eventtype: Optional[str] = None
    scantime: Optional[str] = None
    description: Optional[str] = None
    reason: Optional[str] = None
    displaytime: Optional[str] = None
    location: Optional[str] = None
    localscantime: Optional[str] = None


@s(auto_attribs=True)
class TrackingResponseType:
    state: Optional[str] = None
    status: Optional[StatusType] = JStruct[StatusType]
    origin: Optional[DestinationType] = JStruct[DestinationType]
    destination: Optional[DestinationType] = JStruct[DestinationType]
    scheduling: Optional[SchedulingType] = JStruct[SchedulingType]
    trackingevents: List[TrackingEventType] = JList[TrackingEventType]
