import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AccessPointInformationType:
    pickupByDate: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class AddressType:
    addressLine1: typing.Optional[str] = None
    addressLine2: typing.Optional[str] = None
    addressLine3: typing.Optional[str] = None
    city: typing.Optional[str] = None
    stateProvince: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None
    postalCode: typing.Optional[str] = None
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class LocationType:
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    slic: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class StatusType:
    type: typing.Optional[str] = None
    description: typing.Optional[str] = None
    code: typing.Optional[str] = None
    statusCode: typing.Optional[str] = None
    simplifiedTextDescription: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ActivityType:
    location: typing.Optional[LocationType] = jstruct.JStruct[LocationType]
    status: typing.Optional[StatusType] = jstruct.JStruct[StatusType]
    date: typing.Optional[int] = None
    time: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class NumberType:
    number: typing.Optional[str] = None
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DeliveryDateType:
    type: typing.Optional[str] = None
    date: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class DeliveryPhotoType:
    isNonPostalCodeCountry: typing.Optional[bool] = None
    photo: typing.Optional[str] = None
    photoCaptureInd: typing.Optional[str] = None
    photoDispositionCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class SignatureType:
    image: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DeliveryInformationType:
    location: typing.Optional[str] = None
    receivedBy: typing.Optional[int] = None
    signature: typing.Optional[SignatureType] = jstruct.JStruct[SignatureType]
    deliveryPhoto: typing.Optional[DeliveryPhotoType] = jstruct.JStruct[DeliveryPhotoType]


@attr.s(auto_attribs=True)
class DeliveryTimeType:
    type: typing.Optional[str] = None
    endTime: typing.Optional[int] = None
    startTime: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class SubMilestoneType:
    category: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class MilestoneType:
    category: typing.Optional[str] = None
    code: typing.Optional[str] = None
    current: typing.Optional[bool] = None
    description: typing.Optional[str] = None
    linkedActivity: typing.Optional[str] = None
    state: typing.Optional[str] = None
    subMilestone: typing.Optional[SubMilestoneType] = jstruct.JStruct[SubMilestoneType]


@attr.s(auto_attribs=True)
class PackageAddressType:
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    attentionName: typing.Optional[str] = None
    name: typing.Optional[str] = None
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PaymentInformationType:
    amount: typing.Optional[str] = None
    currency: typing.Optional[str] = None
    id: typing.Optional[str] = None
    paid: typing.Optional[bool] = None
    paymentMethod: typing.Optional[str] = None
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ServiceType:
    code: typing.Optional[str] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class WeightType:
    unitOfMeasurement: typing.Optional[str] = None
    weight: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageType:
    accessPointInformation: typing.Optional[AccessPointInformationType] = jstruct.JStruct[AccessPointInformationType]
    trackingNumber: typing.Optional[str] = None
    activity: typing.Optional[typing.List[ActivityType]] = jstruct.JList[ActivityType]
    additionalAttributes: typing.Optional[typing.List[str]] = None
    additionalServices: typing.Optional[typing.List[str]] = None
    alternateTrackingNumber: typing.Optional[typing.List[NumberType]] = jstruct.JList[NumberType]
    currentStatus: typing.Optional[StatusType] = jstruct.JStruct[StatusType]
    deliveryDate: typing.Optional[typing.List[DeliveryDateType]] = jstruct.JList[DeliveryDateType]
    deliveryInformation: typing.Optional[DeliveryInformationType] = jstruct.JStruct[DeliveryInformationType]
    deliveryTime: typing.Optional[DeliveryTimeType] = jstruct.JStruct[DeliveryTimeType]
    milestones: typing.Optional[typing.List[MilestoneType]] = jstruct.JList[MilestoneType]
    packageAddress: typing.Optional[typing.List[PackageAddressType]] = jstruct.JList[PackageAddressType]
    packageCount: typing.Optional[int] = None
    paymentInformation: typing.Optional[PaymentInformationType] = jstruct.JStruct[PaymentInformationType]
    referenceNumber: typing.Optional[typing.List[NumberType]] = jstruct.JList[NumberType]
    service: typing.Optional[ServiceType] = jstruct.JStruct[ServiceType]
    statusCode: typing.Optional[str] = None
    statusDescription: typing.Optional[str] = None
    suppressionIndicators: typing.Optional[typing.List[str]] = None
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]


@attr.s(auto_attribs=True)
class WarningType:
    code: typing.Optional[int] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentType:
    inquiryNumber: typing.Optional[str] = None
    package: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
    userRelation: typing.Optional[typing.List[str]] = None
    warnings: typing.Optional[typing.List[WarningType]] = jstruct.JList[WarningType]


@attr.s(auto_attribs=True)
class TrackResponseType:
    shipment: typing.Optional[typing.List[ShipmentType]] = jstruct.JList[ShipmentType]


@attr.s(auto_attribs=True)
class TrackingResponseType:
    trackResponse: typing.Optional[TrackResponseType] = jstruct.JStruct[TrackResponseType]
