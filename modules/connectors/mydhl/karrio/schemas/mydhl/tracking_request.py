from attr import s
from typing import List, Optional


@s(auto_attribs=True)
class TrackingRequestType:
    shipmentTrackingNumber: List[str] = []
    pieceTrackingNumber: List[str] = []
    shipmentReference: Optional[str] = None
    shipmentReferenceType: Optional[str] = None
    shipperAccountNumber: Optional[str] = None
    dateRangeFrom: Optional[str] = None
    dateRangeTo: Optional[str] = None
    trackingView: Optional[str] = None
    levelOfDetail: Optional[str] = None
    requestControlledAccessDataCodes: Optional[bool] = None
