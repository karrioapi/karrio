import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class OrderTrackingRequestType:
    trackingnumber: typing.Optional[int] = None
