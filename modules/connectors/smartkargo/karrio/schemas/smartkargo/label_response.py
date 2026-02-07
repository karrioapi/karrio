import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class LabelResponseType:
    base64Content: typing.Optional[str] = None
