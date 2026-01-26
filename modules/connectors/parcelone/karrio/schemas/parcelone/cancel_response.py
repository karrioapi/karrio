import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorType:
    ErrorNo: typing.Optional[str] = None
    Message: typing.Optional[str] = None
    StatusCode: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class WarningType:
    WarningNo: typing.Optional[str] = None
    Message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ResultsType:
    ShipmentID: typing.Optional[int] = None
    ShipmentRef: typing.Optional[str] = None
    TrackingID: typing.Optional[str] = None
    Success: typing.Optional[int] = None
    Errors: typing.Optional[typing.List[ErrorType]] = jstruct.JList[ErrorType]
    Warnings: typing.Optional[typing.List[WarningType]] = jstruct.JList[WarningType]


@attr.s(auto_attribs=True)
class CancelResponseType:
    status: typing.Optional[int] = None
    success: typing.Optional[int] = None
    message: typing.Optional[str] = None
    type: typing.Optional[str] = None
    instance: typing.Optional[str] = None
    results: typing.Optional[ResultsType] = jstruct.JStruct[ResultsType]
    UniqId: typing.Optional[str] = None
