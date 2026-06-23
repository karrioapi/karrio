import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PickupResponseType:
    EstimatedPickUpDate: typing.Optional[str] = None
