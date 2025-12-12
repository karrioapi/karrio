import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingRequestType:
    shipmentTrackingNumber: typing.Optional[typing.List[str]] = None
