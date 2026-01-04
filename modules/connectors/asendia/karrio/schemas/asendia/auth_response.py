import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AuthResponseType:
    id_token: typing.Optional[str] = None
