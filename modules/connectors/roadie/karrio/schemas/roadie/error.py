import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorElement:
    code: typing.Optional[int] = None
    parameter: typing.Optional[str] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Error:
    errors: typing.Optional[typing.List[ErrorElement]] = jstruct.JList[ErrorElement]
