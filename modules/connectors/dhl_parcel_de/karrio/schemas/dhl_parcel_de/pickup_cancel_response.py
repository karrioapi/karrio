import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class EdCancellationType:
    orderID: typing.Optional[str] = None
    orderState: typing.Optional[str] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupCancelResponseType:
    confirmedCancellations: typing.Optional[typing.List[EdCancellationType]] = jstruct.JList[EdCancellationType]
    failedCancellations: typing.Optional[typing.List[EdCancellationType]] = jstruct.JList[EdCancellationType]
