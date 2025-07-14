import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DangerousGoodsItemType:
    Description: typing.Optional[str] = None
    ClassOrDivision: typing.Optional[str] = None
    UNorIDNo: typing.Optional[str] = None
    PackingGroup: typing.Optional[str] = None
    SubsidaryRisk: typing.Optional[str] = None
    Packing: typing.Optional[str] = None
    PackingInstr: typing.Optional[str] = None
    Authorization: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ManufacturerType:
    ManufacturerMID: typing.Optional[str] = None
    Name: typing.Optional[str] = None
    Address1: typing.Optional[str] = None
    Address2: typing.Optional[str] = None
    City: typing.Optional[str] = None
    State: typing.Optional[str] = None
    Zip: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CommodityType:
    Description: typing.Optional[str] = None
    HarmonizedCode: typing.Optional[str] = None
    Units: typing.Optional[int] = None
    UnitValue: typing.Optional[int] = None
    UnitCostValue: typing.Optional[float] = None
    UnitKg: typing.Optional[float] = None
    Currency: typing.Optional[str] = None
    Country: typing.Optional[str] = None
    IsDG: typing.Optional[bool] = None
    itemSKU: typing.Optional[str] = None
    ImageURL: typing.Optional[str] = None
    DangerousGoodsItem: typing.Optional[DangerousGoodsItemType] = jstruct.JStruct[DangerousGoodsItemType]
    Manufacturer: typing.Optional[ManufacturerType] = jstruct.JStruct[ManufacturerType]


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
    Height: typing.Optional[int] = None
    Length: typing.Optional[int] = None
    Id: typing.Optional[int] = None
    Width: typing.Optional[int] = None
    Kg: typing.Optional[float] = None
    Name: typing.Optional[str] = None
    PackageCode: typing.Optional[str] = None
    Type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TaxIDType:
    IdType: typing.Optional[str] = None
    IdNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RatingRequestType:
    DeliveryReference: typing.Optional[str] = None
    Reference2: typing.Optional[str] = None
    Reference3: typing.Optional[str] = None
    Origin: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    Destination: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    IsSaturdayDelivery: typing.Optional[bool] = None
    IsSignatureRequired: typing.Optional[bool] = None
    DangerousGoods: typing.Optional[DangerousGoodsType] = jstruct.JStruct[DangerousGoodsType]
    Commodities: typing.Optional[typing.List[CommodityType]] = jstruct.JList[CommodityType]
    Packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
    Carrier: typing.Optional[str] = None
    Service: typing.Optional[str] = None
    ProductCategory: typing.Optional[str] = None
    ShipType: typing.Optional[str] = None
    CostCentreName: typing.Optional[str] = None
    CostCentreId: typing.Optional[str] = None
    CodValue: typing.Optional[float] = None
    TaxCollected: typing.Optional[bool] = None
    AmountCollected: typing.Optional[float] = None
    CIFValue: typing.Optional[float] = None
    FreightValue: typing.Optional[float] = None
    DutiesAndTaxesByReceiver: typing.Optional[bool] = None
    TaxIds: typing.Optional[typing.List[TaxIDType]] = jstruct.JList[TaxIDType]
