import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DebugListType:
    request: typing.Optional[str] = None
    response: typing.Optional[str] = None
    methodName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorResponseType:
    errorCode: typing.Optional[str] = None
    errorMessage: typing.Optional[str] = None
    errorOrigin: typing.Optional[str] = None
    debugList: typing.Optional[typing.List[DebugListType]] = jstruct.JList[DebugListType]
