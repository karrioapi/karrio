from attr import s
from typing import Optional, List


@s(auto_attribs=True)
class TrackingRequestType:
    includePublished: Optional[bool] = None
    pageable: Optional[str] = None
    trackingNumbers: List[str] = []
