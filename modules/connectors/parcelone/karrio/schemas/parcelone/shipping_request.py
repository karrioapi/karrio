import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class CepSpecialType:
    Key: typing.Optional[str] = None
    Value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class FormatType:
    Type: typing.Optional[str] = None
    Size: typing.Optional[str] = None
    Unit: typing.Optional[str] = None
    Orientation: typing.Optional[int] = None
    Height: typing.Optional[str] = None
    Width: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class MaxChargesType:
    Currency: typing.Optional[str] = None
    Value: typing.Optional[str] = None
    Description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomDetailType:
    Contents: typing.Optional[str] = None
    Quantity: typing.Optional[int] = None
    NetWeightPerItem: typing.Optional[float] = None
    NetWeight: typing.Optional[float] = None
    ItemValuePerItem: typing.Optional[float] = None
    ItemValue: typing.Optional[float] = None
    TariffNumber: typing.Optional[int] = None
    Origin: typing.Optional[str] = None
    AdditionalInfo: typing.Optional[typing.List[CepSpecialType]] = jstruct.JList[CepSpecialType]


@attr.s(auto_attribs=True)
class IntDocDataType:
    PrintInternationalDocuments: typing.Optional[int] = None
    InternationalDocumentFormat: typing.Optional[FormatType] = jstruct.JStruct[FormatType]
    ConsignerCustomsID: typing.Optional[int] = None
    ShipToRef: typing.Optional[str] = None
    CustomDetails: typing.Optional[typing.List[CustomDetailType]] = jstruct.JList[CustomDetailType]
    Postage: typing.Optional[float] = None
    TotalValue: typing.Optional[float] = None
    Currency: typing.Optional[str] = None
    TotalWeightkg: typing.Optional[float] = None
    ItemCategory: typing.Optional[int] = None
    Explanation: typing.Optional[str] = None
    OfficeOfOrigin: typing.Optional[str] = None
    Comments: typing.Optional[str] = None
    Date: typing.Optional[str] = None
    License: typing.Optional[int] = None
    LicenseNo: typing.Optional[str] = None
    Certificate: typing.Optional[int] = None
    CertificateNo: typing.Optional[str] = None
    Invoice: typing.Optional[int] = None
    InvoiceNo: typing.Optional[str] = None
    NonDeliveryInstruction: typing.Optional[str] = None
    ServiceLevel: typing.Optional[str] = None
    ValidatedForExport: typing.Optional[str] = None
    AdditionalInfo: typing.Optional[typing.List[CepSpecialType]] = jstruct.JList[CepSpecialType]


