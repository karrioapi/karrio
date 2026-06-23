import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Carrier:
    id: typing.Optional[str] = None
    name: typing.Optional[str] = None


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
class Charge:
    value: typing.Optional[float] = None
    unit: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateItem:
    rateItemCharge: typing.Optional[Charge] = jstruct.JStruct[Charge]
    rateItemID: typing.Optional[str] = None
    rateItemNameLocalization: typing.Optional[str] = None
    rateItemType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Payload:
    shipmentId: typing.Optional[str] = None
    packageDocumentDetails: typing.Optional[typing.List[PackageDocumentDetail]] = jstruct.JList[PackageDocumentDetail]
    promise: typing.Optional[Promise] = jstruct.JStruct[Promise]
    carrier: typing.Optional[Carrier] = jstruct.JStruct[Carrier]
    service: typing.Optional[Carrier] = jstruct.JStruct[Carrier]
    totalCharge: typing.Optional[Charge] = jstruct.JStruct[Charge]
    rateItems: typing.Optional[typing.List[RateItem]] = jstruct.JList[RateItem]


@attr.s(auto_attribs=True)
class OneClickShipmentResponse:
    payload: typing.Optional[Payload] = jstruct.JStruct[Payload]
