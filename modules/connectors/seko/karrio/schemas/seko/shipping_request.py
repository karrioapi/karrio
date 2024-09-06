from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ItemType:
    HarmonizedCode: Optional[str] = None
    Description: Optional[str] = None
    ClassOrDivision: Optional[str] = None
    UNorIDNo: Optional[str] = None
    PackingGroup: Optional[str] = None
    SubsidaryRisk: Optional[str] = None
    Packing: Optional[str] = None
    PackingInstr: Optional[str] = None
    Authorization: Optional[str] = None


@s(auto_attribs=True)
class CommodityType:
    Description: Optional[str] = None
    HarmonizedCode: Optional[str] = None
    Units: Optional[int] = None
    UnitValue: Optional[int] = None
    UnitKg: Optional[float] = None
    Currency: Optional[str] = None
    Country: Optional[str] = None
    IsDG: Optional[bool] = None
    itemSKU: Optional[str] = None
    DangerousGoodsItem: Optional[ItemType] = JStruct[ItemType]


@s(auto_attribs=True)
class DangerousGoodsType:
    AdditionalHandlingInfo: Optional[str] = None
    HazchemCode: Optional[str] = None
    IsRadioActive: Optional[bool] = None
    CargoAircraftOnly: Optional[bool] = None
    IsDGLQ: Optional[bool] = None
    TotalQuantity: Optional[int] = None
    TotalKg: Optional[float] = None
    SignOffName: Optional[str] = None
    SignOffRole: Optional[str] = None
    LineItems: List[ItemType] = JList[ItemType]


@s(auto_attribs=True)
class AddressType:
    BuildingName: Optional[str] = None
    StreetAddress: Optional[str] = None
    Suburb: Optional[str] = None
    City: Optional[str] = None
    PostCode: Optional[int] = None
    CountryCode: Optional[str] = None


@s(auto_attribs=True)
class DestinationType:
    Id: Optional[int] = None
    Name: Optional[str] = None
    Address: Optional[AddressType] = JStruct[AddressType]
    ContactPerson: Optional[str] = None
    PhoneNumber: Optional[str] = None
    Email: Optional[str] = None
    DeliveryInstructions: Optional[str] = None
    RecipientTaxId: Optional[int] = None
    SendTrackingEmail: Optional[bool] = None


@s(auto_attribs=True)
class PackageType:
    Height: Optional[float] = None
    Length: Optional[float] = None
    Width: Optional[float] = None
    Kg: Optional[float] = None
    Name: Optional[str] = None
    Type: Optional[str] = None
    OverLabelBarcode: Optional[str] = None


@s(auto_attribs=True)
class TaxIDType:
    IdType: Optional[str] = None
    IdNumber: Optional[str] = None


@s(auto_attribs=True)
class ShippingRequestType:
    DeliveryReference: Optional[str] = None
    Reference2: Optional[str] = None
    Reference3: Optional[str] = None
    Origin: Optional[DestinationType] = JStruct[DestinationType]
    Destination: Optional[DestinationType] = JStruct[DestinationType]
    DangerousGoods: Optional[DangerousGoodsType] = JStruct[DangerousGoodsType]
    Commodities: List[CommodityType] = JList[CommodityType]
    Packages: List[PackageType] = JList[PackageType]
    issignaturerequired: Optional[bool] = None
    DutiesAndTaxesByReceiver: Optional[bool] = None
    PrintToPrinter: Optional[bool] = None
    IncludeLineDetails: Optional[bool] = None
    Carrier: Optional[str] = None
    Service: Optional[str] = None
    CostCentreName: Optional[str] = None
    CodValue: Optional[float] = None
    TaxCollected: Optional[bool] = None
    AmountCollected: Optional[float] = None
    TaxIds: List[TaxIDType] = JList[TaxIDType]
    Outputs: List[str] = []
