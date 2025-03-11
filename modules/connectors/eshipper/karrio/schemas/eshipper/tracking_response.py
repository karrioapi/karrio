import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AdditionalPropType:
    pass


@attr.s(auto_attribs=True)
class DataType:
    empty: typing.Optional[bool] = None
    additionalProp1: typing.Optional[AdditionalPropType] = jstruct.JStruct[AdditionalPropType]
    additionalProp2: typing.Optional[AdditionalPropType] = jstruct.JStruct[AdditionalPropType]
    additionalProp3: typing.Optional[AdditionalPropType] = jstruct.JStruct[AdditionalPropType]


@attr.s(auto_attribs=True)
class OriginalEventType:
    name: typing.Optional[str] = None
    identifier: typing.Optional[str] = None
    eventDate: typing.Optional[str] = None
    eventLocation: typing.Optional[str] = None
    data: typing.Optional[DataType] = jstruct.JStruct[DataType]


@attr.s(auto_attribs=True)
class EventType:
    dateTime: typing.Optional[str] = None
    description: typing.Optional[str] = None
    location: typing.Optional[str] = None
    proofOfDelivery: typing.Optional[str] = None
    postalCode: typing.Optional[str] = None
    additionalInformation: typing.Optional[str] = None
    originalEvent: typing.Optional[OriginalEventType] = jstruct.JStruct[OriginalEventType]


@attr.s(auto_attribs=True)
class ShipmentStatusType:
    labelGenerated: typing.Optional[bool] = None
    reachedAtWarehouse: typing.Optional[bool] = None
    inTransit: typing.Optional[bool] = None
    delivered: typing.Optional[bool] = None
    exception: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class TrackingResponseElementType:
    eventTime: typing.Optional[str] = None
    shipDate: typing.Optional[str] = None
    carrierName: typing.Optional[str] = None
    carrierService: typing.Optional[str] = None
    trackingUrl: typing.Optional[str] = None
    trackingNumber: typing.Optional[str] = None
    referenceCodes: typing.Optional[typing.List[str]] = None
    expectedDeliveryDate: typing.Optional[str] = None
    currentStatus: typing.Optional[str] = None
    shipmentStatus: typing.Optional[ShipmentStatusType] = jstruct.JStruct[ShipmentStatusType]
    orderId: typing.Optional[str] = None
    eventId: typing.Optional[str] = None
    event: typing.Optional[typing.List[EventType]] = jstruct.JList[EventType]
