from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class PackageIdentifierType:
    type: Optional[str] = None
    value: Optional[str] = None
    trackingNumberUniqueId: Optional[str] = None


@s(auto_attribs=True)
class AdditionalTrackingInfoType:
    hasAssociatedShipments: Optional[bool] = None
    nickname: Optional[str] = None
    packageIdentifiers: List[PackageIdentifierType] = JList[PackageIdentifierType]
    shipmentNotes: Optional[str] = None


@s(auto_attribs=True)
class AvailableImageType:
    size: Optional[str] = None
    type: Optional[str] = None


@s(auto_attribs=True)
class ReasonDetailType:
    description: Optional[str] = None
    type: Optional[str] = None


@s(auto_attribs=True)
class ConsolidationDetailType:
    timeStamp: Optional[str] = None
    consolidationID: Optional[int] = None
    reasonDetail: Optional[ReasonDetailType] = JStruct[ReasonDetailType]
    packageCount: Optional[int] = None
    eventType: Optional[str] = None


@s(auto_attribs=True)
class EstimatedDeliveryTimeWindowWindowType:
    begins: Optional[str] = None
    ends: Optional[str] = None


@s(auto_attribs=True)
class EstimatedDeliveryTimeWindowElementType:
    description: Optional[str] = None
    window: Optional[EstimatedDeliveryTimeWindowWindowType] = JStruct[EstimatedDeliveryTimeWindowWindowType]
    type: Optional[str] = None


@s(auto_attribs=True)
class RequestedAppointmentDetailType:
    date: Optional[str] = None
    window: List[EstimatedDeliveryTimeWindowElementType] = JList[EstimatedDeliveryTimeWindowElementType]


@s(auto_attribs=True)
class CustomDeliveryOptionType:
    requestedAppointmentDetail: Optional[RequestedAppointmentDetailType] = JStruct[RequestedAppointmentDetailType]
    description: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None


@s(auto_attribs=True)
class DateAndTimeType:
    dateTime: Optional[str] = None
    type: Optional[str] = None


@s(auto_attribs=True)
class LastUpdatedDestinationAddressType:
    addressClassification: Optional[str] = None
    residential: Optional[bool] = None
    streetLines: List[str] = []
    city: Optional[str] = None
    urbanizationCode: Optional[str] = None
    stateOrProvinceCode: Optional[str] = None
    postalCode: Optional[int] = None
    countryCode: Optional[str] = None
    countryName: Optional[str] = None


@s(auto_attribs=True)
class DeliveryOptionEligibilityDetailType:
    option: Optional[str] = None
    eligibility: Optional[str] = None


@s(auto_attribs=True)
class DeliveryDetailsType:
    receivedByName: Optional[str] = None
    destinationServiceArea: Optional[str] = None
    destinationServiceAreaDescription: Optional[str] = None
    locationDescription: Optional[str] = None
    actualDeliveryAddress: Optional[LastUpdatedDestinationAddressType] = JStruct[LastUpdatedDestinationAddressType]
    deliveryToday: Optional[bool] = None
    locationType: Optional[str] = None
    signedByName: Optional[str] = None
    officeOrderDeliveryMethod: Optional[str] = None
    deliveryAttempts: Optional[int] = None
    deliveryOptionEligibilityDetails: List[DeliveryOptionEligibilityDetailType] = JList[DeliveryOptionEligibilityDetailType]


@s(auto_attribs=True)
class ContactType:
    personName: Optional[str] = None
    phoneNumber: Optional[int] = None
    companyName: Optional[str] = None


@s(auto_attribs=True)
class RecipientInformationType:
    contact: Optional[ContactType] = JStruct[ContactType]
    address: Optional[LastUpdatedDestinationAddressType] = JStruct[LastUpdatedDestinationAddressType]


@s(auto_attribs=True)
class LocationType:
    locationId: Optional[str] = None
    locationContactAndAddress: Optional[RecipientInformationType] = JStruct[RecipientInformationType]
    locationType: Optional[str] = None


@s(auto_attribs=True)
class DistanceToDestinationType:
    units: Optional[str] = None
    value: Optional[float] = None


