import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AuthResponseType:
    accessToken: typing.Optional[str] = None
    expDate: typing.Optional[int] = None
    refreshToken: typing.Optional[str] = None
    navigation: typing.Optional[int] = None
