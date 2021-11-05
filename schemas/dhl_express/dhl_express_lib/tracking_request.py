from attr import s
from typing import List, Optional
from jstruct import JList


@s(auto_attribs=True)
class TrackingRequest:
    shipmentTrackingNumber: List[int] = JList[int]
    pieceTrackingNumber: List[int] = JList[int]
    shipmentReference: Optional[int] = None
    shipmentReferenceType: Optional[str] = None
    shipperAccountNumber: Optional[int] = None
    dateRangeFrom: Optional[str] = None
    dateRangeTo: Optional[str] = None
    trackingView: Optional[str] = None
    levelOfDetail: Optional[str] = None
