"""XPO logistics LTL rate quote response Datatype definition module."""

import attr
from typing import List, Union, Optional
from jstruct import JList, JStruct


@attr.s(auto_attribs=True)
class rateQuote:
    confirmationNbr
    shipmentInfo
    accessorialTariffName
    actlDiscountPct
    amcAmt
    aMCInd
    commodity
    deficitRatingInfo
    dscntSrcCd
    fscTariffName
    inboundZoneCd
    lnhChargeAmt
    nhChargeAmt
    offShrSIC
    offShrTariff
    offShrZoneCd
    ratingTariffName
    serviced
    bill2Party
    shipperToConsigneeMiles
    consignee
    shipperToConsigneeMiles
    totAccessorialAmt
    totCharge
    exchangeRate
    totDiscountAmt
    totFSCAmt
    totOffShrAccChargeAmt
    totOffShrAmt
    totOffShrFscCharge
    totOffShrLnhChargeAmt
    totTaxAmt
    trailerCnt
    vspApplied


@attr.s(auto_attribs=True)
class transitTime:
    destStateCd: Optional[str] = None
    destPostalCd: Optional[str] = None
    destSicCd: Optional[str] = None
    estDlvrDate: Optional[str] = None
    garntInd: Optional[bool] = None
    latestPkupDate: Optional[str] = None
    origPostalCd: Optional[str] = None
    origStateCd: Optional[str] = None
    origSicCd: Optional[str] = None
    requestedDlvrDate: Optional[str] = None
    requestedPkupDate: Optional[str] = None
    transitDays: Optional[int] = None
    earliestPkupDate: Optional[str] = None
    note: Optional[str] = None
    isPkupDateHoliday: Optional[bool] = None
    isrqstdDeliveryDateHoliday: Optional[bool] = None


@attr.s(auto_attribs=True)
class msgs:
    errorCd: Optional[str] = None
    message: Optional[str] = None
    fieldName: Optional[str] = None
    fieldValue: Optional[str] = None


@attr.s(auto_attribs=True)
class RateResponse:
    rateQuote: rateQuote = JStruct[rateQuote]
    transitTime: transitTime = JStruct[transitTime]
    msgs= msgs = JStruct[msgs]
