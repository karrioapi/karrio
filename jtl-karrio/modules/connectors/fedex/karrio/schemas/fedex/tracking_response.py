import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PackageIdentifierType:
    type: typing.Optional[str] = None
    value: typing.Optional[str] = None
    trackingNumberUniqueId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AdditionalTrackingInfoType:
    hasAssociatedShipments: typing.Optional[bool] = None
    nickname: typing.Optional[str] = None
    packageIdentifiers: typing.Optional[typing.List[PackageIdentifierType]] = jstruct.JList[PackageIdentifierType]
    shipmentNotes: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AvailableImageType:
    size: typing.Optional[str] = None
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReasonDetailType:
    description: typing.Optional[str] = None
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ConsolidationDetailType:
    timeStamp: typing.Optional[str] = None
    consolidationID: typing.Optional[int] = None
    reasonDetail: typing.Optional[ReasonDetailType] = jstruct.JStruct[ReasonDetailType]
    packageCount: typing.Optional[int] = None
    eventType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EstimatedDeliveryTimeWindowWindowType:
    begins: typing.Optional[str] = None
    ends: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EstimatedDeliveryTimeWindowElementType:
    description: typing.Optional[str] = None
    window: typing.Optional[EstimatedDeliveryTimeWindowWindowType] = jstruct.JStruct[EstimatedDeliveryTimeWindowWindowType]
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RequestedAppointmentDetailType:
    date: typing.Optional[str] = None
    window: typing.Optional[typing.List[EstimatedDeliveryTimeWindowElementType]] = jstruct.JList[EstimatedDeliveryTimeWindowElementType]


@attr.s(auto_attribs=True)
class CustomDeliveryOptionType:
    requestedAppointmentDetail: typing.Optional[RequestedAppointmentDetailType] = jstruct.JStruct[RequestedAppointmentDetailType]
    description: typing.Optional[str] = None
    type: typing.Optional[str] = None
    status: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DateAndTimeType:
    dateTime: typing.Optional[str] = None
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class LastUpdatedDestinationAddressType:
    addressClassification: typing.Optional[str] = None
    residential: typing.Optional[bool] = None
    streetLines: typing.Optional[typing.List[str]] = None
    city: typing.Optional[str] = None
    urbanizationCode: typing.Optional[str] = None
    stateOrProvinceCode: typing.Optional[str] = None
    postalCode: typing.Optional[int] = None
    countryCode: typing.Optional[str] = None
    countryName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DeliveryOptionEligibilityDetailType:
    option: typing.Optional[str] = None
    eligibility: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DeliveryDetailsType:
    receivedByName: typing.Optional[str] = None
    destinationServiceArea: typing.Optional[str] = None
    destinationServiceAreaDescription: typing.Optional[str] = None
    locationDescription: typing.Optional[str] = None
    actualDeliveryAddress: typing.Optional[LastUpdatedDestinationAddressType] = jstruct.JStruct[LastUpdatedDestinationAddressType]
    deliveryToday: typing.Optional[bool] = None
    locationType: typing.Optional[str] = None
    signedByName: typing.Optional[str] = None
    officeOrderDeliveryMethod: typing.Optional[str] = None
    deliveryAttempts: typing.Optional[int] = None
    deliveryOptionEligibilityDetails: typing.Optional[typing.List[DeliveryOptionEligibilityDetailType]] = jstruct.JList[DeliveryOptionEligibilityDetailType]


@attr.s(auto_attribs=True)
class ContactType:
    personName: typing.Optional[str] = None
    phoneNumber: typing.Optional[int] = None
    companyName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RecipientInformationType:
    contact: typing.Optional[ContactType] = jstruct.JStruct[ContactType]
    address: typing.Optional[LastUpdatedDestinationAddressType] = jstruct.JStruct[LastUpdatedDestinationAddressType]


