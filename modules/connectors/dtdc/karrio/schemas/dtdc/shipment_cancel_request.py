import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ShipmentCancelRequestType:
    AWBNo: typing.Optional[typing.List[str]] = None
    customerCode: typing.Optional[str] = None
