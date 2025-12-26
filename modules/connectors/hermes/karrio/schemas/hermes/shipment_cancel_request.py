import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ShipmentCancelRequestType:
    shipmentOrderID: typing.Optional[str] = None
