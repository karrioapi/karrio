from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Address:
    Name1: Optional[str] = None
    Name2: Optional[str] = None
    Name3: Optional[str] = None
    CountryCode: Optional[str] = None
    ZIPCode: Optional[int] = None
    City: Optional[str] = None
    Street: Optional[str] = None
    StreetNumber: Optional[str] = None
    eMail: Optional[str] = None
    ContactPerson: Optional[str] = None
    MobilePhoneNumber: Optional[str] = None
    FixedLinePhonenumber: Optional[str] = None


@s(auto_attribs=True)
class Consignee:
    ConsigneeID: Optional[str] = None
    CostCenter: Optional[str] = None
    Category: Optional[str] = None
    Address: Optional[Address] = JStruct[Address]


@s(auto_attribs=True)
class CustomContent:
    CustomerLogo: Optional[str] = None
    Barcode: Optional[str] = None
    BarcodeType: Optional[str] = None
    HideShipperAddress: Optional[bool] = None


@s(auto_attribs=True)
class DefinePrinter:
    LabelPrinter: Optional[str] = None
    DocumentPrinter: Optional[str] = None


@s(auto_attribs=True)
class ReturnLabels:
    TemplateSet: Optional[str] = None
    LabelFormat: Optional[str] = None


@s(auto_attribs=True)
class PrintingOptions:
    UseDefault: Optional[str] = None
    DefinePrinter: Optional[DefinePrinter] = JStruct[DefinePrinter]
    ReturnLabels: Optional[ReturnLabels] = JStruct[ReturnLabels]


@s(auto_attribs=True)
class AddonLiability:
    ServiceName: Optional[str] = None
    Amount: Optional[str] = None
    Currency: Optional[str] = None
    ParcelContent: Optional[str] = None
    Reason: Optional[str] = None


@s(auto_attribs=True)
class Service:
    Cash: Optional[AddonLiability] = JStruct[AddonLiability]
    AddonLiability: Optional[AddonLiability] = JStruct[AddonLiability]


@s(auto_attribs=True)
class ShipmentUnit:
    Weight: Optional[int] = None
    Note1: Optional[str] = None
    Note2: Optional[str] = None
    FRAlphaParcelReference: Optional[str] = None
    TrackID: Optional[str] = None
    ParcelNumber: Optional[str] = None
    Service: List[Service] = JList[Service]


@s(auto_attribs=True)
class Shipper:
    ContactID: Optional[str] = None
    FRAlphaCustomerReference: Optional[str] = None
    AlternativeShipperAddress: Optional[Address] = JStruct[Address]


@s(auto_attribs=True)
class Shipment:
    ShipmentReference: List[str] = JList[str]
    ShippingDate: Optional[str] = None
    IncotermCode: Optional[int] = None
    Identifier: Optional[str] = None
    Middleware: Optional[str] = None
    Product: Optional[str] = None
    ExpressAltDeliveryAllowed: Optional[bool] = None
    Consignee: Optional[Consignee] = JStruct[Consignee]
    Shipper: Optional[Shipper] = JStruct[Shipper]
    ShipmentUnit: List[ShipmentUnit] = JList[ShipmentUnit]
    PrintingOptions: Optional[PrintingOptions] = JStruct[PrintingOptions]
    CustomContent: Optional[CustomContent] = JStruct[CustomContent]


@s(auto_attribs=True)
class ShipmentRequest:
    Shipment: Optional[Shipment] = JStruct[Shipment]
