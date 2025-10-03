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
    EstimatedDeliveryDays: typing.Optional[int] = None
    TransitTime: typing.Optional[str] = None
    ServiceLevel: typing.Optional[str] = None
    CarrierType: typing.Optional[int] = None
    IsOvernight: typing.Optional[bool] = None
    HasTrackPaks: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class RejectedType:
    CarrierName: typing.Optional[str] = None
    DeliveryType: typing.Optional[str] = None
    Reason: typing.Optional[str] = None
    CarrierId: typing.Optional[int] = None
    QuoteId: typing.Optional[str] = None
    ErrorCode: typing.Optional[str] = None
    ErrorDetails: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class SummaryType:
    TotalAvailable: typing.Optional[int] = None
    TotalRejected: typing.Optional[int] = None
    TotalValidationErrors: typing.Optional[int] = None
    Currency: typing.Optional[str] = None
    RequestId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ValidationErrorType:
    Property: typing.Optional[str] = None
    Message: typing.Optional[str] = None
    Key: typing.Optional[str] = None
    Value: typing.Optional[str] = None
    ErrorCode: typing.Optional[str] = None
    Severity: typing.Optional[str] = None
    WarningCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RatingResponseType:
    Available: typing.Optional[typing.List[AvailableType]] = jstruct.JList[AvailableType]
    Rejected: typing.Optional[typing.List[RejectedType]] = jstruct.JList[RejectedType]
    ValidationErrors: typing.Optional[typing.List[ValidationErrorType]] = jstruct.JList[ValidationErrorType]
    Summary: typing.Optional[SummaryType] = jstruct.JStruct[SummaryType]
    Warnings: typing.Optional[typing.List[ValidationErrorType]] = jstruct.JList[ValidationErrorType]
