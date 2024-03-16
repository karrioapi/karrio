from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class HeaderType:
    CreateTimestamp: Optional[str] = None
    Environment: Optional[str] = None
    MessageIdentifier: Optional[str] = None
    MessageSender: Optional[str] = None
    DocumentType: Optional[str] = None
    MessageVersion: Optional[str] = None
    SourceSystemCode: Optional[str] = None


@s(auto_attribs=True)
class ContactType:
    Name: Optional[str] = None


@s(auto_attribs=True)
class PhysicalAddressType:
    AddressLine1: Optional[str] = None
    AddressLine2: Optional[str] = None
    AddressType: Optional[str] = None
    CountryCode: Optional[str] = None
    PostalCode: Optional[int] = None
    StateCode: Optional[str] = None
    Suburb: Optional[str] = None


@s(auto_attribs=True)
class ConsignPartyType:
    Contact: Optional[ContactType] = JStruct[ContactType]
    PartyName: Optional[str] = None
    PhysicalAddress: Optional[PhysicalAddressType] = JStruct[PhysicalAddressType]


@s(auto_attribs=True)
class DatePeriodType:
    DateTime: Optional[str] = None
    DateType: Optional[str] = None


@s(auto_attribs=True)
class DatePeriodCollectionType:
    DatePeriod: List[DatePeriodType] = JList[DatePeriodType]


@s(auto_attribs=True)
class ManifestIDType:
    Value: Optional[str] = None


@s(auto_attribs=True)
class PDFSettingsType:
    StartQuadrant: Optional[int] = None


@s(auto_attribs=True)
class PDFType:
    IsPDFA4: Optional[bool] = None
    PDFSettings: Optional[PDFSettingsType] = JStruct[PDFSettingsType]


@s(auto_attribs=True)
class PrintSettingsType:
    IsLabelThermal: Optional[bool] = None
    IsZPLRawResponseRequired: Optional[bool] = None
    PDF: Optional[PDFType] = JStruct[PDFType]


@s(auto_attribs=True)
class BillToPartyType:
    AccountCode: Optional[int] = None
    Payer: Optional[str] = None


@s(auto_attribs=True)
class ReferenceType:
    ReferenceType: Optional[str] = None
    ReferenceValue: Optional[str] = None


@s(auto_attribs=True)
class ReferencesType:
    Reference: List[ReferenceType] = JList[ReferenceType]


@s(auto_attribs=True)
class CommodityType:
    CommodityCode: Optional[str] = None
    CommodityDescription: Optional[str] = None


@s(auto_attribs=True)
class DimensionsType:
    Height: Optional[int] = None
    HeightUOM: Optional[str] = None
    Length: Optional[int] = None
    LengthUOM: Optional[str] = None
    Volume: Optional[float] = None
    VolumeUOM: Optional[str] = None
    Weight: Optional[int] = None
    WeightUOM: Optional[str] = None
    Width: Optional[int] = None
    WidthUOM: Optional[str] = None


@s(auto_attribs=True)
class IDType:
    SchemeName: Optional[str] = None
    Value: Optional[str] = None


@s(auto_attribs=True)
class IDsType:
    ID: List[IDType] = JList[IDType]


@s(auto_attribs=True)
class ShipmentItemTotalsType:
    ShipmentItemCount: Optional[int] = None


@s(auto_attribs=True)
class ShipmentServiceType:
    ServiceCode: Optional[str] = None


@s(auto_attribs=True)
class ShipmentItemType:
    Commodity: Optional[CommodityType] = JStruct[CommodityType]
    Description: Optional[str] = None
    Dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    IDs: Optional[IDsType] = JStruct[IDsType]
    ShipmentItemTotals: Optional[ShipmentItemTotalsType] = JStruct[ShipmentItemTotalsType]
    ShipmentService: Optional[ShipmentServiceType] = JStruct[ShipmentServiceType]


@s(auto_attribs=True)
class ShipmentItemCollectionType:
    ShipmentItem: List[ShipmentItemType] = JList[ShipmentItemType]


@s(auto_attribs=True)
class ShipmentType:
    BillToParty: Optional[BillToPartyType] = JStruct[BillToPartyType]
    ConsigneeParty: Optional[ConsignPartyType] = JStruct[ConsignPartyType]
    CreateDateTime: Optional[str] = None
    DatePeriodCollection: Optional[DatePeriodCollectionType] = JStruct[DatePeriodCollectionType]
    FreightMode: Optional[str] = None
    References: Optional[ReferencesType] = JStruct[ReferencesType]
    ShipmentID: Optional[str] = None
    ShipmentItemCollection: Optional[ShipmentItemCollectionType] = JStruct[ShipmentItemCollectionType]
    SpecialInstruction: Optional[str] = None


@s(auto_attribs=True)
class ShipmentCollectionType:
    Shipment: List[ShipmentType] = JList[ShipmentType]


@s(auto_attribs=True)
class PrintType:
    BusinessID: Optional[str] = None
    PrintSettings: Optional[PrintSettingsType] = JStruct[PrintSettingsType]
    PrintDocumentType: Optional[str] = None
    ConsignorParty: Optional[ConsignPartyType] = JStruct[ConsignPartyType]
    ManifestID: Optional[ManifestIDType] = JStruct[ManifestIDType]
    CreateDateTime: Optional[str] = None
    DatePeriodCollection: Optional[DatePeriodCollectionType] = JStruct[DatePeriodCollectionType]
    ShipmentCollection: Optional[ShipmentCollectionType] = JStruct[ShipmentCollectionType]


@s(auto_attribs=True)
class TollMessageType:
    Header: Optional[HeaderType] = JStruct[HeaderType]
    Print: Optional[PrintType] = JStruct[PrintType]


@s(auto_attribs=True)
class ManifestRequestType:
    TollMessage: Optional[TollMessageType] = JStruct[TollMessageType]
