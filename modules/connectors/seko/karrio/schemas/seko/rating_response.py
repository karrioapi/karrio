from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class AvailableType:
    QuoteId: Optional[str] = None
    CarrierId: Optional[int] = None
    CarrierName: Optional[str] = None
    DeliveryType: Optional[str] = None
    Cost: Optional[float] = None
    ServiceStandard: Optional[str] = None
    Comments: Optional[str] = None
    Route: Optional[str] = None
    IsRuralDelivery: Optional[bool] = None
    IsSaturdayDelivery: Optional[bool] = None
    IsFreightForward: Optional[bool] = None
    CarrierServiceType: Optional[str] = None


@s(auto_attribs=True)
class RejectedType:
    CarrierName: Optional[str] = None
    DeliveryType: Optional[str] = None
    Reason: Optional[str] = None


@s(auto_attribs=True)
class ValidationErrorsType:
    Property: Optional[str] = None
    Message: Optional[str] = None
    Key: Optional[str] = None
    Value: Optional[str] = None


@s(auto_attribs=True)
class RatingResponseType:
    Available: List[AvailableType] = JList[AvailableType]
    Rejected: List[RejectedType] = JList[RejectedType]
    ValidationErrors: Optional[ValidationErrorsType] = JStruct[ValidationErrorsType]
