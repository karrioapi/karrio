import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class WeightType:
    unit: typing.Optional[str] = None
    value: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class ValueType:
    amount: typing.Optional[int] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CommodityType:
    sku: typing.Optional[str] = None
    title: typing.Optional[str] = None
    value: typing.Optional[ValueType] = jstruct.JStruct[ValueType]
    quantity: typing.Optional[int] = None
    unitWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    description: typing.Optional[str] = None
    countryOfOrigin: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomsType:
    EORI: typing.Optional[str] = None
    contentType: typing.Optional[str] = None
    invoiceDate: typing.Optional[str] = None
    invoiceNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DimensionsType:
    unit: typing.Optional[str] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    length: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class MetadataType:
    fulfillmentOrderId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AddressType:
    city: typing.Optional[str] = None
    line1: typing.Optional[str] = None
    state: typing.Optional[str] = None
    country: typing.Optional[str] = None
    postcode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipFromType:
    name: typing.Optional[str] = None
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    company: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipToType:
    name: typing.Optional[str] = None
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    serviceCode: typing.Optional[str] = None
    customerReference: typing.Optional[str] = None
    packageType: typing.Optional[str] = None
    shipTo: typing.Optional[ShipToType] = jstruct.JStruct[ShipToType]
    shipFrom: typing.Optional[ShipFromType] = jstruct.JStruct[ShipFromType]
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    commodities: typing.Optional[typing.List[CommodityType]] = jstruct.JList[CommodityType]
    metadata: typing.Optional[MetadataType] = jstruct.JStruct[MetadataType]
    customs: typing.Optional[CustomsType] = jstruct.JStruct[CustomsType]
