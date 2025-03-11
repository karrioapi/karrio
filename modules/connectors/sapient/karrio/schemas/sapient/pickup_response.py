import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PickupResponseType:
    CollectionOrderId: typing.Optional[str] = None
    CollectionDate: typing.Optional[str] = None
