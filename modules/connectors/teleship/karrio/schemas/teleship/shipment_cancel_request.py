import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ShipmentCancelRequestType:
    shipmentId: typing.Optional[str] = None
