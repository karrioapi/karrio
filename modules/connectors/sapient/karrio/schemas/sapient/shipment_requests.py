import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ServiceEnhancementType:
    Code: typing.Optional[str] = None
    SafeplaceLocation: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CarrierSpecificsType:
    ServiceLevel: typing.Optional[str] = None
    EbayVtn: typing.Optional[str] = None
    ServiceEnhancements: typing.Optional[typing.List[ServiceEnhancementType]] = jstruct.JList[ServiceEnhancementType]


@attr.s(auto_attribs=True)
class CustomsType:
    ReasonForExport: typing.Optional[str] = None
    Incoterms: typing.Optional[str] = None
    PreRegistrationNumber: typing.Optional[str] = None
    PreRegistrationType: typing.Optional[str] = None
    ShippingCharges: typing.Optional[float] = None
    OtherCharges: typing.Optional[int] = None
    QuotedLandedCost: typing.Optional[float] = None
    InvoiceNumber: typing.Optional[str] = None
    InvoiceDate: typing.Optional[str] = None
    ExportLicenceRequired: typing.Optional[bool] = None
    Airn: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AddressType:
    ContactName: typing.Optional[str] = None
    CompanyName: typing.Optional[str] = None
    ContactEmail: typing.Optional[str] = None
    ContactPhone: typing.Optional[str] = None
    Line1: typing.Optional[str] = None
    Line2: typing.Optional[str] = None
    Line3: typing.Optional[str] = None
    Town: typing.Optional[str] = None
    Postcode: typing.Optional[str] = None
    County: typing.Optional[str] = None
    CountryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DestinationType:
    Address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    EoriNumber: typing.Optional[str] = None
    VatNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ItemType:
    SkuCode: typing.Optional[str] = None
    PackageOccurrence: typing.Optional[int] = None
    Quantity: typing.Optional[int] = None
    Description: typing.Optional[str] = None
    Value: typing.Optional[float] = None
    Weight: typing.Optional[float] = None
    HSCode: typing.Optional[str] = None
    CountryOfOrigin: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DimensionsType:
    Length: typing.Optional[int] = None
    Width: typing.Optional[int] = None
    Height: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PackageType:
    PackageType: typing.Optional[str] = None
    PackageOccurrence: typing.Optional[int] = None
    DeclaredWeight: typing.Optional[float] = None
    Dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    DeclaredValue: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class ReturnToSenderType:
    Address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]


@attr.s(auto_attribs=True)
class ShipmentInformationType:
    ContentType: typing.Optional[str] = None
    Action: typing.Optional[str] = None
    LabelFormat: typing.Optional[str] = None
    ServiceCode: typing.Optional[str] = None
    DescriptionOfGoods: typing.Optional[str] = None
    ShipmentDate: typing.Optional[str] = None
    CurrencyCode: typing.Optional[str] = None
    WeightUnitOfMeasure: typing.Optional[str] = None
    DimensionsUnitOfMeasure: typing.Optional[str] = None
    ContainerId: typing.Optional[str] = None
    DeclaredWeight: typing.Optional[float] = None
    BusinessTransactionType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipperType:
    Address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    ShippingAccountId: typing.Optional[str] = None
    ShippingLocationId: typing.Optional[str] = None
    Reference1: typing.Optional[str] = None
    DepartmentNumber: typing.Optional[str] = None
    EoriNumber: typing.Optional[str] = None
    VatNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    ShipmentInformation: typing.Optional[ShipmentInformationType] = jstruct.JStruct[ShipmentInformationType]
    Shipper: typing.Optional[ShipperType] = jstruct.JStruct[ShipperType]
    Destination: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    CarrierSpecifics: typing.Optional[CarrierSpecificsType] = jstruct.JStruct[CarrierSpecificsType]
    ReturnToSender: typing.Optional[ReturnToSenderType] = jstruct.JStruct[ReturnToSenderType]
    Packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
    Items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]
    Customs: typing.Optional[CustomsType] = jstruct.JStruct[CustomsType]