@attr.s(auto_attribs=True)
class LocationType:
    locationId: typing.Optional[str] = None
    locationContactAndAddress: typing.Optional[RecipientInformationType] = jstruct.JStruct[RecipientInformationType]
    locationType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DistanceToDestinationType:
    units: typing.Optional[str] = None
    value: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class ParameterListType:
    value: typing.Optional[str] = None
    key: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorType:
    code: typing.Optional[str] = None
    parameterList: typing.Optional[typing.List[ParameterListType]] = jstruct.JList[ParameterListType]
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class InformationNoteType:
    code: typing.Optional[str] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AncillaryDetailType:
    reason: typing.Optional[int] = None
    reasonDescription: typing.Optional[str] = None
    action: typing.Optional[str] = None
    actionDescription: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DelayDetailType:
    type: typing.Optional[str] = None
    subType: typing.Optional[str] = None
    status: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class LatestStatusDetailType:
    scanLocation: typing.Optional[LastUpdatedDestinationAddressType] = jstruct.JStruct[LastUpdatedDestinationAddressType]
    code: typing.Optional[str] = None
    derivedCode: typing.Optional[str] = None
    ancillaryDetails: typing.Optional[typing.List[AncillaryDetailType]] = jstruct.JList[AncillaryDetailType]
    statusByLocale: typing.Optional[str] = None
    description: typing.Optional[str] = None
    delayDetail: typing.Optional[DelayDetailType] = jstruct.JStruct[DelayDetailType]


@attr.s(auto_attribs=True)
class DeclaredValueType:
    currency: typing.Optional[str] = None
    value: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class DimensionType:
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    units: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class WeightType:
    unit: typing.Optional[str] = None
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class WeightAndDimensionsType:
    weight: typing.Optional[typing.List[WeightType]] = jstruct.JList[WeightType]
    dimensions: typing.Optional[typing.List[DimensionType]] = jstruct.JList[DimensionType]


@attr.s(auto_attribs=True)
class PackageDetailsType:
    physicalPackagingType: typing.Optional[str] = None
    sequenceNumber: typing.Optional[int] = None
    undeliveredCount: typing.Optional[int] = None
    packagingDescription: typing.Optional[ReasonDetailType] = jstruct.JStruct[ReasonDetailType]
    count: typing.Optional[int] = None
    weightAndDimensions: typing.Optional[WeightAndDimensionsType] = jstruct.JStruct[WeightAndDimensionsType]
    packageContent: typing.Optional[typing.List[str]] = None
    contentPieceCount: typing.Optional[int] = None
    declaredValue: typing.Optional[DeclaredValueType] = jstruct.JStruct[DeclaredValueType]


@attr.s(auto_attribs=True)
class PieceCountType:
    count: typing.Optional[int] = None
    description: typing.Optional[str] = None
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReturnDetailType:
    authorizationName: typing.Optional[str] = None
    reasonDetail: typing.Optional[typing.List[ReasonDetailType]] = jstruct.JList[ReasonDetailType]


@attr.s(auto_attribs=True)
class ScanEventType:
    date: typing.Optional[str] = None
    derivedStatus: typing.Optional[str] = None
    scanLocation: typing.Optional[LastUpdatedDestinationAddressType] = jstruct.JStruct[LastUpdatedDestinationAddressType]
    locationId: typing.Optional[str] = None
    locationType: typing.Optional[str] = None
    exceptionDescription: typing.Optional[str] = None
    eventDescription: typing.Optional[str] = None
    eventType: typing.Optional[str] = None
    derivedStatusCode: typing.Optional[str] = None
    exceptionCode: typing.Optional[str] = None
    delayDetail: typing.Optional[DelayDetailType] = jstruct.JStruct[DelayDetailType]


@attr.s(auto_attribs=True)
class ServiceCommitMessageType:
    message: typing.Optional[str] = None
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ServiceDetailType:
    description: typing.Optional[str] = None
    shortDescription: typing.Optional[str] = None
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ContentType:
    itemNumber: typing.Optional[str] = None
    receivedQuantity: typing.Optional[int] = None
    description: typing.Optional[str] = None
    partNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class SplitShipmentType:
    pieceCount: typing.Optional[int] = None
    statusDescription: typing.Optional[str] = None
    timestamp: typing.Optional[str] = None
    statusCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentDetailsType:
    contents: typing.Optional[typing.List[ContentType]] = jstruct.JList[ContentType]
    beforePossessionStatus: typing.Optional[bool] = None
    weight: typing.Optional[typing.List[WeightType]] = jstruct.JList[WeightType]
    contentPieceCount: typing.Optional[int] = None
    splitShipments: typing.Optional[typing.List[SplitShipmentType]] = jstruct.JList[SplitShipmentType]


