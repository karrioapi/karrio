import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class JSONStatusType:
    title: typing.Optional[str] = None
    status: typing.Optional[int] = None
    type: typing.Optional[str] = None
    detail: typing.Optional[str] = None
    instance: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DocumentType:
    b64: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReturnOrderConfirmationType:
    shipmentNo: typing.Optional[str] = None
    internationalShipmentNo: typing.Optional[str] = None
    routingCode: typing.Optional[str] = None
    qrLink: typing.Optional[str] = None
    sstatus: typing.Optional[JSONStatusType] = jstruct.JStruct[JSONStatusType]
    label: typing.Optional[DocumentType] = jstruct.JStruct[DocumentType]
    qrLabel: typing.Optional[DocumentType] = jstruct.JStruct[DocumentType]
