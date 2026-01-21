import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ShipmentCancelResponseType:
    success: typing.Optional[bool] = None
    message: typing.Optional[str] = None
