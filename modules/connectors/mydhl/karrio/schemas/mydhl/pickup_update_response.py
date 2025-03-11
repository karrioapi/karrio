import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PickupUpdateResponseType:
    dispatchConfirmationNumber: typing.Optional[str] = None
    readyByTime: typing.Optional[str] = None
    nextPickupDate: typing.Optional[str] = None
    warnings: typing.Optional[typing.List[str]] = None
