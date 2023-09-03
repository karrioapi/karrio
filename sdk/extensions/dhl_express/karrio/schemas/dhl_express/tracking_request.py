from attr import s
from typing import List, Optional


@s(auto_attribs=True)
class TrackingRequestType:
    shipmentTrackingNumber: List[int] = []
    pieceTrackingNumber: List[int] = []
    shipmentReference: Optional[int] = None
    shipmentReferenceType: Optional[str] = None
    shipperAccountNumber: Optional[int] = None
    dateRangeFrom: Optional[str] = None
    dateRangeTo: Optional[str] = None
    trackingView: Optional[str] = None
    levelOfDetail: Optional[str] = None
