import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ShipmentCancelRequestType:
    parcelId: typing.Optional[str] = None
