import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingRequestType:
    shipmentno: typing.Optional[int] = None
