from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class DocumentType:
    imageFormat: Optional[str] = None
    content: Optional[str] = None
    typeCode: Optional[str] = None
    packageReferenceNumber: Optional[int] = None


@s(auto_attribs=True)
class EstimatedDeliveryDateType:
    estimatedDeliveryDate: Optional[str] = None
    estimatedDeliveryType: Optional[str] = None


@s(auto_attribs=True)
class PackageType:
    referenceNumber: Optional[int] = None
    trackingNumber: Optional[str] = None
    trackingUrl: Optional[str] = None


@s(auto_attribs=True)
class PickupDetailsType:
    localCutoffDateAndTime: Optional[str] = None
    gmtCutoffTime: Optional[str] = None
    cutoffTimeOffset: Optional[str] = None
    pickupEarliest: Optional[str] = None
    pickupLatest: Optional[str] = None
    totalTransitDays: Optional[int] = None
    pickupAdditionalDays: Optional[int] = None
    deliveryAdditionalDays: Optional[int] = None
    pickupDayOfWeek: Optional[int] = None
    deliveryDayOfWeek: Optional[int] = None


@s(auto_attribs=True)
class ShipmentDetailType:
    pickupDetails: Optional[PickupDetailsType] = JStruct[PickupDetailsType]


@s(auto_attribs=True)
class ShippingResponseType:
    shipmentTrackingNumber: Optional[str] = None
    trackingUrl: Optional[str] = None
    packages: List[PackageType] = JList[PackageType]
    documents: List[DocumentType] = JList[DocumentType]
    shipmentDetails: List[ShipmentDetailType] = JList[ShipmentDetailType]
    estimatedDeliveryDate: Optional[EstimatedDeliveryDateType] = JStruct[EstimatedDeliveryDateType]
