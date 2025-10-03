import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingRequestType:
    tracking_ids: typing.Optional[str] = None
