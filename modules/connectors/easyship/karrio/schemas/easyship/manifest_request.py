from attr import s
from typing import Optional, List


@s(auto_attribs=True)
class ManifestRequestType:
    courier_account_id: Optional[str] = None
    shipment_ids: List[str] = []
