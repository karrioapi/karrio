import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ListOfResultCodeType:
    code: typing.Optional[str] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CarrierType:
    id: typing.Optional[str] = None
    name: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AddressType:
    title: typing.Optional[str] = None
    addressLine1: typing.Optional[str] = None
    addressLine2: typing.Optional[str] = None
    addressLine3: typing.Optional[str] = None
    addressLine4: typing.Optional[str] = None
    addressLine5: typing.Optional[str] = None
    addressLine6: typing.Optional[str] = None
    addressLine7: typing.Optional[str] = None
    addressLine8: typing.Optional[str] = None
    addressLine9: typing.Optional[str] = None
    addressLine10: typing.Optional[str] = None
    postcode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EntityType:
    title: typing.Optional[str] = None
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class HintType:
    type: typing.Optional[str] = None
    text: typing.Optional[str] = None
    line1: typing.Optional[str] = None
    line2: typing.Optional[str] = None
    line3: typing.Optional[str] = None
    line4: typing.Optional[str] = None
    line5: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class OriginType:
    line01: typing.Optional[str] = None
    line02: typing.Optional[str] = None
    line03: typing.Optional[str] = None
    line04: typing.Optional[str] = None
    line05: typing.Optional[str] = None
    line06: typing.Optional[str] = None
    line07: typing.Optional[str] = None
    line08: typing.Optional[str] = None
    line09: typing.Optional[str] = None
    line10: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ServiceDescriptionType:
    serviceDescriptionText: typing.Optional[str] = None
    serviceLogoRef: typing.Optional[str] = None
    servicePosition: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentLabelDataType:
    clientAddress: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    senderAddress: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    destinationAddress: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    carrier1: typing.Optional[CarrierType] = jstruct.JStruct[CarrierType]
    carrier2: typing.Optional[CarrierType] = jstruct.JStruct[CarrierType]
    origin: typing.Optional[OriginType] = jstruct.JStruct[OriginType]
    serviceDescriptions: typing.Optional[typing.List[ServiceDescriptionType]] = jstruct.JList[ServiceDescriptionType]
    entities: typing.Optional[typing.List[EntityType]] = jstruct.JList[EntityType]
    customerReference1: typing.Optional[str] = None
    customerReference2: typing.Optional[str] = None
    clientLogoRef: typing.Optional[str] = None
    hint: typing.Optional[HintType] = jstruct.JStruct[HintType]
    weightLogoRef: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    listOfResultCodes: typing.Optional[typing.List[ListOfResultCodeType]] = jstruct.JList[ListOfResultCodeType]
    shipmentID: typing.Optional[str] = None
    shipmentOrderID: typing.Optional[str] = None
    labelImage: typing.Optional[str] = None
    commInvoiceImage: typing.Optional[str] = None
    labelMediatype: typing.Optional[str] = None
    shipmentLabelData: typing.Optional[ShipmentLabelDataType] = jstruct.JStruct[ShipmentLabelDataType]
