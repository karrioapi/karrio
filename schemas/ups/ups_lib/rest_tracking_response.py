from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Address:
    city: Optional[str] = None
    stateProvince: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None


@s(auto_attribs=True)
class Location:
    address: Optional[Address] = JStruct[Address]


@s(auto_attribs=True)
class Status:
    type: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None


@s(auto_attribs=True)
class Activity:
    location: Optional[Location] = JStruct[Location]
    status: Optional[Status] = JStruct[Status]
    date: Optional[int] = None
    time: Optional[str] = None


@s(auto_attribs=True)
class DeliveryDate:
    type: Optional[str] = None
    date: Optional[int] = None


@s(auto_attribs=True)
class DeliveryTime:
    startTime: Optional[str] = None
    endTime: Optional[int] = None
    type: Optional[str] = None


@s(auto_attribs=True)
class Package:
    trackingNumber: Optional[str] = None
    deliveryDate: List[DeliveryDate] = JList[DeliveryDate]
    deliveryTime: Optional[DeliveryTime] = JStruct[DeliveryTime]
    activity: List[Activity] = JList[Activity]


@s(auto_attribs=True)
class Shipment:
    package: List[Package] = JList[Package]


@s(auto_attribs=True)
class TrackResponse:
    shipment: List[Shipment] = JList[Shipment]


@s(auto_attribs=True)
class RESTTrackingResponse:
    trackResponse: Optional[TrackResponse] = JStruct[TrackResponse]
