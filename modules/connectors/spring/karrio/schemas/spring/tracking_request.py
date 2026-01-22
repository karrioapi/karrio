import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ShipmentType:
    TrackingNumber: typing.Optional[str] = None
    ShipperReference: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingRequestType:
    Apikey: typing.Optional[str] = None
    Command: typing.Optional[str] = None
    Shipment: typing.Optional[ShipmentType] = jstruct.JStruct[ShipmentType]
