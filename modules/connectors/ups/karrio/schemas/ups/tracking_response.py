from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AccessPointInformationType:
    pickupByDate: Optional[int] = None


@s(auto_attribs=True)
class AddressType:
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    addressLine3: Optional[str] = None
    city: Optional[str] = None
    stateProvince: Optional[str] = None
    countryCode: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None


@s(auto_attribs=True)
class LocationType:
    address: Optional[AddressType] = JStruct[AddressType]
    slic: Optional[str] = None


@s(auto_attribs=True)
class StatusType:
    type: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None
    statusCode: Optional[str] = None
    simplifiedTextDescription: Optional[str] = None


@s(auto_attribs=True)
class ActivityType:
    location: Optional[LocationType] = JStruct[LocationType]
    status: Optional[StatusType] = JStruct[StatusType]
    date: Optional[int] = None
    time: Optional[int] = None


@s(auto_attribs=True)
class NumberType:
    number: Optional[str] = None
    type: Optional[str] = None


@s(auto_attribs=True)
class DeliveryDateType:
    type: Optional[str] = None
    date: Optional[int] = None


@s(auto_attribs=True)
class DeliveryPhotoType:
    isNonPostalCodeCountry: Optional[bool] = None
    photo: Optional[str] = None
    photoCaptureInd: Optional[str] = None
    photoDispositionCode: Optional[str] = None


@s(auto_attribs=True)
class SignatureType:
    image: Optional[str] = None


@s(auto_attribs=True)
class DeliveryInformationType:
    location: Optional[str] = None
    receivedBy: Optional[int] = None
    signature: Optional[SignatureType] = JStruct[SignatureType]
    deliveryPhoto: Optional[DeliveryPhotoType] = JStruct[DeliveryPhotoType]


@s(auto_attribs=True)
class DeliveryTimeType:
    type: Optional[str] = None
    endTime: Optional[int] = None
    startTime: Optional[int] = None


@s(auto_attribs=True)
class SubMilestoneType:
    category: Optional[str] = None


@s(auto_attribs=True)
class MilestoneType:
    category: Optional[str] = None
    code: Optional[str] = None
    current: Optional[bool] = None
    description: Optional[str] = None
    linkedActivity: Optional[str] = None
    state: Optional[str] = None
    subMilestone: Optional[SubMilestoneType] = JStruct[SubMilestoneType]


@s(auto_attribs=True)
class PackageAddressType:
    address: Optional[AddressType] = JStruct[AddressType]
    attentionName: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None


@s(auto_attribs=True)
class PaymentInformationType:
    amount: Optional[str] = None
    currency: Optional[str] = None
    id: Optional[str] = None
    paid: Optional[bool] = None
    paymentMethod: Optional[str] = None
    type: Optional[str] = None


@s(auto_attribs=True)
class ServiceType:
    code: Optional[str] = None
    description: Optional[str] = None


@s(auto_attribs=True)
class WeightType:
    unitOfMeasurement: Optional[str] = None
    weight: Optional[str] = None


@s(auto_attribs=True)
class PackageType:
    accessPointInformation: Optional[AccessPointInformationType] = JStruct[AccessPointInformationType]
    trackingNumber: Optional[str] = None
    activity: List[ActivityType] = JList[ActivityType]
    additionalAttributes: List[str] = []
    additionalServices: List[str] = []
    alternateTrackingNumber: List[NumberType] = JList[NumberType]
    currentStatus: Optional[StatusType] = JStruct[StatusType]
    deliveryDate: List[DeliveryDateType] = JList[DeliveryDateType]
    deliveryInformation: Optional[DeliveryInformationType] = JStruct[DeliveryInformationType]
    deliveryTime: Optional[DeliveryTimeType] = JStruct[DeliveryTimeType]
    milestones: List[MilestoneType] = JList[MilestoneType]
    packageAddress: List[PackageAddressType] = JList[PackageAddressType]
    packageCount: Optional[int] = None
    paymentInformation: Optional[PaymentInformationType] = JStruct[PaymentInformationType]
    referenceNumber: List[NumberType] = JList[NumberType]
    service: Optional[ServiceType] = JStruct[ServiceType]
    statusCode: Optional[str] = None
    statusDescription: Optional[str] = None
    suppressionIndicators: List[str] = []
    weight: Optional[WeightType] = JStruct[WeightType]


@s(auto_attribs=True)
class WarningType:
    code: Optional[int] = None
    message: Optional[str] = None


@s(auto_attribs=True)
class ShipmentType:
    inquiryNumber: Optional[str] = None
    package: List[PackageType] = JList[PackageType]
    userRelation: List[str] = []
    warnings: List[WarningType] = JList[WarningType]


@s(auto_attribs=True)
class TrackResponseType:
    shipment: List[ShipmentType] = JList[ShipmentType]


@s(auto_attribs=True)
class TrackingResponseType:
    trackResponse: Optional[TrackResponseType] = JStruct[TrackResponseType]
