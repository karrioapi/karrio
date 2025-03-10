import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AvailableType:
    QuoteId: typing.Optional[str] = None
    CarrierId: typing.Optional[int] = None
    CarrierName: typing.Optional[str] = None
    DeliveryType: typing.Optional[str] = None
    Cost: typing.Optional[float] = None
    ServiceStandard: typing.Optional[str] = None
    Comments: typing.Optional[str] = None
    Route: typing.Optional[str] = None
    IsRuralDelivery: typing.Optional[bool] = None
    IsSaturdayDelivery: typing.Optional[bool] = None
    IsFreightForward: typing.Optional[bool] = None
    CarrierServiceType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RejectedType:
    CarrierName: typing.Optional[str] = None
    DeliveryType: typing.Optional[str] = None
    Reason: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ValidationErrorsType:
    Property: typing.Optional[str] = None
    Message: typing.Optional[str] = None
    Key: typing.Optional[str] = None
    Value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RatingResponseType:
    Available: typing.Optional[typing.List[AvailableType]] = jstruct.JList[AvailableType]
    Rejected: typing.Optional[typing.List[RejectedType]] = jstruct.JList[RejectedType]
    ValidationErrors: typing.Optional[ValidationErrorsType] = jstruct.JStruct[ValidationErrorsType]
