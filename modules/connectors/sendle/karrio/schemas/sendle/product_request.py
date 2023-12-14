from attr import s
from typing import Optional


@s(auto_attribs=True)
class ProductRequestType:
    senderaddressline1: Optional[str] = None
    senderaddressline2: Optional[str] = None
    sendersuburb: Optional[str] = None
    senderpostcode: Optional[str] = None
    sendercountry: Optional[str] = None
    receiveraddressline1: Optional[str] = None
    receiveraddressline2: Optional[str] = None
    receiversuburb: Optional[str] = None
    receiverpostcode: Optional[str] = None
    receivercountry: Optional[str] = None
    weightvalue: Optional[float] = None
    weightunits: Optional[str] = None
    volumevalue: Optional[str] = None
    volumeunits: Optional[str] = None
    lengthvalue: Optional[float] = None
    widthvalue: Optional[float] = None
    heightvalue: Optional[float] = None
    dimensionunits: Optional[str] = None
