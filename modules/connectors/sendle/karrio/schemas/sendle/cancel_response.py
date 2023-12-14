from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class MetadataType:
    pass


@s(auto_attribs=True)
class CancelResponseType:
    orderid: Optional[str] = None
    state: Optional[str] = None
    orderurl: Optional[str] = None
    sendlereference: Optional[str] = None
    trackingurl: Optional[str] = None
    customerreference: Optional[str] = None
    metadata: Optional[dict] = {}
    cancelledat: Optional[str] = None
    cancellationmessage: Optional[str] = None
