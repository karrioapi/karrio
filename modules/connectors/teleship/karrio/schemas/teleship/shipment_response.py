import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ChargeType:
    name: typing.Optional[str] = None
    amount: typing.Optional[float] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DimensionsType:
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    unit: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DocumentType:
    type: typing.Optional[str] = None
    format: typing.Optional[str] = None
    url: typing.Optional[str] = None
    base64String: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AddressType:
    line1: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    postcode: typing.Optional[str] = None
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipFromType:
    name: typing.Optional[str] = None
    company: typing.Optional[str] = None
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]


@attr.s(auto_attribs=True)
class ShipToType:
    name: typing.Optional[str] = None
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]


@attr.s(auto_attribs=True)
class TotalChargeType:
    amount: typing.Optional[float] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class WeightType:
    value: typing.Optional[float] = None
    unit: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentType:
    shipmentId: typing.Optional[str] = None
    trackingNumber: typing.Optional[str] = None
    status: typing.Optional[str] = None
    customerReference: typing.Optional[str] = None
    serviceCode: typing.Optional[str] = None
    serviceName: typing.Optional[str] = None
    shipDate: typing.Optional[str] = None
    estimatedDelivery: typing.Optional[str] = None
    packageType: typing.Optional[str] = None
    documents: typing.Optional[typing.List[DocumentType]] = jstruct.JList[DocumentType]
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    shipTo: typing.Optional[ShipToType] = jstruct.JStruct[ShipToType]
    shipFrom: typing.Optional[ShipFromType] = jstruct.JStruct[ShipFromType]
    charges: typing.Optional[typing.List[ChargeType]] = jstruct.JList[ChargeType]
    totalCharge: typing.Optional[TotalChargeType] = jstruct.JStruct[TotalChargeType]


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    shipment: typing.Optional[ShipmentType] = jstruct.JStruct[ShipmentType]
    messages: typing.Optional[typing.List[typing.Any]] = None
