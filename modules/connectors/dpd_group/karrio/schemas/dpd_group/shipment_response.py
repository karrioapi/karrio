import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class LabelType:
    format: typing.Optional[str] = None
    content: typing.Optional[str] = None
    encoding: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelType:
    parcelNumber: typing.Optional[str] = None
    trackingNumber: typing.Optional[str] = None
    parcelId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ServicesType:
    productCode: typing.Optional[str] = None
    productName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    shipmentId: typing.Optional[str] = None
    shipmentNumber: typing.Optional[str] = None
    parcels: typing.Optional[typing.List[ParcelType]] = jstruct.JList[ParcelType]
    label: typing.Optional[LabelType] = jstruct.JStruct[LabelType]
    shipmentDate: typing.Optional[str] = None
    trackingUrl: typing.Optional[str] = None
    services: typing.Optional[ServicesType] = jstruct.JStruct[ServicesType]
