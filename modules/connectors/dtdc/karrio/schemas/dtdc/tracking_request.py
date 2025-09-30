import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingRequestType:
    trkType: typing.Optional[str] = None
    strcnno: typing.Optional[str] = None
    addtnlDtl: typing.Optional[str] = None
