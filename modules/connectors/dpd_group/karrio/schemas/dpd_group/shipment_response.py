import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DebugListType:
    methodName: typing.Optional[str] = None
    request: typing.Optional[str] = None
    response: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class LabelType:
    base64Data: typing.Optional[str] = None
    mediatype: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelBarcodeType:
    parcel: typing.Optional[str] = None
    barcode: typing.Optional[str] = None
    reference: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    shipmentId: typing.Optional[str] = None
    parcelIds: typing.Optional[typing.List[str]] = None
    networkShipmentId: typing.Optional[str] = None
    networkParcelIds: typing.Optional[typing.List[str]] = None
    parcelBarcodes: typing.Optional[typing.List[ParcelBarcodeType]] = jstruct.JList[ParcelBarcodeType]
    label: typing.Optional[LabelType] = jstruct.JStruct[LabelType]
    qrcode: typing.Optional[LabelType] = jstruct.JStruct[LabelType]
    debugList: typing.Optional[typing.List[DebugListType]] = jstruct.JList[DebugListType]
