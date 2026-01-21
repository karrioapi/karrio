import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingRequestType:
    trackingNumbers: typing.Optional[typing.List[str]] = None
