import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Rate:
    id: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentPurchase:
    insurance: typing.Optional[float] = None
    rate: typing.Optional[Rate] = jstruct.JStruct[Rate]
