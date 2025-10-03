import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class LabelResponseType:
    referenceNumber: typing.Optional[str] = None
    label: typing.Optional[str] = None
