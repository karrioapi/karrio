from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class TrackingNumberInfoType:
    trackingNumber: Optional[str] = None
    carrierCode: Optional[str] = None
    trackingNumberUniqueId: Optional[str] = None


@s(auto_attribs=True)
class TrackingInfoType:
    shipDateBegin: Optional[str] = None
    shipDateEnd: Optional[str] = None
    trackingNumberInfo: Optional[TrackingNumberInfoType] = JStruct[TrackingNumberInfoType]


@s(auto_attribs=True)
class TrackingRequestType:
    includeDetailedScans: Optional[bool] = None
    trackingInfo: List[TrackingInfoType] = JList[TrackingInfoType]
