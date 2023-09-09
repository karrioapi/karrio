from attr import s
from typing import Optional, Any
from jstruct import JStruct


@s(auto_attribs=True)
class CourierType:
    id: Optional[int] = None
    name: Optional[str] = None
    phone: Optional[str] = None


@s(auto_attribs=True)
class TrackingResponseType:
    reference: Optional[str] = None
    status: Optional[str] = None
    statusChangeDateTime: Optional[str] = None
    purchaseOrderNumber: Optional[str] = None
    trackinglink: Optional[str] = None
    proofOfDeliveryPhotoUrl: Any = None
    signatureUrl: Any = None
    courier: Optional[CourierType] = JStruct[CourierType]
