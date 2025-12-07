import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PickupCancelRequestType:
    dispatchConfirmationNumber: typing.Optional[str] = None
    requestorName: typing.Optional[str] = None
    reason: typing.Optional[str] = None
