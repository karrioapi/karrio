import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class RateResponseElementType:
    deliverySpeed: typing.Optional[str] = None
    price: typing.Optional[int] = None
    deliveredBy: typing.Optional[str] = None
    earliestPickupEta: typing.Optional[str] = None
    earliestDropEta: typing.Optional[str] = None
