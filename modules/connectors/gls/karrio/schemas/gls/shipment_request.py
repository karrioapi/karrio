import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class CustomContentType:
    CustomerLogo: typing.Optional[typing.List[str]] = None
    BarcodeContentType: typing.Optional[str] = None
    Barcode: typing.Optional[str] = None
    BarcodeType: typing.Optional[str] = None
    HideShipperAddress: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class DefinePrinterType:
    LabelPrinter: typing.Optional[str] = None
    DocumentPrinter: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReturnLabelsType:
    TemplateSet: typing.Optional[str] = None
    LabelFormat: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PrintingOptionsType:
    ReturnLabels: typing.Optional[ReturnLabelsType] = jstruct.JStruct[ReturnLabelsType]
    UseDefault: typing.Optional[str] = None
    DefinePrinter: typing.Optional[DefinePrinterType] = jstruct.JStruct[DefinePrinterType]


@attr.s(auto_attribs=True)
class ReturnOptionsType:
    ReturnPrintData: typing.Optional[bool] = None
    ReturnRoutingInfo: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class AddressType:
    Name1: typing.Optional[str] = None
    Name2: typing.Optional[str] = None
    Name3: typing.Optional[str] = None
    CountryCode: typing.Optional[str] = None
    Province: typing.Optional[str] = None
    City: typing.Optional[str] = None
    Street: typing.Optional[str] = None
    StreetNumber: typing.Optional[str] = None
    ContactPerson: typing.Optional[str] = None
    FixedLinePhonenumber: typing.Optional[str] = None
    MobilePhoneNumber: typing.Optional[str] = None
    Email: typing.Optional[str] = None
    ZIPCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ConsigneeType:
    ConsigneeID: typing.Optional[str] = None
    CostCenter: typing.Optional[str] = None
    Category: typing.Optional[str] = None
    Address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]


@attr.s(auto_attribs=True)
class ReturnType:
    Address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]


@attr.s(auto_attribs=True)
class DeliveryAtWorkType:
    ServiceName: typing.Optional[str] = None
    RecipientName: typing.Optional[str] = None
    AlternateRecipientName: typing.Optional[str] = None
    Building: typing.Optional[str] = None
    Floor: typing.Optional[str] = None
    Room: typing.Optional[str] = None
    Phonenumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DepositType:
    ServiceName: typing.Optional[str] = None
    PlaceOfDeposit: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ExchangeType:
    ServiceName: typing.Optional[str] = None
    Address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    ExpectedWeight: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class IntercompanyType:
    ServiceName: typing.Optional[str] = None
    Address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    NumberOfLabels: typing.Optional[int] = None
    ExpectedWeight: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class NationalityType:
    CountryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class IdentType:
    ServiceName: typing.Optional[str] = None
    Birthdate: typing.Optional[str] = None
    Firstname: typing.Optional[str] = None
    Lastname: typing.Optional[str] = None
    Nationality: typing.Optional[NationalityType] = jstruct.JStruct[NationalityType]


@attr.s(auto_attribs=True)
class IdentPinType:
    ServiceName: typing.Optional[str] = None
    Pin: typing.Optional[str] = None
    Birthdate: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickAndType:
    ServiceName: typing.Optional[str] = None
    PickupDate: typing.Optional[str] = None
    SendEMailToShipper: typing.Optional[bool] = None
    SendEMailToConsignee: typing.Optional[bool] = None
    SendSMSToShipper: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class ServiceType:
    ServiceName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShopDeliveryType:
    ServiceName: typing.Optional[str] = None
    ParcelShopID: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShopReturnType:
    ServiceName: typing.Optional[str] = None
    NumberOfLabels: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ShipmentServiceType:
    Service: typing.Optional[ServiceType] = jstruct.JStruct[ServiceType]
    ShopDelivery: typing.Optional[ShopDeliveryType] = jstruct.JStruct[ShopDeliveryType]
    ShopReturn: typing.Optional[ShopReturnType] = jstruct.JStruct[ShopReturnType]
    Intercompany: typing.Optional[IntercompanyType] = jstruct.JStruct[IntercompanyType]
    Exchange: typing.Optional[ExchangeType] = jstruct.JStruct[ExchangeType]
    DeliveryAtWork: typing.Optional[DeliveryAtWorkType] = jstruct.JStruct[DeliveryAtWorkType]
    Deposit: typing.Optional[DepositType] = jstruct.JStruct[DepositType]
    IdentPin: typing.Optional[IdentPinType] = jstruct.JStruct[IdentPinType]
    Ident: typing.Optional[IdentType] = jstruct.JStruct[IdentType]
    PickAndShip: typing.Optional[PickAndType] = jstruct.JStruct[PickAndType]
    PickAndReturn: typing.Optional[PickAndType] = jstruct.JStruct[PickAndType]


