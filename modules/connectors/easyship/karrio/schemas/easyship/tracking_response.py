from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class MetaType:
    requestid: Optional[str] = None


@s(auto_attribs=True)
class CheckpointType:
    checkpointtime: Optional[str] = None
    city: Optional[str] = None
    countryiso3: Optional[str] = None
    countryname: Optional[str] = None
    handler: Optional[str] = None
    location: Optional[str] = None
    message: Optional[str] = None
    ordernumber: Optional[str] = None
    postalcode: Optional[str] = None
    countryalpha2: Optional[str] = None
    description: Optional[str] = None
    primarystatus: Optional[str] = None
    state: Optional[str] = None


@s(auto_attribs=True)
class CourierType:
    id: Optional[str] = None
    umbrellaname: Optional[str] = None


@s(auto_attribs=True)
class TrackingType:
    courier: Optional[CourierType] = JStruct[CourierType]
    destinationcountryalpha2: Optional[str] = None
    easyshipshipmentid: Optional[str] = None
    etadate: Optional[str] = None
    id: Optional[str] = None
    origincountryalpha2: Optional[str] = None
    platformordernumber: Optional[str] = None
    source: Optional[str] = None
    status: Optional[str] = None
    trackingnumber: Optional[str] = None
    trackingstatus: Optional[str] = None
    trackingpageurl: Optional[str] = None
    checkpoints: List[CheckpointType] = JList[CheckpointType]


@s(auto_attribs=True)
class TrackingResponseType:
    meta: Optional[MetaType] = JStruct[MetaType]
    tracking: Optional[TrackingType] = JStruct[TrackingType]
