import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ConsigneeAddressType:
    Name: typing.Optional[str] = None
    City: typing.Optional[str] = None
    State: typing.Optional[str] = None
    Zip: typing.Optional[str] = None
    Country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EventType:
    Timestamp: typing.Optional[int] = None
    DateTime: typing.Optional[str] = None
    Country: typing.Optional[str] = None
    City: typing.Optional[str] = None
    State: typing.Optional[str] = None
    Zip: typing.Optional[str] = None
    Code: typing.Optional[int] = None
    Description: typing.Optional[str] = None
    CarrierCode: typing.Optional[str] = None
    CarrierDescription: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentType:
    TrackingNumber: typing.Optional[str] = None
    ShipperReference: typing.Optional[str] = None
    DisplayId: typing.Optional[str] = None
    Service: typing.Optional[str] = None
    Carrier: typing.Optional[str] = None
    CarrierTrackingNumber: typing.Optional[str] = None
    CarrierLocalTrackingNumber: typing.Optional[str] = None
    CarrierTrackingUrl: typing.Optional[str] = None
    Weight: typing.Optional[str] = None
    WeightUnit: typing.Optional[str] = None
    ConsigneeAddress: typing.Optional[ConsigneeAddressType] = jstruct.JStruct[ConsigneeAddressType]
    Events: typing.Optional[typing.List[EventType]] = jstruct.JList[EventType]


@attr.s(auto_attribs=True)
class TrackingResponseType:
    ErrorLevel: typing.Optional[int] = None
    Error: typing.Optional[str] = None
    Shipment: typing.Optional[ShipmentType] = jstruct.JStruct[ShipmentType]
