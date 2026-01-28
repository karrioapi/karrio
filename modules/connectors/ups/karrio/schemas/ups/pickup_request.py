import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TransactionReferenceType:
    CustomerContext: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RequestType:
    SubVersion: typing.Optional[str] = None
    TransactionReference: typing.Optional[TransactionReferenceType] = jstruct.JStruct[TransactionReferenceType]


@attr.s(auto_attribs=True)
class AccountType:
    AccountNumber: typing.Optional[str] = None
    AccountCountryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CardAddressType:
    AddressLine: typing.Optional[typing.List[str]] = None
    City: typing.Optional[str] = None
    StateProvince: typing.Optional[str] = None
    PostalCode: typing.Optional[str] = None
    CountryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ChargeCardType:
    CardHolderName: typing.Optional[str] = None
    CardType: typing.Optional[str] = None
    CardNumber: typing.Optional[str] = None
    ExpirationDate: typing.Optional[str] = None
    SecurityCode: typing.Optional[str] = None
    CardAddress: typing.Optional[CardAddressType] = jstruct.JStruct[CardAddressType]


@attr.s(auto_attribs=True)
class ShipperType:
    Account: typing.Optional[AccountType] = jstruct.JStruct[AccountType]
    ChargeCard: typing.Optional[ChargeCardType] = jstruct.JStruct[ChargeCardType]


@attr.s(auto_attribs=True)
class PickupDateInfoType:
    CloseTime: typing.Optional[str] = None
    ReadyTime: typing.Optional[str] = None
    PickupDate: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PhoneType:
    Number: typing.Optional[str] = None
    Extension: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupAddressType:
    CompanyName: typing.Optional[str] = None
    ContactName: typing.Optional[str] = None
    AddressLine: typing.Optional[str] = None
    Room: typing.Optional[str] = None
    Floor: typing.Optional[str] = None
    City: typing.Optional[str] = None
    StateProvince: typing.Optional[str] = None
    Urbanization: typing.Optional[str] = None
    PostalCode: typing.Optional[str] = None
    CountryCode: typing.Optional[str] = None
    ResidentialIndicator: typing.Optional[str] = None
    PickupPoint: typing.Optional[str] = None
    Phone: typing.Optional[PhoneType] = jstruct.JStruct[PhoneType]


@attr.s(auto_attribs=True)
class PickupPieceType:
    ServiceCode: typing.Optional[str] = None
    Quantity: typing.Optional[str] = None
    DestinationCountryCode: typing.Optional[str] = None
    ContainerCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TotalWeightType:
    Weight: typing.Optional[str] = None
    UnitOfMeasurement: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingDataType:
    TrackingNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingDataWithReferenceNumberType:
    TrackingNumber: typing.Optional[str] = None
    ReferenceNumber: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class UnitOfMeasurementType:
    Code: typing.Optional[str] = None
    Description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DimensionsType:
    UnitOfMeasurement: typing.Optional[UnitOfMeasurementType] = jstruct.JStruct[UnitOfMeasurementType]
    Length: typing.Optional[str] = None
    Width: typing.Optional[str] = None
    Height: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PalletInformationType:
    Dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]


@attr.s(auto_attribs=True)
class ShipmentDetailType:
    HazmatIndicator: typing.Optional[str] = None
    PalletInformation: typing.Optional[PalletInformationType] = jstruct.JStruct[PalletInformationType]


@attr.s(auto_attribs=True)
class DestinationAddressType:
    City: typing.Optional[str] = None
    StateProvince: typing.Optional[str] = None
    PostalCode: typing.Optional[str] = None
    CountryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentServiceOptionsType:
    OriginLiftGateIndicator: typing.Optional[str] = None
    DropoffAtUPSFacilityIndicator: typing.Optional[str] = None
    HoldForPickupIndicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class FreightOptionsType:
    ShipmentServiceOptions: typing.Optional[ShipmentServiceOptionsType] = jstruct.JStruct[ShipmentServiceOptionsType]
    OriginServiceCenterCode: typing.Optional[str] = None
    OriginServiceCountryCode: typing.Optional[str] = None
    DestinationAddress: typing.Optional[DestinationAddressType] = jstruct.JStruct[DestinationAddressType]
    ShipmentDetail: typing.Optional[ShipmentDetailType] = jstruct.JStruct[ShipmentDetailType]


@attr.s(auto_attribs=True)
class NotificationType:
    ConfirmationEmailAddress: typing.Optional[str] = None
    UndeliverableEmailAddress: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupCreationRequestType:
    Request: typing.Optional[RequestType] = jstruct.JStruct[RequestType]
    RatePickupIndicator: typing.Optional[str] = None
    RateChartType: typing.Optional[str] = None
    TaxInformationIndicator: typing.Optional[str] = None
    UserLevelDiscountIndicator: typing.Optional[str] = None
    Shipper: typing.Optional[ShipperType] = jstruct.JStruct[ShipperType]
    PickupDateInfo: typing.Optional[PickupDateInfoType] = jstruct.JStruct[PickupDateInfoType]
    PickupAddress: typing.Optional[PickupAddressType] = jstruct.JStruct[PickupAddressType]
    AlternateAddressIndicator: typing.Optional[str] = None
    PickupPiece: typing.Optional[typing.List[PickupPieceType]] = jstruct.JList[PickupPieceType]
    TotalWeight: typing.Optional[TotalWeightType] = jstruct.JStruct[TotalWeightType]
    OverweightIndicator: typing.Optional[str] = None
    TrackingData: typing.Optional[typing.List[TrackingDataType]] = jstruct.JList[TrackingDataType]
    TrackingDataWithReferenceNumber: typing.Optional[TrackingDataWithReferenceNumberType] = jstruct.JStruct[TrackingDataWithReferenceNumberType]
    PaymentMethod: typing.Optional[str] = None
    SpecialInstruction: typing.Optional[str] = None
    ReferenceNumber: typing.Optional[str] = None
    FreightOptions: typing.Optional[FreightOptionsType] = jstruct.JStruct[FreightOptionsType]
    ServiceCategory: typing.Optional[str] = None
    CashType: typing.Optional[str] = None
    ShippingLabelsAvailable: typing.Optional[str] = None
    Notification: typing.Optional[NotificationType] = jstruct.JStruct[NotificationType]


@attr.s(auto_attribs=True)
class PickupCreationRequestWrapperType:
    PickupCreationRequest: typing.Optional[PickupCreationRequestType] = jstruct.JStruct[PickupCreationRequestType]
