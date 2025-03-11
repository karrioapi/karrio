import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingRequestType:
    noSuivi: typing.Optional[str] = None
    refUniExp: typing.Optional[str] = None
