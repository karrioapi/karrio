from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AddressType:
    AddressType: Optional[str] = None
    Area: Optional[str] = None
    Buildingname: Optional[str] = None
    City: Optional[str] = None
    CompanyName: Optional[str] = None
    Countrycode: Optional[str] = None
    Department: Optional[str] = None
    Doorcode: Optional[int] = None
    FirstName: Optional[str] = None
    Floor: Optional[int] = None
    HouseNr: Optional[int] = None
    HouseNrExt: Optional[str] = None
    Name: Optional[str] = None
    Region: Optional[str] = None
    Street: Optional[str] = None
    StreetHouseNrExt: Optional[str] = None
    Zipcode: Optional[str] = None


@s(auto_attribs=True)
class CustomerType:
    Address: Optional[AddressType] = JStruct[AddressType]
    CollectionLocation: Optional[int] = None
    ContactPerson: Optional[str] = None
    CustomerCode: Optional[str] = None
    CustomerNumber: Optional[int] = None
    Email: Optional[str] = None
    Name: Optional[str] = None


@s(auto_attribs=True)
class MessageType:
    MessageID: Optional[str] = None
    MessageTimeStamp: Optional[str] = None
    Printertype: Optional[str] = None


@s(auto_attribs=True)
class AmountType:
    AmountType: Optional[str] = None
    AccountName: Optional[str] = None
    BIC: Optional[str] = None
    Currency: Optional[str] = None
    IBAN: Optional[str] = None
    Reference: Optional[str] = None
    TransactionNumber: Optional[str] = None
    Value: Optional[int] = None


@s(auto_attribs=True)
class ContactType:
    ContactType: Optional[str] = None
    Email: Optional[str] = None
    SMSNr: Optional[str] = None
    TelNr: Optional[str] = None


@s(auto_attribs=True)
class ContentType:
    Description: Optional[str] = None
    Quantity: Optional[int] = None
    Weight: Optional[int] = None
    Value: Optional[int] = None
    HSTariffNr: Optional[int] = None
    CountryOfOrigin: Optional[str] = None


@s(auto_attribs=True)
class CustomType:
    Certificate: Optional[str] = None
    CertificateNr: Optional[str] = None
    License: Optional[str] = None
    LicenseNr: Optional[str] = None
    Invoice: Optional[str] = None
    InvoiceNr: Optional[str] = None
    HandleAsNonDeliverable: Optional[bool] = None
    Currency: Optional[str] = None
    ShipmentType: Optional[str] = None
    TrustedShipperID: Optional[str] = None
    ImporterReferenceCode: Optional[str] = None
    TransactionCode: Optional[str] = None
    TransactionDescription: Optional[str] = None
    Content: List[ContentType] = JList[ContentType]


@s(auto_attribs=True)
class DimensionType:
    Height: Optional[int] = None
    Length: Optional[int] = None
    Volume: Optional[int] = None
    Weight: Optional[int] = None
    Width: Optional[int] = None


@s(auto_attribs=True)
class ExtraFieldType:
    Key: Optional[str] = None
    Value: Optional[str] = None


@s(auto_attribs=True)
class GroupType:
    GroupType: Optional[str] = None
    GroupSequence: Optional[str] = None
    GroupCount: Optional[int] = None
    MainBarcode: Optional[str] = None


@s(auto_attribs=True)
class HazardousMaterialType:
    ToxicSubstanceCode: Optional[str] = None
    AdditionalToxicSubstanceCode: List[str] = []
    ADRPoints: Optional[str] = None
    TunnelCode: Optional[str] = None
    PackagingGroupCode: Optional[str] = None
    PackagingGroupDescription: Optional[str] = None
    GrossWeight: Optional[str] = None
    UNDGNumber: Optional[str] = None
    TransportCategoryCode: Optional[str] = None
    ChemicalTechnicalDescription: Optional[str] = None


@s(auto_attribs=True)
class ProductOptionType:
    Characteristic: Optional[str] = None
    Option: Optional[str] = None


@s(auto_attribs=True)
class ShipmentType:
    Addresses: List[AddressType] = JList[AddressType]
    Amounts: List[AmountType] = JList[AmountType]
    Barcode: Optional[str] = None
    CodingText: Optional[str] = None
    CollectionTimeStampStart: Optional[str] = None
    CollectionTimeStampEnd: Optional[str] = None
    Contacts: List[ContactType] = JList[ContactType]
    Content: Optional[str] = None
    CostCenter: Optional[str] = None
    CustomerOrderNumber: Optional[str] = None
    Customs: List[CustomType] = JList[CustomType]
    DeliveryAddress: Optional[str] = None
    DeliveryDate: Optional[str] = None
    Dimension: Optional[DimensionType] = JStruct[DimensionType]
    DownPartnerBarcode: Optional[str] = None
    DownPartnerID: Optional[str] = None
    DownPartnerLocation: Optional[str] = None
    Groups: List[GroupType] = JList[GroupType]
    HazardousMaterial: List[HazardousMaterialType] = JList[HazardousMaterialType]
    ProductCodeCollect: Optional[int] = None
    ProductCodeDelivery: Optional[int] = None
    ProductOptions: List[ProductOptionType] = JList[ProductOptionType]
    ReceiverDateOfBirth: Optional[str] = None
    Reference: Optional[str] = None
    ReferenceCollect: Optional[str] = None
    Remark: Optional[str] = None
    ReturnBarcode: Optional[str] = None
    ReturnReference: Optional[str] = None
    TimeslotID: Optional[str] = None
    ExtraFields: List[ExtraFieldType] = JList[ExtraFieldType]


@s(auto_attribs=True)
class ShipmentRequestType:
    Customer: Optional[CustomerType] = JStruct[CustomerType]
    LabelSignature: Optional[str] = None
    Message: Optional[MessageType] = JStruct[MessageType]
    Shipments: List[ShipmentType] = JList[ShipmentType]
