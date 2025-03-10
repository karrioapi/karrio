import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class CancelResponseType:
    responseStatusCode: typing.Optional[int] = None
    responseStatusMessage: typing.Optional[str] = None
