from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class CancelResponseType:
    order_id: Optional[str] = None
    state: Optional[str] = None
    order_url: Optional[str] = None
    sendle_reference: Optional[str] = None
    tracking_url: Optional[str] = None
    customer_reference: Optional[str] = None
    metadata: Optional[dict] = {}
    cancelled_at: Optional[str] = None
    cancellation_message: Optional[str] = None
