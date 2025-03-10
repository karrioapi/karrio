import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class HeaderType:
    CreateTimestamp: typing.Optional[str] = None
    Environment: typing.Optional[str] = None
    MessageIdentifier: typing.Optional[str] = None
    MessageSender: typing.Optional[str] = None
    DocumentType: typing.Optional[str] = None
    MessageVersion: typing.Optional[str] = None
    SourceSystemCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ContactType:
    Name: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PhysicalAddressType:
    AddressLine1: typing.Optional[str] = None
    AddressLine2: typing.Optional[str] = None
    AddressType: typing.Optional[str] = None
    CountryCode: typing.Optional[str] = None
    PostalCode: typing.Optional[int] = None
    StateCode: typing.Optional[str] = None
    Suburb: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ConsignPartyType:
    Contact: typing.Optional[ContactType] = jstruct.JStruct[ContactType]
    PartyName: typing.Optional[str] = None
    PhysicalAddress: typing.Optional[PhysicalAddressType] = jstruct.JStruct[PhysicalAddressType]


@attr.s(auto_attribs=True)
class PDFSettingsType:
    StartQuadrant: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PDFType:
    IsPDFA4: typing.Optional[bool] = None
    PDFSettings: typing.Optional[PDFSettingsType] = jstruct.JStruct[PDFSettingsType]


@attr.s(auto_attribs=True)
class PrintSettingsType:
    IsLabelThermal: typing.Optional[bool] = None
    IsZPLRawResponseRequired: typing.Optional[bool] = None
    PDF: typing.Optional[PDFType] = jstruct.JStruct[PDFType]


@attr.s(auto_attribs=True)
class BillToPartyType:
    AccountCode: typing.Optional[int] = None
    Payer: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DatePeriodType:
    DateTime: typing.Optional[str] = None
    DateType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DatePeriodCollectionType:
    DatePeriod: typing.Optional[typing.List[DatePeriodType]] = jstruct.JList[DatePeriodType]


@attr.s(auto_attribs=True)
class ReferenceType:
    ReferenceType: typing.Optional[str] = None
    ReferenceValue: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReferencesType:
    Reference: typing.Optional[typing.List[ReferenceType]] = jstruct.JList[ReferenceType]


@attr.s(auto_attribs=True)
class CommodityType:
    CommodityCode: typing.Optional[str] = None
    CommodityDescription: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DimensionsType:
    Height: typing.Optional[float] = None
    HeightUOM: typing.Optional[str] = None
    Length: typing.Optional[float] = None
    LengthUOM: typing.Optional[str] = None
    Volume: typing.Optional[float] = None
    VolumeUOM: typing.Optional[str] = None
    Weight: typing.Optional[float] = None
    WeightUOM: typing.Optional[str] = None
    Width: typing.Optional[float] = None
    WidthUOM: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class IDType:
    SchemeName: typing.Optional[str] = None
    Value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class IDsType:
    ID: typing.Optional[typing.List[IDType]] = jstruct.JList[IDType]


@attr.s(auto_attribs=True)
class ShipmentItemTotalsType:
    ShipmentItemCount: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ShipmentServiceType:
    ServiceCode: typing.Optional[str] = None
    ShipmentProductCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentItemType:
    Commodity: typing.Optional[CommodityType] = jstruct.JStruct[CommodityType]
    Description: typing.Optional[str] = None
    Dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    IDs: typing.Optional[IDsType] = jstruct.JStruct[IDsType]
    ShipmentItemTotals: typing.Optional[ShipmentItemTotalsType] = jstruct.JStruct[ShipmentItemTotalsType]
    ShipmentService: typing.Optional[ShipmentServiceType] = jstruct.JStruct[ShipmentServiceType]


@attr.s(auto_attribs=True)
class ShipmentItemCollectionType:
    ShipmentItem: typing.Optional[typing.List[ShipmentItemType]] = jstruct.JList[ShipmentItemType]


@attr.s(auto_attribs=True)
class ShipmentType:
    BillToParty: typing.Optional[BillToPartyType] = jstruct.JStruct[BillToPartyType]
    ConsigneeParty: typing.Optional[ConsignPartyType] = jstruct.JStruct[ConsignPartyType]
    CreateDateTime: typing.Optional[str] = None
    DatePeriodCollection: typing.Optional[DatePeriodCollectionType] = jstruct.JStruct[DatePeriodCollectionType]
    FreightMode: typing.Optional[str] = None
    References: typing.Optional[ReferencesType] = jstruct.JStruct[ReferencesType]
    ShipmentID: typing.Optional[str] = None
    ShipmentItemCollection: typing.Optional[ShipmentItemCollectionType] = jstruct.JStruct[ShipmentItemCollectionType]
    SpecialInstruction: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentCollectionType:
    Shipment: typing.Optional[typing.List[ShipmentType]] = jstruct.JList[ShipmentType]


@attr.s(auto_attribs=True)
class PrintType:
    BusinessID: typing.Optional[str] = None
    PrintSettings: typing.Optional[PrintSettingsType] = jstruct.JStruct[PrintSettingsType]
    PrintDocumentType: typing.Optional[str] = None
    ConsignorParty: typing.Optional[ConsignPartyType] = jstruct.JStruct[ConsignPartyType]
    CreateDateTime: typing.Optional[str] = None
    ShipmentCollection: typing.Optional[ShipmentCollectionType] = jstruct.JStruct[ShipmentCollectionType]


@attr.s(auto_attribs=True)
class TollMessageType:
    Header: typing.Optional[HeaderType] = jstruct.JStruct[HeaderType]
    Print: typing.Optional[PrintType] = jstruct.JStruct[PrintType]


@attr.s(auto_attribs=True)
class LabelRequestType:
    TollMessage: typing.Optional[TollMessageType] = jstruct.JStruct[TollMessageType]
