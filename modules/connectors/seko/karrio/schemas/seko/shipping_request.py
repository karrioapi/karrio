import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ItemType:
    HarmonizedCode: typing.Optional[str] = None
    Description: typing.Optional[str] = None
    ClassOrDivision: typing.Optional[str] = None
    UNorIDNo: typing.Optional[str] = None
    PackingGroup: typing.Optional[str] = None
    SubsidaryRisk: typing.Optional[str] = None
    Packing: typing.Optional[str] = None
    PackingInstr: typing.Optional[str] = None
    Authorization: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CommodityType:
    Description: typing.Optional[str] = None
    HarmonizedCode: typing.Optional[str] = None
    Units: typing.Optional[int] = None
    UnitValue: typing.Optional[int] = None
    UnitKg: typing.Optional[float] = None
    Currency: typing.Optional[str] = None
    Country: typing.Optional[str] = None
    IsDG: typing.Optional[bool] = None
    itemSKU: typing.Optional[str] = None
    DangerousGoodsItem: typing.Optional[ItemType] = jstruct.JStruct[ItemType]


@attr.s(auto_attribs=True)
class DangerousGoodsType:
    AdditionalHandlingInfo: typing.Optional[str] = None
    HazchemCode: typing.Optional[str] = None
    IsRadioActive: typing.Optional[bool] = None
    CargoAircraftOnly: typing.Optional[bool] = None
    IsDGLQ: typing.Optional[bool] = None
    TotalQuantity: typing.Optional[int] = None
    TotalKg: typing.Optional[float] = None
    SignOffName: typing.Optional[str] = None
    SignOffRole: typing.Optional[str] = None
    LineItems: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]


@attr.s(auto_attribs=True)
class AddressType:
    BuildingName: typing.Optional[str] = None
    StreetAddress: typing.Optional[str] = None
    Suburb: typing.Optional[str] = None
    City: typing.Optional[str] = None
    PostCode: typing.Optional[int] = None
    CountryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DestinationType:
    Id: typing.Optional[int] = None
    Name: typing.Optional[str] = None
    Address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    ContactPerson: typing.Optional[str] = None
    PhoneNumber: typing.Optional[str] = None
    Email: typing.Optional[str] = None
    DeliveryInstructions: typing.Optional[str] = None
    RecipientTaxId: typing.Optional[int] = None
    SendTrackingEmail: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class PackageType:
    Height: typing.Optional[float] = None
    Length: typing.Optional[float] = None
    Width: typing.Optional[float] = None
    Kg: typing.Optional[float] = None
    Name: typing.Optional[str] = None
    Type: typing.Optional[str] = None
    OverLabelBarcode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TaxIDType:
    IdType: typing.Optional[str] = None
    IdNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingRequestType:
    DeliveryReference: typing.Optional[str] = None
    Reference2: typing.Optional[str] = None
    Reference3: typing.Optional[str] = None
    Origin: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    Destination: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    DangerousGoods: typing.Optional[DangerousGoodsType] = jstruct.JStruct[DangerousGoodsType]
    Commodities: typing.Optional[typing.List[CommodityType]] = jstruct.JList[CommodityType]
    Packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
    issignaturerequired: typing.Optional[bool] = None
    DutiesAndTaxesByReceiver: typing.Optional[bool] = None
    PrintToPrinter: typing.Optional[bool] = None
    IncludeLineDetails: typing.Optional[bool] = None
    Carrier: typing.Optional[str] = None
    Service: typing.Optional[str] = None
    CostCentreName: typing.Optional[str] = None
    CodValue: typing.Optional[float] = None
    TaxCollected: typing.Optional[bool] = None
    AmountCollected: typing.Optional[float] = None
    TaxIds: typing.Optional[typing.List[TaxIDType]] = jstruct.JList[TaxIDType]
    Outputs: typing.Optional[typing.List[str]] = None
