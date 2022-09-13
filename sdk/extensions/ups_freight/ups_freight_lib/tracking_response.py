from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AddressType:
    city: Optional[str] = None
    stateProvince: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None


@s(auto_attribs=True)
class LocationType:
    address: Optional[AddressType] = JStruct[AddressType]


@s(auto_attribs=True)
class StatusType:
    type: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None


@s(auto_attribs=True)
class ActivityType:
    location: Optional[LocationType] = JStruct[LocationType]
    status: Optional[StatusType] = JStruct[StatusType]
    date: Optional[int] = None
    time: Optional[str] = None


@s(auto_attribs=True)
class DeliveryDateType:
    type: Optional[str] = None
    date: Optional[int] = None


@s(auto_attribs=True)
class DeliveryTimeType:
    startTime: Optional[str] = None
    endTime: Optional[int] = None
    type: Optional[str] = None


@s(auto_attribs=True)
class PackageType:
    trackingNumber: Optional[str] = None
    deliveryDate: List[DeliveryDateType] = JList[DeliveryDateType]
    deliveryTime: Optional[DeliveryTimeType] = JStruct[DeliveryTimeType]
    activity: List[ActivityType] = JList[ActivityType]


@s(auto_attribs=True)
class ShipmentType:
    package: List[PackageType] = JList[PackageType]


@s(auto_attribs=True)
class TrackResponseType:
    shipment: List[ShipmentType] = JList[ShipmentType]


@s(auto_attribs=True)
class TrackingResponseType:
    trackResponse: Optional[TrackResponseType] = JStruct[TrackResponseType]
