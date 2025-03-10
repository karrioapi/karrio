import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Error:
    errorCode: typing.Optional[str] = None
    errorDescription: typing.Optional[str] = None
    errorCause: typing.Optional[str] = None
    errorResolution: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Errors:
    httpCode: typing.Optional[int] = None
    httpMessage: typing.Optional[str] = None
    moreInformation: typing.Optional[str] = None
    errors: typing.Optional[typing.List[Error]] = jstruct.JList[Error]