@attr.s(auto_attribs=True)
class PackageDimensionsType:
    Measurement: typing.Optional[str] = None
    Length: typing.Optional[str] = None
    Width: typing.Optional[str] = None
    Height: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageVolumeClassType:
    Unit: typing.Optional[str] = None
    Value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ServiceType:
    ServiceID: typing.Optional[str] = None
    Value: typing.Optional[MaxChargesType] = jstruct.JStruct[MaxChargesType]
    Parameters: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageType:
    PackageID: typing.Optional[str] = None
    PackageRef: typing.Optional[str] = None
    PackageTrackingID: typing.Optional[str] = None
    PackageType: typing.Optional[str] = None
    PackageWeight: typing.Optional[PackageVolumeClassType] = jstruct.JStruct[PackageVolumeClassType]
    PackageDimensions: typing.Optional[PackageDimensionsType] = jstruct.JStruct[PackageDimensionsType]
    PackageVolume: typing.Optional[PackageVolumeClassType] = jstruct.JStruct[PackageVolumeClassType]
    Services: typing.Optional[typing.List[ServiceType]] = jstruct.JList[ServiceType]
    IntDocData: typing.Optional[IntDocDataType] = jstruct.JStruct[IntDocDataType]
    Remarks: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BankAccountType:
    BankCode: typing.Optional[str] = None
    Bank: typing.Optional[str] = None
    AccountOwner: typing.Optional[str] = None
    AccountNumber: typing.Optional[str] = None
    Iban: typing.Optional[str] = None
    Bic: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentAddressType:
    Street: typing.Optional[str] = None
    Streetno: typing.Optional[int] = None
    PostalCode: typing.Optional[int] = None
    City: typing.Optional[str] = None
    District: typing.Optional[str] = None
    State: typing.Optional[str] = None
    Country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentContactType:
    Email: typing.Optional[str] = None
    Phone: typing.Optional[str] = None
    Mobile: typing.Optional[str] = None
    Fax: typing.Optional[str] = None
    Company: typing.Optional[str] = None
    ContactPerson: typing.Optional[str] = None
    AttentionName: typing.Optional[str] = None
    Salutation: typing.Optional[str] = None
    FirstName: typing.Optional[str] = None
    LastName: typing.Optional[str] = None
    BirthDate: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipFromDataType:
    Reference: typing.Optional[str] = None
    Name1: typing.Optional[str] = None
    Name2: typing.Optional[str] = None
    Name3: typing.Optional[str] = None
    ShipmentAddress: typing.Optional[ShipmentAddressType] = jstruct.JStruct[ShipmentAddressType]
    ShipmentContact: typing.Optional[ShipmentContactType] = jstruct.JStruct[ShipmentContactType]
    SalesTaxID: typing.Optional[str] = None
    CustomsID: typing.Optional[str] = None
    BankAccount: typing.Optional[BankAccountType] = jstruct.JStruct[BankAccountType]


@attr.s(auto_attribs=True)
class ShipToDataType:
    Reference: typing.Optional[str] = None
    Name1: typing.Optional[str] = None
    Name2: typing.Optional[str] = None
    Name3: typing.Optional[str] = None
    ShipmentAddress: typing.Optional[ShipmentAddressType] = jstruct.JStruct[ShipmentAddressType]
    PrivateAddressIndicator: typing.Optional[int] = None
    ShipmentContact: typing.Optional[ShipmentContactType] = jstruct.JStruct[ShipmentContactType]
    SalesTaxID: typing.Optional[str] = None
    CustomsID: typing.Optional[str] = None
    BranchID: typing.Optional[str] = None
    CEPCustID: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingDataType:
    ShipmentID: typing.Optional[str] = None
    ShipmentRef: typing.Optional[str] = None
    TrackingID: typing.Optional[str] = None
    CEPID: typing.Optional[str] = None
    ProductID: typing.Optional[str] = None
    CustomerID: typing.Optional[str] = None
    MandatorID: typing.Optional[int] = None
    ConsignerID: typing.Optional[int] = None
    ShipToData: typing.Optional[ShipToDataType] = jstruct.JStruct[ShipToDataType]
    ShipFromData: typing.Optional[ShipFromDataType] = jstruct.JStruct[ShipFromDataType]
    ReturnShipmentIndicator: typing.Optional[int] = None
    PrintLabel: typing.Optional[int] = None
    LabelFormat: typing.Optional[FormatType] = jstruct.JStruct[FormatType]
    PrintDocuments: typing.Optional[int] = None
    ReturnCharges: typing.Optional[int] = None
    MaxCharges: typing.Optional[MaxChargesType] = jstruct.JStruct[MaxChargesType]
    DocumentFormat: typing.Optional[FormatType] = jstruct.JStruct[FormatType]
    Software: typing.Optional[str] = None
    Packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
    Services: typing.Optional[typing.List[ServiceType]] = jstruct.JList[ServiceType]
    CEPSpecials: typing.Optional[typing.List[CepSpecialType]] = jstruct.JList[CepSpecialType]
    CostCenter: typing.Optional[str] = None
    Other1: typing.Optional[str] = None
    Other2: typing.Optional[str] = None
    Other3: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingRequestType:
    ShippingData: typing.Optional[ShippingDataType] = jstruct.JStruct[ShippingDataType]
