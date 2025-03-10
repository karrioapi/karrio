import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorResponseType:
    Property: typing.Optional[str] = None
    Message: typing.Optional[str] = None
    Key: typing.Optional[str] = None
    Value: typing.Optional[str] = None
