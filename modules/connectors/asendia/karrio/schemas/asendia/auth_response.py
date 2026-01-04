import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AuthResponseType:
    idtoken: typing.Optional[str] = None
