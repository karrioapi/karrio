import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AuthRequestType:
    username: typing.Optional[str] = None
    password: typing.Optional[str] = None
    customerType: typing.Optional[int] = None
    deviceId: typing.Optional[str] = None
    fcmToken: typing.Optional[str] = None
