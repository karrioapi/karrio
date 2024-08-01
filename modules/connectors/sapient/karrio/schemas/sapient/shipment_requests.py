from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class ServiceEnhancementType:
    Code: Optional[str] = None
    SafeplaceLocation: Optional[str] = None


@s(auto_attribs=True)
class CarrierSpecificsType:
    ServiceLevel: Optional[str] = None
    EbayVtn: Optional[str] = None
    ServiceEnhancements: List[ServiceEnhancementType] = JList[ServiceEnhancementType]


@s(auto_attribs=True)
class CustomsType:
    ReasonForExport: Optional[str] = None
    Incoterms: Optional[str] = None
    PreRegistrationNumber: Optional[str] = None
    PreRegistrationType: Optional[str] = None
    ShippingCharges: Optional[float] = None
    OtherCharges: Optional[int] = None
    QuotedLandedCost: Optional[float] = None
    InvoiceNumber: Optional[str] = None
    InvoiceDate: Optional[str] = None
    ExportLicenceRequired: Optional[bool] = None
    Airn: Optional[str] = None


@s(auto_attribs=True)
class AddressType:
    ContactName: Optional[str] = None
    CompanyName: Optional[str] = None
    ContactEmail: Optional[str] = None
    ContactPhone: Optional[str] = None
    Line1: Optional[str] = None
    Line2: Optional[str] = None
    Line3: Optional[str] = None
    Town: Optional[str] = None
    Postcode: Optional[str] = None
    County: Optional[str] = None
    CountryCode: Optional[str] = None


@s(auto_attribs=True)
class DestinationType:
    Address: Optional[AddressType] = JStruct[AddressType]
    EoriNumber: Optional[str] = None
    VatNumber: Optional[str] = None


@s(auto_attribs=True)
class ItemType:
    SkuCode: Optional[str] = None
    PackageOccurrence: Optional[int] = None
    Quantity: Optional[int] = None
    Description: Optional[str] = None
    Value: Optional[float] = None
    Weight: Optional[float] = None
    HSCode: Optional[str] = None
    CountryOfOrigin: Optional[str] = None


@s(auto_attribs=True)
class DimensionsType:
    Length: Optional[int] = None
    Width: Optional[int] = None
    Height: Optional[int] = None


@s(auto_attribs=True)
class PackageType:
    PackageType: Optional[str] = None
    PackageOccurrence: Optional[int] = None
    DeclaredWeight: Optional[float] = None
    Dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    DeclaredValue: Optional[float] = None


@s(auto_attribs=True)
class ReturnToSenderType:
    Address: Optional[AddressType] = JStruct[AddressType]


@s(auto_attribs=True)
class ShipmentInformationType:
    ContentType: Optional[str] = None
    Action: Optional[str] = None
    LabelFormat: Optional[str] = None
    ServiceCode: Optional[str] = None
    DescriptionOfGoods: Optional[str] = None
    ShipmentDate: Optional[str] = None
    CurrencyCode: Optional[str] = None
    WeightUnitOfMeasure: Optional[str] = None
    DimensionsUnitOfMeasure: Optional[str] = None
    ContainerId: Optional[str] = None
    DeclaredWeight: Optional[float] = None
    BusinessTransactionType: Optional[str] = None


@s(auto_attribs=True)
class ShipperType:
    Address: Optional[AddressType] = JStruct[AddressType]
    ShippingAccountId: Optional[str] = None
    ShippingLocationId: Optional[str] = None
    Reference1: Optional[str] = None
    DepartmentNumber: Optional[str] = None
    EoriNumber: Optional[str] = None
    VatNumber: Optional[str] = None


@s(auto_attribs=True)
class ShipmentRequestType:
    ShipmentInformation: Optional[ShipmentInformationType] = JStruct[ShipmentInformationType]
    Shipper: Optional[ShipperType] = JStruct[ShipperType]
    Destination: Optional[DestinationType] = JStruct[DestinationType]
    CarrierSpecifics: Optional[CarrierSpecificsType] = JStruct[CarrierSpecificsType]
    ReturnToSender: Optional[ReturnToSenderType] = JStruct[ReturnToSenderType]
    Packages: List[PackageType] = JList[PackageType]
    Items: List[ItemType] = JList[ItemType]
    Customs: Optional[CustomsType] = JStruct[CustomsType]