@s(auto_attribs=True)
class ParameterListType:
    value: Optional[str] = None
    key: Optional[str] = None


@s(auto_attribs=True)
class ErrorType:
    code: Optional[str] = None
    parameterList: List[ParameterListType] = JList[ParameterListType]
    message: Optional[str] = None


@s(auto_attribs=True)
class InformationNoteType:
    code: Optional[str] = None
    description: Optional[str] = None


@s(auto_attribs=True)
class AncillaryDetailType:
    reason: Optional[int] = None
    reasonDescription: Optional[str] = None
    action: Optional[str] = None
    actionDescription: Optional[str] = None


@s(auto_attribs=True)
class DelayDetailType:
    type: Optional[str] = None
    subType: Optional[str] = None
    status: Optional[str] = None


@s(auto_attribs=True)
class LatestStatusDetailType:
    scanLocation: Optional[LastUpdatedDestinationAddressType] = JStruct[LastUpdatedDestinationAddressType]
    code: Optional[str] = None
    derivedCode: Optional[str] = None
    ancillaryDetails: List[AncillaryDetailType] = JList[AncillaryDetailType]
    statusByLocale: Optional[str] = None
    description: Optional[str] = None
    delayDetail: Optional[DelayDetailType] = JStruct[DelayDetailType]


@s(auto_attribs=True)
class DeclaredValueType:
    currency: Optional[str] = None
    value: Optional[float] = None


@s(auto_attribs=True)
class DimensionType:
    length: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    units: Optional[str] = None


@s(auto_attribs=True)
class WeightType:
    unit: Optional[str] = None
    value: Optional[str] = None


@s(auto_attribs=True)
class WeightAndDimensionsType:
    weight: List[WeightType] = JList[WeightType]
    dimensions: List[DimensionType] = JList[DimensionType]


@s(auto_attribs=True)
class PackageDetailsType:
    physicalPackagingType: Optional[str] = None
    sequenceNumber: Optional[int] = None
    undeliveredCount: Optional[int] = None
    packagingDescription: Optional[ReasonDetailType] = JStruct[ReasonDetailType]
    count: Optional[int] = None
    weightAndDimensions: Optional[WeightAndDimensionsType] = JStruct[WeightAndDimensionsType]
    packageContent: List[str] = []
    contentPieceCount: Optional[int] = None
    declaredValue: Optional[DeclaredValueType] = JStruct[DeclaredValueType]


@s(auto_attribs=True)
class PieceCountType:
    count: Optional[int] = None
    description: Optional[str] = None
    type: Optional[str] = None


@s(auto_attribs=True)
class ReturnDetailType:
    authorizationName: Optional[str] = None
    reasonDetail: List[ReasonDetailType] = JList[ReasonDetailType]


@s(auto_attribs=True)
class ScanEventType:
    date: Optional[str] = None
    derivedStatus: Optional[str] = None
    scanLocation: Optional[LastUpdatedDestinationAddressType] = JStruct[LastUpdatedDestinationAddressType]
    locationId: Optional[str] = None
    locationType: Optional[str] = None
    exceptionDescription: Optional[str] = None
    eventDescription: Optional[str] = None
    eventType: Optional[str] = None
    derivedStatusCode: Optional[str] = None
    exceptionCode: Optional[str] = None
    delayDetail: Optional[DelayDetailType] = JStruct[DelayDetailType]


@s(auto_attribs=True)
class ServiceCommitMessageType:
    message: Optional[str] = None
    type: Optional[str] = None


@s(auto_attribs=True)
class ServiceDetailType:
    description: Optional[str] = None
    shortDescription: Optional[str] = None
    type: Optional[str] = None


@s(auto_attribs=True)
class ContentType:
    itemNumber: Optional[str] = None
    receivedQuantity: Optional[int] = None
    description: Optional[str] = None
    partNumber: Optional[str] = None


@s(auto_attribs=True)
class SplitShipmentType:
    pieceCount: Optional[int] = None
    statusDescription: Optional[str] = None
    timestamp: Optional[str] = None
    statusCode: Optional[str] = None


