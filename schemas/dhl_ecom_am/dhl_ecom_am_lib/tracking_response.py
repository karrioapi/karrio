from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Links:
    previous: Optional[str] = None
    next: Optional[str] = None


@s(auto_attribs=True)
class Event:
    location: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    timeZone: Optional[str] = None
    postalCode: Optional[int] = None
    primaryEventId: Optional[int] = None
    primaryEventDescription: Optional[str] = None
    secondaryEventId: Optional[int] = None
    secondaryEventDescription: Optional[str] = None


@s(auto_attribs=True)
class Weight:
    value: Optional[float] = None
    unitOfMeasure: Optional[str] = None
    intelligentMailBarcodeFlag: Optional[bool] = None
    declaredValue: Optional[float] = None
    declaredValueCurrency: Optional[str] = None
    batchReference: Optional[str] = None
    deliveryConfirmationFlag: Optional[bool] = None
    customerReference: Optional[str] = None
    contentCategory: Optional[str] = None


@s(auto_attribs=True)
class PackagePackage:
    dhlPackageId: Optional[str] = None
    packageId: Optional[str] = None
    manifestId: Optional[str] = None
    trackingId: Optional[str] = None
    deliveryConfirmationNumber: Optional[str] = None
    overlabeledDspNumber: Optional[str] = None
    intelligentMailBarcode: Optional[str] = None
    overlabeledIntelligentMailBarcode: Optional[str] = None
    productClass: Optional[str] = None
    orderedProductId: Optional[str] = None
    billedProductId: Optional[str] = None
    productName: Optional[str] = None
    signatureConfirmationFlag: Optional[bool] = None
    intelligentMailBarcodeFlag: Optional[bool] = None
    deliveryConfirmationFlag: Optional[bool] = None
    customerReference: Optional[str] = None
    expectedDelivery: Optional[str] = None
    weight: Optional[Weight] = JStruct[Weight]


@s(auto_attribs=True)
class Recipient:
    name: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    address3: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postalCode: Optional[str] = None
    phone: Optional[str] = None
    signedForName: Optional[str] = None


@s(auto_attribs=True)
class PickupDetail:
    soldTo: Optional[int] = None
    pickup: Optional[int] = None
    pickupAddress: Optional[Recipient] = JStruct[Recipient]


@s(auto_attribs=True)
class PackageElement:
    recipient: Optional[Recipient] = JStruct[Recipient]
    events: List[Event] = JList[Event]
    pickupDetail: Optional[PickupDetail] = JStruct[PickupDetail]
    package: Optional[PackagePackage] = JStruct[PackagePackage]


@s(auto_attribs=True)
class TrackingResponse:
    total: Optional[int] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    timestamp: Optional[str] = None
    links: Optional[Links] = JStruct[Links]
    packages: List[PackageElement] = JList[PackageElement]
