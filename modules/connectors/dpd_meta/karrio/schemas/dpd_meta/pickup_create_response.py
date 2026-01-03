import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DebugListType:
    methodName: typing.Optional[str] = None
    request: typing.Optional[str] = None
    response: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ScheduledPickupResponseType:
    pickupreference: typing.Optional[str] = None
    statusCode: typing.Optional[str] = None
    statusDescription: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupCreateResponseType:
    scheduledPickupResponse: typing.Optional[typing.List[ScheduledPickupResponseType]] = jstruct.JList[ScheduledPickupResponseType]
    debugList: typing.Optional[typing.List[DebugListType]] = jstruct.JList[DebugListType]
