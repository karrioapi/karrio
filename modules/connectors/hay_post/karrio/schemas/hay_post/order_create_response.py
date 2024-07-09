from attr import s
from typing import Optional, Any


@s(auto_attribs=True)
class OrderCreateResponseType:
    id: Optional[int] = None
    barcode: Optional[str] = None
    revertOrderId: Optional[int] = None
    revertBarcode: Optional[str] = None
    postalcode: Any = None
