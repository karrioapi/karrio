import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingRequestType:
    trackingNumberVendor: typing.Optional[int] = None