@attr.s(auto_attribs=True)
class CashType:
    ServiceName: typing.Optional[str] = None
    Reason: typing.Optional[str] = None
    Amount: typing.Optional[float] = None
    Currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AddonLiabilityType:
    ServiceName: typing.Optional[str] = None
    Amount: typing.Optional[float] = None
    Currency: typing.Optional[str] = None
    ParcelContent: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class HazardousGoodType:
    Weight: typing.Optional[float] = None
    GlshazNo: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class HazardousGoodsType:
    ServiceName: typing.Optional[str] = None
    HazardousGood: typing.Optional[typing.List[HazardousGoodType]] = jstruct.JList[HazardousGoodType]


@attr.s(auto_attribs=True)
class LimitedQuantitiesType:
    ServiceName: typing.Optional[str] = None
    Weight: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class ShipmentUnitServiceType:
    Cash: typing.Optional[CashType] = jstruct.JStruct[CashType]
    AddonLiability: typing.Optional[AddonLiabilityType] = jstruct.JStruct[AddonLiabilityType]
    HazardousGoods: typing.Optional[HazardousGoodsType] = jstruct.JStruct[HazardousGoodsType]
    ExWorks: typing.Optional[ServiceType] = jstruct.JStruct[ServiceType]
    LimitedQuantities: typing.Optional[LimitedQuantitiesType] = jstruct.JStruct[LimitedQuantitiesType]


@attr.s(auto_attribs=True)
class VolumeType:
    Width: typing.Optional[str] = None
    Height: typing.Optional[str] = None
    Length: typing.Optional[str] = None
    ScannerStation: typing.Optional[str] = None
    VolumetricType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentUnitType:
    ShipmentUnitReference: typing.Optional[typing.List[str]] = None
    PartnerParcelNumber: typing.Optional[str] = None
    Weight: typing.Optional[float] = None
    Note1: typing.Optional[str] = None
    Note2: typing.Optional[str] = None
    Service: typing.Optional[typing.List[ShipmentUnitServiceType]] = jstruct.JList[ShipmentUnitServiceType]
    TrackID: typing.Optional[str] = None
    Injected: typing.Optional[bool] = None
    ParcelNumber: typing.Optional[str] = None
    Volume: typing.Optional[VolumeType] = jstruct.JStruct[VolumeType]
    FralphaParcelReference: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipperType:
    ContactID: typing.Optional[str] = None
    AlternativeShipperAddress: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    Address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    FralphaCustomerReference: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentType:
    ShipmentReference: typing.Optional[typing.List[str]] = None
    ShippingDate: typing.Optional[str] = None
    IncotermCode: typing.Optional[str] = None
    Identifier: typing.Optional[str] = None
    Middleware: typing.Optional[str] = None
    Product: typing.Optional[str] = None
    ExpressAltDeliveryAllowed: typing.Optional[bool] = None
    Consignee: typing.Optional[ConsigneeType] = jstruct.JStruct[ConsigneeType]
    Shipper: typing.Optional[ShipperType] = jstruct.JStruct[ShipperType]
    Carrier: typing.Optional[str] = None
    ShipmentUnit: typing.Optional[typing.List[ShipmentUnitType]] = jstruct.JList[ShipmentUnitType]
    Service: typing.Optional[typing.List[ShipmentServiceType]] = jstruct.JList[ShipmentServiceType]
    Return: typing.Optional[ReturnType] = jstruct.JStruct[ReturnType]


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    Shipment: typing.Optional[ShipmentType] = jstruct.JStruct[ShipmentType]
    PrintingOptions: typing.Optional[PrintingOptionsType] = jstruct.JStruct[PrintingOptionsType]
    CustomContent: typing.Optional[CustomContentType] = jstruct.JStruct[CustomContentType]
    ReturnOptions: typing.Optional[ReturnOptionsType] = jstruct.JStruct[ReturnOptionsType]
    PartnerReference: typing.Optional[str] = None
