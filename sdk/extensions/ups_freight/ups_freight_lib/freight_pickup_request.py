from attr import s
from typing import Optional, List
from jstruct import JStruct


@s(auto_attribs=True)
class ExistingShipmentIDType:
    ShipmentNumber: Optional[str] = None
    BOLID: Optional[str] = None


@s(auto_attribs=True)
class EMailNotificationType:
    EMailAddress: Optional[str] = None
    EventType: Optional[str] = None
    FailedEMail: Optional[str] = None


@s(auto_attribs=True)
class PickupNotificationsType:
    CompanyName: Optional[str] = None
    EMailNotification: Optional[EMailNotificationType] = JStruct[EMailNotificationType]


@s(auto_attribs=True)
class PomType:
    POMNumber: Optional[str] = None
    POMNumberType: Optional[str] = None
    PickupNotifications: Optional[PickupNotificationsType] = JStruct[PickupNotificationsType]


@s(auto_attribs=True)
class TransactionReferenceType:
    CustomerContext: Optional[str] = None
    TransactionIdentifier: Optional[str] = None


@s(auto_attribs=True)
class RequestType:
    TransactionReference: Optional[TransactionReferenceType] = JStruct[TransactionReferenceType]


@s(auto_attribs=True)
class AddressType:
    AddressLine: List[str] = []
    City: Optional[str] = None
    StateProvinceCode: Optional[str] = None
    PostalCode: Optional[int] = None
    CountryCode: Optional[str] = None


@s(auto_attribs=True)
class PhoneType:
    Number: Optional[str] = None
    Extension: Optional[int] = None


@s(auto_attribs=True)
class RequesterType:
    ThirdPartyIndicator: Optional[bool] = None
    AttentionName: Optional[str] = None
    EMailAddress: Optional[str] = None
    Name: Optional[str] = None
    Phone: Optional[PhoneType] = JStruct[PhoneType]
    Address: Optional[AddressType] = JStruct[AddressType]


@s(auto_attribs=True)
class PackagingTypeType:
    Code: Optional[str] = None
    Description: Optional[str] = None


@s(auto_attribs=True)
class WeightType:
    UnitOfMeasurement: Optional[PackagingTypeType] = JStruct[PackagingTypeType]
    Value: Optional[int] = None


@s(auto_attribs=True)
class ShipmentDetailType:
    HazmatIndicator: Optional[str] = None
    PackagingType: Optional[PackagingTypeType] = JStruct[PackagingTypeType]
    NumberOfPieces: Optional[int] = None
    DescriptionOfCommodity: Optional[str] = None
    Weight: Optional[WeightType] = JStruct[WeightType]


@s(auto_attribs=True)
class ShipmentServiceOptionsType:
    FreezableProtectionIndicator: Optional[str] = None
    LimitedAccessPickupIndicator: Optional[str] = None
    LimitedAccessDeliveryIndicator: Optional[str] = None
    ExtremeLengthIndicator: Optional[str] = None


@s(auto_attribs=True)
class FreightPickupRequestClassType:
    Request: Optional[RequestType] = JStruct[RequestType]
    DestinationPostalCode: Optional[int] = None
    DestinationCountryCode: Optional[str] = None
    Requester: Optional[RequesterType] = JStruct[RequesterType]
    ShipFrom: Optional[RequesterType] = JStruct[RequesterType]
    PickupDate: Optional[int] = None
    EarliestTimeReady: Optional[str] = None
    LatestTimeReady: Optional[int] = None
    ShipmentServiceOptions: Optional[ShipmentServiceOptionsType] = JStruct[ShipmentServiceOptionsType]
    ShipmentDetail: Optional[ShipmentDetailType] = JStruct[ShipmentDetailType]
    ExistingShipmentID: Optional[ExistingShipmentIDType] = JStruct[ExistingShipmentIDType]
    POM: Optional[PomType] = JStruct[PomType]
    PickupInstructions: Optional[str] = None
    AdditionalComments: Optional[str] = None
    HandlingInstructions: Optional[str] = None
    SpecialInstructions: Optional[str] = None
    DeliveryInstructions: Optional[str] = None


@s(auto_attribs=True)
class FreightPickupRequestType:
    FreightPickupRequest: Optional[FreightPickupRequestClassType] = JStruct[FreightPickupRequestClassType]
