"""ParcelOne Shipping REST API v1 - Request Types."""

import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AddressType:
    """Address data format."""

    Street: typing.Optional[str] = None
    Streetno: typing.Optional[str] = None
    PostalCode: typing.Optional[str] = None
    City: typing.Optional[str] = None
    District: typing.Optional[str] = None
    State: typing.Optional[str] = None
    Country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ContactType:
    """Contact information."""

    Email: typing.Optional[str] = None
    Phone: typing.Optional[str] = None
    Mobile: typing.Optional[str] = None
    Fax: typing.Optional[str] = None
    AttentionName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipToType:
    """Recipient/consignee address data."""

    Name1: typing.Optional[str] = None
    Name2: typing.Optional[str] = None
    Name3: typing.Optional[str] = None
    Reference: typing.Optional[str] = None
    ShipmentAddress: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    ShipmentContact: typing.Optional[ContactType] = jstruct.JStruct[ContactType]
    PrivateAddressIndicator: typing.Optional[int] = None
    SalesTaxID: typing.Optional[str] = None
    CustomsID: typing.Optional[str] = None
    BranchID: typing.Optional[str] = None
    CEPCustID: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipFromType:
    """Consigner/sender address data."""

    Name1: typing.Optional[str] = None
    Name2: typing.Optional[str] = None
    Name3: typing.Optional[str] = None
    Reference: typing.Optional[str] = None
    ShipmentAddress: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    ShipmentContact: typing.Optional[ContactType] = jstruct.JStruct[ContactType]
    SalesTaxID: typing.Optional[str] = None
    CustomsID: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class FormatType:
    """Document format specification."""

    Type: typing.Optional[str] = None
    Size: typing.Optional[str] = None
    Unit: typing.Optional[str] = None
    Orientation: typing.Optional[int] = None
    Height: typing.Optional[str] = None
    Width: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class MeasurementType:
    """Weight or volume measurement."""

    Unit: typing.Optional[str] = None
    Value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DimensionsType:
    """Package dimensions."""

    Length: typing.Optional[str] = None
    Width: typing.Optional[str] = None
    Height: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AmountType:
    """Monetary amount."""

    Currency: typing.Optional[str] = None
    Value: typing.Optional[str] = None
    Description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentServiceType:
    """Service for shipment or package."""

    ServiceID: typing.Optional[str] = None
    Value: typing.Optional[AmountType] = jstruct.JStruct[AmountType]
    Parameters: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomDetailType:
    """Customs detail line item."""

    Contents: typing.Optional[str] = None
    ItemValue: typing.Optional[float] = None
    ItemValuePerItem: typing.Optional[float] = None
    NetWeight: typing.Optional[float] = None
    NetWeightPerItem: typing.Optional[float] = None
    Origin: typing.Optional[str] = None
    Quantity: typing.Optional[int] = None
    TariffNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class InternationalDocFormatType:
    """International document format."""

    Type: typing.Optional[str] = None
    Size: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class IntDocDataType:
    """International/customs documentation data."""

    ConsignerCustomsID: typing.Optional[str] = None
    Invoice: typing.Optional[int] = None
    InvoiceNo: typing.Optional[str] = None
    PrintInternationalDocuments: typing.Optional[int] = None
    InternationalDocumentFormat: typing.Optional[InternationalDocFormatType] = jstruct.JStruct[InternationalDocFormatType]
    ShipToRef: typing.Optional[str] = None
    TotalWeightkg: typing.Optional[float] = None
    Postage: typing.Optional[float] = None
    ItemCategory: typing.Optional[int] = None
    CustomDetails: typing.Optional[typing.List[CustomDetailType]] = jstruct.JList[CustomDetailType]


@attr.s(auto_attribs=True)
class ShipmentPackageType:
    """Package within a shipment."""

    PackageRef: typing.Optional[str] = None
    PackageType: typing.Optional[str] = None
    PackageWeight: typing.Optional[MeasurementType] = jstruct.JStruct[MeasurementType]
    PackageDimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    PackageVolume: typing.Optional[MeasurementType] = jstruct.JStruct[MeasurementType]
    Services: typing.Optional[typing.List[ShipmentServiceType]] = jstruct.JList[ShipmentServiceType]
    IntDocData: typing.Optional[IntDocDataType] = jstruct.JStruct[IntDocDataType]
    Remarks: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CEPSpecialType:
    """CEP-specific special options."""

    Key: typing.Optional[str] = None
    Value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentType:
    """Complete shipment registration request."""

    ShipmentRef: typing.Optional[str] = None
    CEPID: typing.Optional[str] = None
    ProductID: typing.Optional[str] = None
    MandatorID: typing.Optional[str] = None
    ConsignerID: typing.Optional[str] = None
    ShipToData: typing.Optional[ShipToType] = jstruct.JStruct[ShipToType]
    ShipFromData: typing.Optional[ShipFromType] = jstruct.JStruct[ShipFromType]
    ReturnShipmentIndicator: typing.Optional[int] = None
    PrintLabel: typing.Optional[int] = None
    LabelFormat: typing.Optional[FormatType] = jstruct.JStruct[FormatType]
    PrintDocuments: typing.Optional[int] = None
    DocumentFormat: typing.Optional[FormatType] = jstruct.JStruct[FormatType]
    ReturnCharges: typing.Optional[int] = None
    MaxCharges: typing.Optional[AmountType] = jstruct.JStruct[AmountType]
    Software: typing.Optional[str] = None
    Packages: typing.Optional[typing.List[ShipmentPackageType]] = jstruct.JList[ShipmentPackageType]
    Services: typing.Optional[typing.List[ShipmentServiceType]] = jstruct.JList[ShipmentServiceType]
    CEPSpecials: typing.Optional[typing.List[CEPSpecialType]] = jstruct.JList[CEPSpecialType]
    CostCenter: typing.Optional[str] = None
    Other1: typing.Optional[str] = None
    Other2: typing.Optional[str] = None
    Other3: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingDataRequestType:
    """Root shipping data request wrapper."""

    ShippingData: typing.Optional[ShipmentType] = jstruct.JStruct[ShipmentType]
