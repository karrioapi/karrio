import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ValidationMessageType:
    property: typing.Optional[str] = None
    validationMessage: typing.Optional[str] = None
    validationState: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ItemType:
    shipmentNo: typing.Optional[str] = None
    validationMessages: typing.Optional[typing.List[ValidationMessageType]] = jstruct.JList[ValidationMessageType]


@attr.s(auto_attribs=True)
class StatusType:
    title: typing.Optional[str] = None
    statusCode: typing.Optional[int] = None
    instance: typing.Optional[str] = None
    detail: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorResponseType:
    title: typing.Optional[str] = None
    statusCode: typing.Optional[int] = None
    instance: typing.Optional[str] = None
    detail: typing.Optional[str] = None
    status: typing.Optional[StatusType] = jstruct.JStruct[StatusType]
    items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]
