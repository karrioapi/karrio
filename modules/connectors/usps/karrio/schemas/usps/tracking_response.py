from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class EMailType:
    futureDelivery: Optional[bool] = None
    alertDelivery: Optional[bool] = None
    todayDelivery: Optional[bool] = None
    UP: Optional[bool] = None
    DND: Optional[bool] = None
    firstDisplayable: Optional[bool] = None
    otherActivity: Optional[bool] = None


@s(auto_attribs=True)
class SMSType:
    futureDelivery: Optional[bool] = None
    alertDelivery: Optional[bool] = None
    todayDelivery: Optional[bool] = None
    UP: Optional[bool] = None
    DND: Optional[bool] = None


@s(auto_attribs=True)
class EnabledNotificationRequestsType:
    SMS: Optional[SMSType] = JStruct[SMSType]
    EMail: Optional[EMailType] = JStruct[EMailType]


@s(auto_attribs=True)
class ExtendRetentionExtraServiceCodeOptionType:
    pass


@s(auto_attribs=True)
class TrackingEventType:
    eventType: Optional[str] = None
    eventTimestamp: Optional[str] = None
    GMTTimestamp: Optional[str] = None
    GMTOffset: Optional[str] = None
    eventCountry: Optional[str] = None
    eventCity: Optional[str] = None
    eventState: Optional[str] = None
    eventZIP: Optional[str] = None
    firm: Optional[str] = None
    name: Optional[str] = None
    authorizedAgent: Optional[bool] = None
    eventCode: Optional[str] = None
    actionCode: Optional[str] = None
    reasonCode: Optional[str] = None


@s(auto_attribs=True)
class TrackingResponseType:
    trackingNumber: Optional[str] = None
    additionalInfo: Optional[str] = None
    ADPScripting: Optional[str] = None
    archiveRestoreInfo: Optional[str] = None
    associatedLabel: Optional[str] = None
    carrierRelease: Optional[bool] = None
    mailClass: Optional[str] = None
    destinationCity: Optional[str] = None
    destinationCountryCode: Optional[str] = None
    destinationState: Optional[str] = None
    destinationZIP: Optional[str] = None
    editedLabelId: Optional[str] = None
    emailEnabled: Optional[bool] = None
    endOfDay: Optional[str] = None
    eSOFEligible: Optional[bool] = None
    expectedDeliveryTimeStamp: Optional[str] = None
    expectedDeliveryType: Optional[str] = None
    guaranteedDeliveryTimeStamp: Optional[str] = None
    guaranteedDetails: Optional[str] = None
    itemShape: Optional[str] = None
    kahalaIndicator: Optional[bool] = None
    mailType: Optional[str] = None
    approximateIntakeDate: Optional[str] = None
    uniqueTrackingId: Optional[str] = None
    onTime: Optional[bool] = None
    originCity: Optional[str] = None
    originCountry: Optional[str] = None
    originState: Optional[str] = None
    originZIP: Optional[str] = None
    proofOfDeliveryEnabled: Optional[bool] = None
    predictedDeliveryTimeStamp: Optional[str] = None
    predictedDeliveryDate: Optional[str] = None
    predictedDeliveryWindowStartTime: Optional[str] = None
    predictedDeliveryWindowEndTime: Optional[str] = None
    relatedReturnReceiptID: Optional[str] = None
    redeliveryEnabled: Optional[bool] = None
    enabledNotificationRequests: Optional[EnabledNotificationRequestsType] = JStruct[EnabledNotificationRequestsType]
    restoreEnabled: Optional[bool] = None
    returnDateNotice: Optional[str] = None
    RRAMenabled: Optional[bool] = None
    RREEnabled: Optional[bool] = None
    services: List[str] = []
    serviceTypeCode: Optional[str] = None
    status: Optional[str] = None
    statusCategory: Optional[str] = None
    statusSummary: Optional[str] = None
    trackingProofOfDeliveryEnabled: Optional[bool] = None
    valueofArticle: Optional[str] = None
    extendRetentionPurchasedCode: Optional[str] = None
    extendRetentionExtraServiceCodeOptions: List[ExtendRetentionExtraServiceCodeOptionType] = JList[ExtendRetentionExtraServiceCodeOptionType]
    trackingEvents: List[TrackingEventType] = JList[TrackingEventType]
