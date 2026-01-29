import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TransactionReferenceType:
    CustomerContext: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ResponseStatusType:
    Code: typing.Optional[str] = None
    Description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AlertType:
    Code: typing.Optional[str] = None
    Description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ResponseType:
    ResponseStatus: typing.Optional[ResponseStatusType] = jstruct.JStruct[ResponseStatusType]
    Alert: typing.Optional[typing.List[AlertType]] = jstruct.JList[AlertType]
    TransactionReference: typing.Optional[TransactionReferenceType] = jstruct.JStruct[TransactionReferenceType]


@attr.s(auto_attribs=True)
class WeekendServiceTerritoryType:
    SatWST: typing.Optional[str] = None
    SunWST: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateStatusType:
    Code: typing.Optional[str] = None
    Description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DisclaimerType:
    Code: typing.Optional[str] = None
    Description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ChargeDetailType:
    ChargeCode: typing.Optional[str] = None
    ChargeDescription: typing.Optional[str] = None
    ChargeAmount: typing.Optional[str] = None
    IncentedAmount: typing.Optional[str] = None
    TaxAmount: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TaxChargesType:
    Type: typing.Optional[str] = None
    MonetaryValue: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateResultType:
    Disclaimer: typing.Optional[DisclaimerType] = jstruct.JStruct[DisclaimerType]
    RateType: typing.Optional[str] = None
    CurrencyCode: typing.Optional[str] = None
    ChargeDetail: typing.Optional[typing.List[ChargeDetailType]] = jstruct.JList[ChargeDetailType]
    TaxCharges: typing.Optional[typing.List[TaxChargesType]] = jstruct.JList[TaxChargesType]
    TotalTax: typing.Optional[str] = None
    GrandTotalOfAllCharge: typing.Optional[str] = None
    GrandTotalOfAllIncentedCharge: typing.Optional[str] = None
    PreTaxTotalCharge: typing.Optional[str] = None
    PreTaxTotalIncentedCharge: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupCreationResponseType:
    Response: typing.Optional[ResponseType] = jstruct.JStruct[ResponseType]
    PRN: typing.Optional[str] = None
    WeekendServiceTerritory: typing.Optional[WeekendServiceTerritoryType] = jstruct.JStruct[WeekendServiceTerritoryType]
    WeekendServiceTerritoryIndicator: typing.Optional[str] = None
    RateStatus: typing.Optional[RateStatusType] = jstruct.JStruct[RateStatusType]
    RateResult: typing.Optional[RateResultType] = jstruct.JStruct[RateResultType]


@attr.s(auto_attribs=True)
class PickupCreationResponseWrapperType:
    PickupCreationResponse: typing.Optional[PickupCreationResponseType] = jstruct.JStruct[PickupCreationResponseType]


# Cancel Response Types
@attr.s(auto_attribs=True)
class GWNStatusType:
    Code: typing.Optional[str] = None
    Description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupCancelResponseType:
    Response: typing.Optional[ResponseType] = jstruct.JStruct[ResponseType]
    PickupType: typing.Optional[str] = None
    GWNStatus: typing.Optional[GWNStatusType] = jstruct.JStruct[GWNStatusType]


@attr.s(auto_attribs=True)
class PickupCancelResponseWrapperType:
    PickupCancelResponse: typing.Optional[PickupCancelResponseType] = jstruct.JStruct[PickupCancelResponseType]
