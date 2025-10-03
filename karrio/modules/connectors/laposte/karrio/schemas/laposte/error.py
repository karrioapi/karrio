import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Error:
    returnCode: typing.Optional[int] = None
    returnMessage: typing.Optional[str] = None
    lang: typing.Optional[str] = None
    scope: typing.Optional[str] = None
    idShip: typing.Optional[str] = None
    code: typing.Optional[str] = None
    message: typing.Optional[str] = None