@s(auto_attribs=True)
class ShipmentDetailsType:
    contents: List[ContentType] = JList[ContentType]
    beforePossessionStatus: Optional[bool] = None
    weight: List[WeightType] = JList[WeightType]
    contentPieceCount: Optional[int] = None
    splitShipments: List[SplitShipmentType] = JList[SplitShipmentType]


@s(auto_attribs=True)
class SpecialHandlingType:
    description: Optional[str] = None
    type: Optional[str] = None
    paymentType: Optional[str] = None


@s(auto_attribs=True)
class TrackingNumberInfoType:
    trackingNumber: Optional[str] = None
    carrierCode: Optional[str] = None
    trackingNumberUniqueId: Optional[str] = None


@s(auto_attribs=True)
class TrackResultType:
    trackingNumberInfo: Optional[TrackingNumberInfoType] = JStruct[TrackingNumberInfoType]
    additionalTrackingInfo: Optional[AdditionalTrackingInfoType] = JStruct[AdditionalTrackingInfoType]
    distanceToDestination: Optional[DistanceToDestinationType] = JStruct[DistanceToDestinationType]
    consolidationDetail: List[ConsolidationDetailType] = JList[ConsolidationDetailType]
    meterNumber: Optional[int] = None
    returnDetail: Optional[ReturnDetailType] = JStruct[ReturnDetailType]
    serviceDetail: Optional[ServiceDetailType] = JStruct[ServiceDetailType]
    destinationLocation: Optional[LocationType] = JStruct[LocationType]
    latestStatusDetail: Optional[LatestStatusDetailType] = JStruct[LatestStatusDetailType]
    serviceCommitMessage: Optional[ServiceCommitMessageType] = JStruct[ServiceCommitMessageType]
    informationNotes: List[InformationNoteType] = JList[InformationNoteType]
    error: Optional[ErrorType] = JStruct[ErrorType]
    specialHandlings: List[SpecialHandlingType] = JList[SpecialHandlingType]
    availableImages: List[AvailableImageType] = JList[AvailableImageType]
    deliveryDetails: Optional[DeliveryDetailsType] = JStruct[DeliveryDetailsType]
    scanEvents: List[ScanEventType] = JList[ScanEventType]
    dateAndTimes: List[DateAndTimeType] = JList[DateAndTimeType]
    packageDetails: Optional[PackageDetailsType] = JStruct[PackageDetailsType]
    goodsClassificationCode: Optional[str] = None
    holdAtLocation: Optional[LocationType] = JStruct[LocationType]
    customDeliveryOptions: List[CustomDeliveryOptionType] = JList[CustomDeliveryOptionType]
    estimatedDeliveryTimeWindow: Optional[EstimatedDeliveryTimeWindowElementType] = JStruct[EstimatedDeliveryTimeWindowElementType]
    pieceCounts: List[PieceCountType] = JList[PieceCountType]
    originLocation: Optional[LocationType] = JStruct[LocationType]
    recipientInformation: Optional[RecipientInformationType] = JStruct[RecipientInformationType]
    standardTransitTimeWindow: Optional[EstimatedDeliveryTimeWindowElementType] = JStruct[EstimatedDeliveryTimeWindowElementType]
    shipmentDetails: Optional[ShipmentDetailsType] = JStruct[ShipmentDetailsType]
    reasonDetail: Optional[ReasonDetailType] = JStruct[ReasonDetailType]
    availableNotifications: List[str] = []
    shipperInformation: Optional[RecipientInformationType] = JStruct[RecipientInformationType]
    lastUpdatedDestinationAddress: Optional[LastUpdatedDestinationAddressType] = JStruct[LastUpdatedDestinationAddressType]


@s(auto_attribs=True)
class CompleteTrackResultType:
    trackingNumber: Optional[str] = None
    trackResults: List[TrackResultType] = JList[TrackResultType]


@s(auto_attribs=True)
class OutputType:
    completeTrackResults: List[CompleteTrackResultType] = JList[CompleteTrackResultType]
    alerts: Optional[str] = None


@s(auto_attribs=True)
class TrackingResponseType:
    transactionId: Optional[str] = None
    customerTransactionId: Optional[str] = None
    output: Optional[OutputType] = JStruct[OutputType]
