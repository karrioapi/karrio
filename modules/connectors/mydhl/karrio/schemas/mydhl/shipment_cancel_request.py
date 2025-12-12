import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ShipmentCancelRequestType:
    shipmentTrackingNumber: typing.Optional[int] = None
    reason: typing.Optional[str] = None
