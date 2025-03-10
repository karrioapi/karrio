import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PickupResponseType:
    dispatchConfirmationNumbers: typing.Optional[typing.List[str]] = None
