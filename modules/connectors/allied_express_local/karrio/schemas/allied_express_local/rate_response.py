from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AccountType:
    accountCode: Optional[str] = None
    accountHash: Optional[str] = None
    accountKey: Optional[int] = None
    accountLedger: Optional[str] = None
    accountName: Optional[str] = None
    accountState: Optional[str] = None
    defaultAddress: Optional[str] = None
    defaultContact: Optional[str] = None
    defaultPhoneNo: Optional[str] = None
    defaultPostCode: Optional[int] = None
    defaultState: Optional[str] = None
    defaultSuburbName: Optional[str] = None
    discountLevel: Optional[int] = None
    priceSuppressed: Optional[bool] = None
    shippingDivision: Optional[str] = None


@s(auto_attribs=True)
class ItemType:
    dangerous: Optional[bool] = None
    height: Optional[str] = None
    itemCount: Optional[int] = None
    length: Optional[str] = None
    volume: Optional[str] = None
    weight: Optional[str] = None
    width: Optional[str] = None


@s(auto_attribs=True)
class GeographicAddressType:
    address1: Optional[str] = None
    address2: Optional[str] = None
    country: Optional[str] = None
    postCode: Optional[int] = None
    sortCode: Optional[str] = None
    state: Optional[str] = None
    suburb: Optional[str] = None


@s(auto_attribs=True)
class JobStopType:
    companyName: Optional[str] = None
    contact: Optional[str] = None
    emailAddress: Optional[str] = None
    geographicAddress: Optional[GeographicAddressType] = JStruct[GeographicAddressType]
    stopNumber: Optional[int] = None
    stopType: Optional[str] = None
    phoneNumber: Optional[str] = None


@s(auto_attribs=True)
class PriceType:
    chargeQuantity: Optional[int] = None
    cubicFactor: Optional[int] = None
    discountRate: Optional[str] = None
    grossPrice: Optional[str] = None
    netPrice: Optional[str] = None
    reason: Optional[str] = None


@s(auto_attribs=True)
class VehicleType:
    vehicleID: Optional[int] = None


@s(auto_attribs=True)
class ResultType:
    account: Optional[AccountType] = JStruct[AccountType]
    bookedBy: Optional[str] = None
    cubicWeight: Optional[str] = None
    docketNumber: Optional[str] = None
    instructions: Optional[str] = None
    itemCount: Optional[int] = None
    items: List[ItemType] = JList[ItemType]
    jobNumber: Optional[int] = None
    jobStops: List[JobStopType] = JList[JobStopType]
    price: Optional[PriceType] = JStruct[PriceType]
    readyDate: Optional[str] = None
    referenceNumbers: List[str] = []
    scheduledDeliveryDate: Optional[str] = None
    serviceLevel: Optional[str] = None
    validatedHash: Optional[str] = None
    vehicle: Optional[VehicleType] = JStruct[VehicleType]
    volume: Optional[str] = None
    weight: Optional[str] = None


@s(auto_attribs=True)
class Ns1QuoteLocalCourierJobResponseType:
    xmlnsns1: Optional[str] = None
    result: Optional[ResultType] = JStruct[ResultType]


@s(auto_attribs=True)
class SoapenvBodyType:
    ns1quoteLocalCourierJobResponse: Optional[Ns1QuoteLocalCourierJobResponseType] = JStruct[Ns1QuoteLocalCourierJobResponseType]


@s(auto_attribs=True)
class SoapenvEnvelopeType:
    xmlnssoapenv: Optional[str] = None
    xmlnsxsd: Optional[str] = None
    xmlnsxsi: Optional[str] = None
    soapenvBody: Optional[SoapenvBodyType] = JStruct[SoapenvBodyType]


@s(auto_attribs=True)
class RateResponseType:
    soapenvEnvelope: Optional[SoapenvEnvelopeType] = JStruct[SoapenvEnvelopeType]
