from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AdditionalPropType:
    pass


@s(auto_attribs=True)
class DataType:
    empty: Optional[bool] = None
    additionalProp1: Optional[AdditionalPropType] = JStruct[AdditionalPropType]
    additionalProp2: Optional[AdditionalPropType] = JStruct[AdditionalPropType]
    additionalProp3: Optional[AdditionalPropType] = JStruct[AdditionalPropType]


@s(auto_attribs=True)
class OriginalEventType:
    name: Optional[str] = None
    identifier: Optional[str] = None
    eventDate: Optional[str] = None
    eventLocation: Optional[str] = None
    data: Optional[DataType] = JStruct[DataType]


@s(auto_attribs=True)
class EventType:
    dateTime: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    proofOfDelivery: Optional[str] = None
    postalCode: Optional[str] = None
    additionalInformation: Optional[str] = None
    originalEvent: Optional[OriginalEventType] = JStruct[OriginalEventType]


@s(auto_attribs=True)
class ShipmentStatusType:
    labelGenerated: Optional[bool] = None
    reachedAtWarehouse: Optional[bool] = None
    inTransit: Optional[bool] = None
    delivered: Optional[bool] = None
    exception: Optional[bool] = None


@s(auto_attribs=True)
class TrackingResponseElementType:
    eventTime: Optional[str] = None
    shipDate: Optional[str] = None
    carrierName: Optional[str] = None
    carrierService: Optional[str] = None
    trackingUrl: Optional[str] = None
    trackingNumber: Optional[str] = None
    referenceCodes: List[str] = []
    expectedDeliveryDate: Optional[str] = None
    currentStatus: Optional[str] = None
    shipmentStatus: Optional[ShipmentStatusType] = JStruct[ShipmentStatusType]
    orderId: Optional[str] = None
    eventId: Optional[str] = None
    event: List[EventType] = JList[EventType]
