import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class EMailType:
    futureDelivery: typing.Optional[bool] = None
    alertDelivery: typing.Optional[bool] = None
    todayDelivery: typing.Optional[bool] = None
    UP: typing.Optional[bool] = None
    DND: typing.Optional[bool] = None
    firstDisplayable: typing.Optional[bool] = None
    otherActivity: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class SMSType:
    futureDelivery: typing.Optional[bool] = None
    alertDelivery: typing.Optional[bool] = None
    todayDelivery: typing.Optional[bool] = None
    UP: typing.Optional[bool] = None
    DND: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class EnabledNotificationRequestsType:
    SMS: typing.Optional[SMSType] = jstruct.JStruct[SMSType]
    EMail: typing.Optional[EMailType] = jstruct.JStruct[EMailType]


@attr.s(auto_attribs=True)
class ExtendRetentionExtraServiceCodeOptionType:
    pass


@attr.s(auto_attribs=True)
class TrackingEventType:
    eventType: typing.Optional[str] = None
    eventTimestamp: typing.Optional[str] = None
    GMTTimestamp: typing.Optional[str] = None
    GMTOffset: typing.Optional[str] = None
    eventCountry: typing.Optional[str] = None
    eventCity: typing.Optional[str] = None
    eventState: typing.Optional[str] = None
    eventZIP: typing.Optional[str] = None
    firm: typing.Optional[str] = None
    name: typing.Optional[str] = None
    authorizedAgent: typing.Optional[bool] = None
    eventCode: typing.Optional[str] = None
    additionalProp: typing.Any = None
    actionCode: typing.Optional[str] = None
    reasonCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponseType:
    destinationCity: typing.Optional[str] = None
    destinationState: typing.Optional[str] = None
    destinationZIP: typing.Optional[str] = None
    emailEnabled: typing.Optional[bool] = None
    kahalaIndicator: typing.Optional[bool] = None
    mailClass: typing.Optional[str] = None
    mailType: typing.Optional[str] = None
    originCity: typing.Optional[str] = None
    originState: typing.Optional[str] = None
    originZIP: typing.Optional[str] = None
    proofOfDeliveryEnabled: typing.Optional[bool] = None
    restoreEnabled: typing.Optional[bool] = None
    RRAMEnabled: typing.Optional[bool] = None
    RREEnabled: typing.Optional[bool] = None
    services: typing.Optional[typing.List[str]] = None
    serviceTypeCode: typing.Optional[str] = None
    status: typing.Optional[str] = None
    statusCategory: typing.Optional[str] = None
    statusSummary: typing.Optional[str] = None
    tableCode: typing.Optional[str] = None
    uniqueMailPieceID: typing.Optional[int] = None
    mailPieceIntakeDate: typing.Optional[str] = None
    trackingEvents: typing.Optional[typing.List[TrackingEventType]] = jstruct.JList[TrackingEventType]
    trackingNumber: typing.Optional[str] = None
    additionalInfo: typing.Optional[str] = None
    ADPScripting: typing.Optional[str] = None
    archiveRestoreInfo: typing.Optional[str] = None
    associatedLabel: typing.Optional[str] = None
    carrierRelease: typing.Optional[bool] = None
    destinationCountryCode: typing.Optional[str] = None
    editedLabelId: typing.Optional[str] = None
    endOfDay: typing.Optional[str] = None
    eSOFEligible: typing.Optional[bool] = None
    expectedDeliveryTimeStamp: typing.Optional[str] = None
    expectedDeliveryType: typing.Optional[str] = None
    guaranteedDeliveryTimeStamp: typing.Optional[str] = None
    guaranteedDetails: typing.Optional[str] = None
    itemShape: typing.Optional[str] = None
    approximateIntakeDate: typing.Optional[str] = None
    uniqueTrackingId: typing.Optional[str] = None
    uniqueMailPieceId: typing.Optional[str] = None
    onTime: typing.Optional[bool] = None
    originCountry: typing.Optional[str] = None
    predictedDeliveryTimeStamp: typing.Optional[str] = None
    predictedDeliveryDate: typing.Optional[str] = None
    predictedDeliveryWindowStartTime: typing.Optional[str] = None
    predictedDeliveryWindowEndTime: typing.Optional[str] = None
    relatedReturnReceiptID: typing.Optional[str] = None
    redeliveryEnabled: typing.Optional[bool] = None
    enabledNotificationRequests: typing.Optional[EnabledNotificationRequestsType] = jstruct.JStruct[EnabledNotificationRequestsType]
    returnDateNotice: typing.Optional[str] = None
    RRAMenabled: typing.Optional[bool] = None
    trackingProofOfDeliveryEnabled: typing.Optional[bool] = None
    valueofArticle: typing.Optional[str] = None
    extendRetentionPurchasedCode: typing.Optional[str] = None
    extendRetentionExtraServiceCodeOptions: typing.Optional[typing.List[ExtendRetentionExtraServiceCodeOptionType]] = jstruct.JList[ExtendRetentionExtraServiceCodeOptionType]
