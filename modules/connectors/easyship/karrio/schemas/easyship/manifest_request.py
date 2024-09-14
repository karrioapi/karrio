from attr import s
from typing import Optional, List


@s(auto_attribs=True)
class ManifestRequestType:
    courieraccountid: Optional[str] = None
    shipmentids: List[str] = []
