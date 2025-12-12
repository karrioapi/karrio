import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ShipmentCancelResponseType:
    shipmentTrackingNumber: typing.Optional[int] = None
    status: typing.Optional[str] = None
    message: typing.Optional[str] = None
