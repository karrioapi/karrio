import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class UnitWeightType:
    unit: typing.Optional[str] = None
    value: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class ConsigneeChargesType:
    amount: typing.Optional[float] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CommodityType:
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    hsCode: typing.Optional[str] = None
    sku: typing.Optional[str] = None
    quantity: typing.Optional[int] = None
    value: typing.Optional[ConsigneeChargesType] = jstruct.JStruct[ConsigneeChargesType]
    unitWeight: typing.Optional[UnitWeightType] = jstruct.JStruct[UnitWeightType]
    countryOfOrigin: typing.Optional[str] = None
    category: typing.Optional[str] = None
    imageUrl: typing.Optional[str] = None
    productUrl: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomsType:
    contentType: typing.Optional[str] = None
    incoterms: typing.Optional[str] = None
    invoiceNumber: typing.Optional[str] = None
    invoiceDate: typing.Optional[str] = None
    EORI: typing.Optional[str] = None
    VAT: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class MessageType:
    code: typing.Optional[int] = None
    level: typing.Optional[str] = None
    timestamp: typing.Optional[str] = None
    message: typing.Optional[str] = None
    details: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class AddressType:
    line1: typing.Optional[str] = None
    line2: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    postcode: typing.Optional[str] = None
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipType:
    name: typing.Optional[str] = None
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    company: typing.Optional[str] = None
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]


@attr.s(auto_attribs=True)
class DutiesTaxesRequestType:
    messages: typing.Optional[typing.List[MessageType]] = jstruct.JList[MessageType]
    shipTo: typing.Optional[ShipType] = jstruct.JStruct[ShipType]
    shipFrom: typing.Optional[ShipType] = jstruct.JStruct[ShipType]
    commodities: typing.Optional[typing.List[CommodityType]] = jstruct.JList[CommodityType]
    customs: typing.Optional[CustomsType] = jstruct.JStruct[CustomsType]
    currency: typing.Optional[str] = None
    orderTrackingReference: typing.Optional[int] = None
    freightCost: typing.Optional[ConsigneeChargesType] = jstruct.JStruct[ConsigneeChargesType]
    consigneeCharges: typing.Optional[ConsigneeChargesType] = jstruct.JStruct[ConsigneeChargesType]
    insuranceValue: typing.Optional[ConsigneeChargesType] = jstruct.JStruct[ConsigneeChargesType]
