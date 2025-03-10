import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class CodLabelType:
    b64: typing.Optional[str] = None
    zpl2: typing.Optional[str] = None
    url: typing.Optional[str] = None
    fileFormat: typing.Optional[str] = None
    printFormat: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class StatusType:
    title: typing.Optional[str] = None
    statusCode: typing.Optional[int] = None
    instance: typing.Optional[str] = None
    detail: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ValidationMessageType:
    property: typing.Optional[str] = None
    validationMessage: typing.Optional[str] = None
    validationState: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ItemType:
    shipmentNo: typing.Optional[str] = None
    returnShipmentNo: typing.Optional[str] = None
    sstatus: typing.Optional[StatusType] = jstruct.JStruct[StatusType]
    shipmentRefNo: typing.Optional[str] = None
    label: typing.Optional[CodLabelType] = jstruct.JStruct[CodLabelType]
    returnLabel: typing.Optional[CodLabelType] = jstruct.JStruct[CodLabelType]
    customsDoc: typing.Optional[CodLabelType] = jstruct.JStruct[CodLabelType]
    codLabel: typing.Optional[CodLabelType] = jstruct.JStruct[CodLabelType]
    validationMessages: typing.Optional[typing.List[ValidationMessageType]] = jstruct.JList[ValidationMessageType]


@attr.s(auto_attribs=True)
class ShippingResponseType:
    status: typing.Optional[StatusType] = jstruct.JStruct[StatusType]
    items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]
