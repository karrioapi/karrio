from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class CarrierType:
    carrierName: Optional[str] = None
    serviceName: Optional[str] = None
    carrierLogoPath: Optional[str] = None


@s(auto_attribs=True)
class FromType:
    attention: Optional[str] = None
    company: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None
    zip: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    instructions: Optional[str] = None
    residential: Optional[bool] = None
    tailgateRequired: Optional[bool] = None
    confirmDelivery: Optional[bool] = None
    notifyRecipient: Optional[bool] = None


@s(auto_attribs=True)
class PackageType:
    height: Optional[int] = None
    length: Optional[int] = None
    width: Optional[int] = None
    dimensionUnit: Optional[str] = None
    weight: Optional[int] = None
    weightUnit: Optional[str] = None
    type: Optional[str] = None
    freightClass: Optional[str] = None
    nmfcCode: Optional[str] = None
    insuranceAmount: Optional[int] = None
    codAmount: Optional[int] = None
    description: Optional[str] = None
    harmonizedCode: Optional[str] = None
    skuCode: Optional[str] = None


@s(auto_attribs=True)
class PackagesType:
    type: Optional[str] = None
    quantity: Optional[int] = None
    weightUnit: Optional[str] = None
    packages: List[PackageType] = JList[PackageType]
    totalWeight: Optional[int] = None


@s(auto_attribs=True)
class OrderDetailsType:
    carrier: Optional[CarrierType] = JStruct[CarrierType]
    orderDetailsfrom: Optional[FromType] = JStruct[FromType]
    to: Optional[FromType] = JStruct[FromType]
    packages: Optional[PackagesType] = JStruct[PackagesType]


@s(auto_attribs=True)
class StatusType:
    labelGenerated: Optional[bool] = None
    reachedAtWarehouse: Optional[bool] = None
    inTransit: Optional[bool] = None
    delivered: Optional[bool] = None
    exception: Optional[bool] = None


@s(auto_attribs=True)
class TrackingDetailType:
    carrier: Optional[str] = None
    carrierEventCode: Optional[str] = None
    dateTime: Optional[str] = None
    location: Optional[str] = None
    postalCode: Optional[str] = None
    proofOfDelivery: Optional[str] = None
    signatoryName: Optional[str] = None
    description: Optional[str] = None
    additionalInfo: Optional[str] = None
    awbNumber: Optional[str] = None
    vehicleId: Optional[str] = None
    vehicleType: Optional[str] = None
    eshipperOrderStatus: Optional[str] = None


@s(auto_attribs=True)
class TrackingResponseType:
    trackingUrl: Optional[str] = None
    brandedTrackingUrl: Optional[str] = None
    lmcCarrierTrackingUrl: Optional[str] = None
    carbonNeutral: Optional[bool] = None
    remarks: Optional[str] = None
    trackingDetails: List[TrackingDetailType] = JList[TrackingDetailType]
    status: Optional[StatusType] = JStruct[StatusType]
    orderDetails: Optional[OrderDetailsType] = JStruct[OrderDetailsType]