@attr.s(auto_attribs=True)
class SpecialHandlingType:
    description: typing.Optional[str] = None
    type: typing.Optional[str] = None
    paymentType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingNumberInfoType:
    trackingNumber: typing.Optional[str] = None
    carrierCode: typing.Optional[str] = None
    trackingNumberUniqueId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackResultType:
    trackingNumberInfo: typing.Optional[TrackingNumberInfoType] = jstruct.JStruct[TrackingNumberInfoType]
    additionalTrackingInfo: typing.Optional[AdditionalTrackingInfoType] = jstruct.JStruct[AdditionalTrackingInfoType]
    distanceToDestination: typing.Optional[DistanceToDestinationType] = jstruct.JStruct[DistanceToDestinationType]
    consolidationDetail: typing.Optional[typing.List[ConsolidationDetailType]] = jstruct.JList[ConsolidationDetailType]
    meterNumber: typing.Optional[int] = None
    returnDetail: typing.Optional[ReturnDetailType] = jstruct.JStruct[ReturnDetailType]
    serviceDetail: typing.Optional[ServiceDetailType] = jstruct.JStruct[ServiceDetailType]
    destinationLocation: typing.Optional[LocationType] = jstruct.JStruct[LocationType]
    latestStatusDetail: typing.Optional[LatestStatusDetailType] = jstruct.JStruct[LatestStatusDetailType]
    serviceCommitMessage: typing.Optional[ServiceCommitMessageType] = jstruct.JStruct[ServiceCommitMessageType]
    informationNotes: typing.Optional[typing.List[InformationNoteType]] = jstruct.JList[InformationNoteType]
    error: typing.Optional[ErrorType] = jstruct.JStruct[ErrorType]
    specialHandlings: typing.Optional[typing.List[SpecialHandlingType]] = jstruct.JList[SpecialHandlingType]
    availableImages: typing.Optional[typing.List[AvailableImageType]] = jstruct.JList[AvailableImageType]
    deliveryDetails: typing.Optional[DeliveryDetailsType] = jstruct.JStruct[DeliveryDetailsType]
    scanEvents: typing.Optional[typing.List[ScanEventType]] = jstruct.JList[ScanEventType]
    dateAndTimes: typing.Optional[typing.List[DateAndTimeType]] = jstruct.JList[DateAndTimeType]
    packageDetails: typing.Optional[PackageDetailsType] = jstruct.JStruct[PackageDetailsType]
    goodsClassificationCode: typing.Optional[str] = None
    holdAtLocation: typing.Optional[LocationType] = jstruct.JStruct[LocationType]
    customDeliveryOptions: typing.Optional[typing.List[CustomDeliveryOptionType]] = jstruct.JList[CustomDeliveryOptionType]
    estimatedDeliveryTimeWindow: typing.Optional[EstimatedDeliveryTimeWindowElementType] = jstruct.JStruct[EstimatedDeliveryTimeWindowElementType]
    pieceCounts: typing.Optional[typing.List[PieceCountType]] = jstruct.JList[PieceCountType]
    originLocation: typing.Optional[LocationType] = jstruct.JStruct[LocationType]
    recipientInformation: typing.Optional[RecipientInformationType] = jstruct.JStruct[RecipientInformationType]
    standardTransitTimeWindow: typing.Optional[EstimatedDeliveryTimeWindowElementType] = jstruct.JStruct[EstimatedDeliveryTimeWindowElementType]
    shipmentDetails: typing.Optional[ShipmentDetailsType] = jstruct.JStruct[ShipmentDetailsType]
    reasonDetail: typing.Optional[ReasonDetailType] = jstruct.JStruct[ReasonDetailType]
    availableNotifications: typing.Optional[typing.List[str]] = None
    shipperInformation: typing.Optional[RecipientInformationType] = jstruct.JStruct[RecipientInformationType]
    lastUpdatedDestinationAddress: typing.Optional[LastUpdatedDestinationAddressType] = jstruct.JStruct[LastUpdatedDestinationAddressType]


@attr.s(auto_attribs=True)
class CompleteTrackResultType:
    trackingNumber: typing.Optional[str] = None
    trackResults: typing.Optional[typing.List[TrackResultType]] = jstruct.JList[TrackResultType]


@attr.s(auto_attribs=True)
class OutputType:
    completeTrackResults: typing.Optional[typing.List[CompleteTrackResultType]] = jstruct.JList[CompleteTrackResultType]
    alerts: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponseType:
    transactionId: typing.Optional[str] = None
    customerTransactionId: typing.Optional[str] = None
    output: typing.Optional[OutputType] = jstruct.JStruct[OutputType]
