import attr
from jstruct import JStruct, JList
from typing import Optional, List


@attr.s(auto_attribs=True)
class Activity:
    parcelId: Optional[int] = None
    activityDate: Optional[str] = None
    createDate: Optional[str] = None
    status: Optional[str] = None
    statusDetail: Optional[str] = None
    code: Optional[str] = None
    codeDetail: Optional[str] = None
    group: Optional[str] = None
    additionalInformation: Optional[str] = None
    terminal: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    width: Optional[str] = None
    length: Optional[str] = None


@attr.s(auto_attribs=True)
class Tracking:
    id: Optional[int] = None
    billingAccount: Optional[int] = None
    status: Optional[int] = None
    custRefNum: Optional[str] = None
    activities: Optional[List[Activity]] = JList[Activity]
    activityImages: Optional[List[dict]] = JList[dict]
    isAuthorized: Optional[bool] = None
    trackingNumber: Optional[str] = None
    category: Optional[str] = None
    paymentType: Optional[str] = None
    note: Optional[str] = None
    direction: Optional[str] = None
    sender: Optional[dict] = None
    consignee: Optional[dict] = None
    unitOfMeasurement: Optional[str] = None
    parcels: Optional[List[dict]] = None
    surcharges: Optional[List[dict]] = None
    createDate: Optional[str] = None
    updateDate: Optional[str] = None
    deliveryType: Optional[str] = None
    references: Optional[List[dict]] = None
    returnAddress: Optional[dict] = None
    appointment: Optional[dict] = None
    promoCodes: Optional[List[dict]] = None
    internationalDetails: Optional[dict] = None
    pickupDate: Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingAPI:
    tracking: Optional[List[Tracking]] = JList[Tracking]
