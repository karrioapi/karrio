import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ValidationType:
    packageReference: typing.Optional[str] = None
    property: typing.Optional[str] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorResponseType:
    headerReference: typing.Any = None
    packageReference: typing.Any = None
    status: typing.Optional[str] = None
    details: typing.Any = None
    validations: typing.Optional[typing.List[ValidationType]] = jstruct.JList[ValidationType]
