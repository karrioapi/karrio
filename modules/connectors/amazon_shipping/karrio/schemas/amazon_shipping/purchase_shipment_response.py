import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Benefits:
    includedBenefits: typing.Optional[typing.List[str]] = None
    excludedBenefits: typing.Optional[typing.List[typing.Any]] = None


@attr.s(auto_attribs=True)
class PackageDocument:
    type: typing.Optional[str] = None
    format: typing.Optional[str] = None
    contents: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageDocumentDetail:
    packageClientReferenceId: typing.Optional[str] = None
    packageDocuments: typing.Optional[typing.List[PackageDocument]] = jstruct.JList[PackageDocument]
    trackingId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Window:
    start: typing.Optional[str] = None
    end: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Promise:
    deliveryWindow: typing.Optional[Window] = jstruct.JStruct[Window]
    pickupWindow: typing.Optional[Window] = jstruct.JStruct[Window]


@attr.s(auto_attribs=True)
class TotalCharge:
    value: typing.Optional[float] = None
    unit: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Payload:
    shipmentId: typing.Optional[str] = None
    packageDocumentDetails: typing.Optional[typing.List[PackageDocumentDetail]] = jstruct.JList[PackageDocumentDetail]
    promise: typing.Optional[Promise] = jstruct.JStruct[Promise]
    benefits: typing.Optional[Benefits] = jstruct.JStruct[Benefits]
    totalCharge: typing.Optional[TotalCharge] = jstruct.JStruct[TotalCharge]


@attr.s(auto_attribs=True)
class PurchaseShipmentResponse:
    payload: typing.Optional[Payload] = jstruct.JStruct[Payload]
