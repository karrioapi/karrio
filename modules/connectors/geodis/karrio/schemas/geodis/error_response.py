import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorResponseType:
    ok: typing.Optional[bool] = None
    codeErreur: typing.Optional[str] = None
    texteErreur: typing.Optional[str] = None
