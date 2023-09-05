from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AddressType:
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
class ConsigneeType:
    ConsigneeID: Optional[str] = None
    CostCenter: Optional[str] = None
    Category: Optional[str] = None
    Address: Optional[AddressType] = JStruct[AddressType]


@s(auto_attribs=True)
class CustomContentType:
    CustomerLogo: Optional[str] = None
    Barcode: Optional[str] = None
    BarcodeType: Optional[str] = None
    HideShipperAddress: Optional[bool] = None


@s(auto_attribs=True)
class DefinePrinterType:
    LabelPrinter: Optional[str] = None
    DocumentPrinter: Optional[str] = None


@s(auto_attribs=True)
class ReturnLabelsType:
    TemplateSet: Optional[str] = None
    LabelFormat: Optional[str] = None


@s(auto_attribs=True)
class PrintingOptionsType:
    UseDefault: Optional[str] = None
    DefinePrinter: Optional[DefinePrinterType] = JStruct[DefinePrinterType]
    ReturnLabels: Optional[ReturnLabelsType] = JStruct[ReturnLabelsType]


@s(auto_attribs=True)
class AddonLiabilityType:
    ServiceName: Optional[str] = None
    Amount: Optional[str] = None
    Currency: Optional[str] = None
    ParcelContent: Optional[str] = None
    Reason: Optional[str] = None


@s(auto_attribs=True)
class ServiceType:
    Cash: Optional[AddonLiabilityType] = JStruct[AddonLiabilityType]
    AddonLiability: Optional[AddonLiabilityType] = JStruct[AddonLiabilityType]


@s(auto_attribs=True)
class ShipmentUnitType:
    Weight: Optional[int] = None
    Note1: Optional[str] = None
    Note2: Optional[str] = None
    FRAlphaParcelReference: Optional[str] = None
    TrackID: Optional[str] = None
    ParcelNumber: Optional[str] = None
    Service: List[ServiceType] = JList[ServiceType]


@s(auto_attribs=True)
class ShipperType:
    ContactID: Optional[str] = None
    FRAlphaCustomerReference: Optional[str] = None
    AlternativeShipperAddress: Optional[AddressType] = JStruct[AddressType]


@s(auto_attribs=True)
class ShipmentType:
    ShipmentReference: List[str] = []
    ShippingDate: Optional[str] = None
    IncotermCode: Optional[int] = None
    Identifier: Optional[str] = None
    Middleware: Optional[str] = None
    Product: Optional[str] = None
    ExpressAltDeliveryAllowed: Optional[bool] = None
    Consignee: Optional[ConsigneeType] = JStruct[ConsigneeType]
    Shipper: Optional[ShipperType] = JStruct[ShipperType]
    ShipmentUnit: List[ShipmentUnitType] = JList[ShipmentUnitType]
    PrintingOptions: Optional[PrintingOptionsType] = JStruct[PrintingOptionsType]
    CustomContent: Optional[CustomContentType] = JStruct[CustomContentType]


@s(auto_attribs=True)
class ShipmentRequestType:
    Shipment: Optional[ShipmentType] = JStruct[ShipmentType]
