import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AccountType:
    typeCode: typing.Optional[str] = None
    number: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class InvoiceType:
    number: typing.Optional[str] = None
    date: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CommodityCodeType:
    typeCode: typing.Optional[str] = None
    value: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class QuantityType:
    value: typing.Optional[int] = None
    unitOfMeasurement: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class WeightType:
    netValue: typing.Optional[float] = None
    grossValue: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class LineItemType:
    number: typing.Optional[int] = None
    description: typing.Optional[str] = None
    price: typing.Optional[int] = None
    quantity: typing.Optional[QuantityType] = jstruct.JStruct[QuantityType]
    commodityCodes: typing.Optional[typing.List[CommodityCodeType]] = jstruct.JList[CommodityCodeType]
    exportReasonType: typing.Optional[str] = None
    manufacturerCountry: typing.Optional[str] = None
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]


@attr.s(auto_attribs=True)
class ExportDeclarationType:
    lineItems: typing.Optional[typing.List[LineItemType]] = jstruct.JList[LineItemType]
    invoice: typing.Optional[InvoiceType] = jstruct.JStruct[InvoiceType]


@attr.s(auto_attribs=True)
class DimensionsType:
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PackageType:
    typeCode: typing.Optional[str] = None
    weight: typing.Optional[float] = None
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]


@attr.s(auto_attribs=True)
class ContentType:
    packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
    isCustomsDeclarable: typing.Optional[bool] = None
    declaredValue: typing.Optional[float] = None
    declaredValueCurrency: typing.Optional[str] = None
    exportDeclaration: typing.Optional[ExportDeclarationType] = jstruct.JStruct[ExportDeclarationType]
    description: typing.Optional[str] = None
    incoterm: typing.Optional[str] = None
    unitOfMeasurement: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ContactInformationType:
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    companyName: typing.Optional[str] = None
    fullName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PostalAddressType:
    postalCode: typing.Optional[int] = None
    cityName: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None
    addressLine1: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErDetailsType:
    postalAddress: typing.Optional[PostalAddressType] = jstruct.JStruct[PostalAddressType]
    contactInformation: typing.Optional[ContactInformationType] = jstruct.JStruct[ContactInformationType]
    typeCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomerDetailsType:
    shipperDetails: typing.Optional[ErDetailsType] = jstruct.JStruct[ErDetailsType]
    receiverDetails: typing.Optional[ErDetailsType] = jstruct.JStruct[ErDetailsType]


@attr.s(auto_attribs=True)
class ImageOptionType:
    typeCode: typing.Optional[str] = None
    templateName: typing.Optional[str] = None
    isRequested: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class OutputImagePropertiesType:
    printerDPI: typing.Optional[int] = None
    encodingFormat: typing.Optional[str] = None
    imageOptions: typing.Optional[typing.List[ImageOptionType]] = jstruct.JList[ImageOptionType]


@attr.s(auto_attribs=True)
class PickupType:
    isRequested: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    plannedShippingDateAndTime: typing.Optional[str] = None
    pickup: typing.Optional[PickupType] = jstruct.JStruct[PickupType]
    productCode: typing.Optional[str] = None
    localProductCode: typing.Optional[str] = None
    getRateEstimates: typing.Optional[bool] = None
    accounts: typing.Optional[typing.List[AccountType]] = jstruct.JList[AccountType]
    outputImageProperties: typing.Optional[OutputImagePropertiesType] = jstruct.JStruct[OutputImagePropertiesType]
    customerDetails: typing.Optional[CustomerDetailsType] = jstruct.JStruct[CustomerDetailsType]
    content: typing.Optional[ContentType] = jstruct.JStruct[ContentType]
