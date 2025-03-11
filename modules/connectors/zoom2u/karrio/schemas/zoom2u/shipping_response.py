import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ShippingResponseType:
    reference: typing.Optional[str] = None
    price: typing.Optional[float] = None
    trackinglink: typing.Optional[str] = None
    trackingCode: typing.Optional[str] = None
