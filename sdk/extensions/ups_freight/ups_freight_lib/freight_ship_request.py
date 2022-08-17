from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class MiscellaneousType:
    WSVersion: Optional[str] = None
    ReleaseID: Optional[str] = None


@s(auto_attribs=True)
class ServiceType:
    Code: Optional[str] = None


@s(auto_attribs=True)
class DimensionsType:
    UnitOfMeasurement: Optional[ServiceType] = JStruct[ServiceType]
    Length: Optional[int] = None
    Width: Optional[int] = None
    Height: Optional[int] = None


@s(auto_attribs=True)
class WeightType:
    UnitOfMeasurement: Optional[ServiceType] = JStruct[ServiceType]
    Value: Optional[int] = None


@s(auto_attribs=True)
class CommodityType:
    Description: Optional[str] = None
    Weight: Optional[WeightType] = JStruct[WeightType]
    Dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    NumberOfPieces: Optional[int] = None
    PackagingType: Optional[ServiceType] = JStruct[ServiceType]
    FreightClass: Optional[int] = None


@s(auto_attribs=True)
class HandlingUnitOneType:
    Quantity: Optional[int] = None
    Type: Optional[ServiceType] = JStruct[ServiceType]


@s(auto_attribs=True)
class AddressType:
    AddressLine: Optional[str] = None
    City: Optional[str] = None
    StateProvinceCode: Optional[str] = None
    PostalCode: Optional[str] = None
    CountryCode: Optional[str] = None


@s(auto_attribs=True)
class PhoneType:
    Number: Optional[str] = None


@s(auto_attribs=True)
class PayerType:
    Name: Optional[str] = None
    Address: Optional[AddressType] = JStruct[AddressType]
    ShipperNumber: Optional[str] = None
    AccountType: Optional[int] = None
    AttentionName: Optional[str] = None
    Phone: Optional[PhoneType] = JStruct[PhoneType]


@s(auto_attribs=True)
class PaymentInformationType:
    Payer: Optional[PayerType] = JStruct[PayerType]
    ShipmentBillingOption: Optional[ServiceType] = JStruct[ServiceType]


@s(auto_attribs=True)
class ShipFromType:
    AttentionName: Optional[str] = None
    EMailAddress: Optional[str] = None
    Name: Optional[str] = None
    Phone: Optional[PhoneType] = JStruct[PhoneType]
    Address: Optional[AddressType] = JStruct[AddressType]


@s(auto_attribs=True)
class PickupRequestType:
    Requester: Optional[ShipFromType] = JStruct[ShipFromType]
    PickupDate: Optional[int] = None
    EarliestTimeReady: Optional[str] = None
    LatestTimeReady: Optional[int] = None


@s(auto_attribs=True)
class ShipmentType:
    ShipFrom: Optional[ShipFromType] = JStruct[ShipFromType]
    ShipperNumber: Optional[int] = None
    ShipTo: Optional[ShipFromType] = JStruct[ShipFromType]
    PaymentInformation: Optional[PaymentInformationType] = JStruct[PaymentInformationType]
    Service: Optional[ServiceType] = JStruct[ServiceType]
    HandlingUnitOne: Optional[HandlingUnitOneType] = JStruct[HandlingUnitOneType]
    Commodity: List[CommodityType] = JList[CommodityType]
    DensityEligibleIndicator: Optional[str] = None
    PickupRequest: Optional[PickupRequestType] = JStruct[PickupRequestType]
    TimeInTransitIndicator: Optional[str] = None


@s(auto_attribs=True)
class FreightShipRequestClassType:
    Shipment: Optional[ShipmentType] = JStruct[ShipmentType]
    Miscellaneous: Optional[MiscellaneousType] = JStruct[MiscellaneousType]


@s(auto_attribs=True)
class FreightShipRequestType:
    FreightShipRequest: Optional[FreightShipRequestClassType] = JStruct[FreightShipRequestClassType]
