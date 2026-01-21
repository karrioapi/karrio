import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AuthRequestType:
    username: typing.Optional[str] = None
    password: typing.Optional[str] = None
