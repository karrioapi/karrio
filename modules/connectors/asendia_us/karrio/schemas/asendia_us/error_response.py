import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorResponseType:
    responseStatusCode: typing.Optional[int] = None
    responseStatusMessage: typing.Optional[str] = None
