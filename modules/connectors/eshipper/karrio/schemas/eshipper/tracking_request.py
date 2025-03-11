import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingRequestType:
    includePublished: typing.Optional[bool] = None
    pageable: typing.Optional[str] = None
    trackingNumbers: typing.Optional[typing.List[str]] = None
