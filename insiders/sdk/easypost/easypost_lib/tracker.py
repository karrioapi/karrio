from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Fee:
    object: Optional[str] = None
    type: Optional[str] = None
    amount: Optional[str] = None
    charged: Optional[bool] = None
    refunded: Optional[bool] = None


@s(auto_attribs=True)
class TrackingLocation:
    object: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: None
    zip: Optional[int] = None


@s(auto_attribs=True)
class TrackingDetail:
    object: Optional[str] = None
    message: Optional[str] = None
    status: Optional[str] = None
    trackingdetaildatetime: Optional[str] = None
    source: Optional[str] = None
    trackinglocation: Optional[TrackingLocation] = JStruct[TrackingLocation]


@s(auto_attribs=True)
class Tracker:
    id: Optional[str] = None
    object: Optional[str] = None
    mode: Optional[str] = None
    trackingcode: Optional[str] = None
    status: Optional[str] = None
    createdat: Optional[str] = None
    updatedat: Optional[str] = None
    signedby: None
    weight: None
    estdeliverydate: None
    shipmentid: None
    carrier: Optional[str] = None
    publicurl: Optional[str] = None
    trackingdetails: List[TrackingDetail] = JList[TrackingDetail]
    carrierdetail: None
    fees: List[Fee] = JList[Fee]
