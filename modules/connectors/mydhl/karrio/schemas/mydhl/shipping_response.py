import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DocumentType:
    imageFormat: typing.Optional[str] = None
    content: typing.Optional[str] = None
    typeCode: typing.Optional[str] = None
    packageReferenceNumber: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class EstimatedDeliveryDateType:
    estimatedDeliveryDate: typing.Optional[str] = None
    estimatedDeliveryType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageType:
    referenceNumber: typing.Optional[int] = None
    trackingNumber: typing.Optional[str] = None
    trackingUrl: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupDetailsType:
    localCutoffDateAndTime: typing.Optional[str] = None
    gmtCutoffTime: typing.Optional[str] = None
    cutoffTimeOffset: typing.Optional[str] = None
    pickupEarliest: typing.Optional[str] = None
    pickupLatest: typing.Optional[str] = None
    totalTransitDays: typing.Optional[int] = None
    pickupAdditionalDays: typing.Optional[int] = None
    deliveryAdditionalDays: typing.Optional[int] = None
    pickupDayOfWeek: typing.Optional[int] = None
    deliveryDayOfWeek: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ShipmentDetailType:
    pickupDetails: typing.Optional[PickupDetailsType] = jstruct.JStruct[PickupDetailsType]


@attr.s(auto_attribs=True)
class ShippingResponseType:
    shipmentTrackingNumber: typing.Optional[str] = None
    trackingUrl: typing.Optional[str] = None
    packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
    documents: typing.Optional[typing.List[DocumentType]] = jstruct.JList[DocumentType]
    shipmentDetails: typing.Optional[typing.List[ShipmentDetailType]] = jstruct.JList[ShipmentDetailType]
    estimatedDeliveryDate: typing.Optional[EstimatedDeliveryDateType] = jstruct.JStruct[EstimatedDeliveryDateType]
