import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PickupCancelResponseType:
    dispatchConfirmationNumber: typing.Optional[str] = None
    status: typing.Optional[str] = None
