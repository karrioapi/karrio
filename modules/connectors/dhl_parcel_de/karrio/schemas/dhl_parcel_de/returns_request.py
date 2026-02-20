import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ContactAddressType:
    name1: typing.Optional[str] = None
    name2: typing.Optional[str] = None
    name3: typing.Optional[str] = None
    addressStreet: typing.Optional[str] = None
    addressHouse: typing.Optional[str] = None
    postalCode: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class WeightType:
    uom: typing.Optional[str] = None
    value: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class ValueType:
    currency: typing.Optional[str] = None
    value: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class CommodityType:
    itemDescription: typing.Optional[str] = None
    packagedQuantity: typing.Optional[int] = None
    countryOfOrigin: typing.Optional[str] = None
    hsCode: typing.Optional[str] = None
    itemWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    itemValue: typing.Optional[ValueType] = jstruct.JStruct[ValueType]


@attr.s(auto_attribs=True)
class CustomsDetailsType:
    items: typing.Optional[typing.List[CommodityType]] = jstruct.JList[CommodityType]


@attr.s(auto_attribs=True)
class VASType:
    goGreenPlus: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class ReturnOrderType:
    receiverId: typing.Optional[str] = None
    customerReference: typing.Optional[str] = None
    shipmentReference: typing.Optional[str] = None
    creationSoftware: typing.Optional[str] = None
    shipper: typing.Optional[ContactAddressType] = jstruct.JStruct[ContactAddressType]
    itemWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    itemValue: typing.Optional[ValueType] = jstruct.JStruct[ValueType]
    customsDetails: typing.Optional[CustomsDetailsType] = jstruct.JStruct[CustomsDetailsType]
    services: typing.Optional[VASType] = jstruct.JStruct[VASType]
