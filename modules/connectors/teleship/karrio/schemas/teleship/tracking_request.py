import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingRequestType:
    trackingNumber: typing.Optional[str] = None
