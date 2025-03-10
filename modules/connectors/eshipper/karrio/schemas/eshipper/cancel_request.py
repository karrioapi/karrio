import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class OrderType:
    trackingId: typing.Optional[str] = None
    orderId: typing.Optional[str] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CancelRequestType:
    order: typing.Optional[OrderType] = jstruct.JStruct[OrderType]
