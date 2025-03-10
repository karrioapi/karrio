import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class OrderType:
    trackingId: typing.Optional[str] = None
    orderId: typing.Optional[str] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CancelResponseType:
    order: typing.Optional[typing.List[OrderType]] = jstruct.JList[OrderType]
