from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class AlternateRateOptionsType:
    Code: Optional[str] = None


@s(auto_attribs=True)
class UnitOfMeasurementType:
    Code: Optional[str] = None
    Description: Optional[str] = None


@s(auto_attribs=True)
class DimensionsType:
    UnitOfMeasurement: Optional[UnitOfMeasurementType] = JStruct[UnitOfMeasurementType]
    Length: Optional[int] = None
    Width: Optional[int] = None
    Height: Optional[int] = None


@s(auto_attribs=True)
class WeightType:
    UnitOfMeasurement: Optional[AlternateRateOptionsType] = JStruct[AlternateRateOptionsType]
    Value: Optional[int] = None


@s(auto_attribs=True)
class CommodityType:
    Description: Optional[str] = None
    Weight: Optional[WeightType] = JStruct[WeightType]
    Dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    NumberOfPieces: Optional[int] = None
    PackagingType: Optional[AlternateRateOptionsType] = JStruct[AlternateRateOptionsType]
    FreightClass: Optional[int] = None


@s(auto_attribs=True)
class GFPOptionsType:
    GPFAccesorialRateIndicator: Optional[str] = None


@s(auto_attribs=True)
class AddressType:
    AddressLine: Optional[str] = None
    City: Optional[str] = None
    StateProvinceCode: Optional[str] = None
    PostalCode: Optional[int] = None
    CountryCode: Optional[str] = None
    ResidentialAddressIndicator: Optional[str] = None


@s(auto_attribs=True)
class PayerPhoneType:
    Number: Optional[str] = None
    Extension: Optional[int] = None


@s(auto_attribs=True)
class PayerType:
    Name: Optional[str] = None
    Address: Optional[AddressType] = JStruct[AddressType]
    ShipperNumber: Optional[str] = None
    AccountType: Optional[int] = None
    AttentionName: Optional[str] = None
    Phone: Optional[PayerPhoneType] = JStruct[PayerPhoneType]
    EMailAddress: Optional[str] = None


@s(auto_attribs=True)
class PaymentInformationType:
    Payer: Optional[PayerType] = JStruct[PayerType]
    ShipmentBillingOption: Optional[AlternateRateOptionsType] = JStruct[AlternateRateOptionsType]


@s(auto_attribs=True)
class PickupRequestType:
    PickupDate: Optional[int] = None


@s(auto_attribs=True)
class ShipFromType:
    Name: Optional[str] = None
    Address: Optional[AddressType] = JStruct[AddressType]
    AttentionName: Optional[str] = None
    Phone: Optional[PayerPhoneType] = JStruct[PayerPhoneType]
    EMailAddress: Optional[str] = None


@s(auto_attribs=True)
class ShipToPhoneType:
    Number: Optional[str] = None


@s(auto_attribs=True)
class ShipToType:
    Name: Optional[str] = None
    Address: Optional[AddressType] = JStruct[AddressType]
    AttentionName: Optional[str] = None
    Phone: Optional[ShipToPhoneType] = JStruct[ShipToPhoneType]


@s(auto_attribs=True)
class FreightRateRequestClassType:
    ShipFrom: Optional[ShipFromType] = JStruct[ShipFromType]
    ShipperNumber: Optional[str] = None
    ShipTo: Optional[ShipToType] = JStruct[ShipToType]
    PaymentInformation: Optional[PaymentInformationType] = JStruct[PaymentInformationType]
    Service: Optional[AlternateRateOptionsType] = JStruct[AlternateRateOptionsType]
    Commodity: Optional[CommodityType] = JStruct[CommodityType]
    DensityEligibleIndicator: Optional[str] = None
    AlternateRateOptions: Optional[AlternateRateOptionsType] = JStruct[AlternateRateOptionsType]
    PickupRequest: Optional[PickupRequestType] = JStruct[PickupRequestType]
    GFPOptions: Optional[GFPOptionsType] = JStruct[GFPOptionsType]
    TimeInTransitIndicator: Optional[str] = None


@s(auto_attribs=True)
class FreightRateRequestType:
    FreightRateRequest: Optional[FreightRateRequestClassType] = JStruct[FreightRateRequestClassType]
