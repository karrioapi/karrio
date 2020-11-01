import attr
from jstruct import JStruct, JList, REQUIRED
from typing import Optional, List


@attr.s(auto_attribs=True)
class Appointment:
    type: str
    date: Optional[str] = None
    time: Optional[str] = None
    phone: Optional[str] = None


@attr.s(auto_attribs=True)
class Address:
    postalCode: str
    provinceCode: str
    number: Optional[int] = None
    countryCode: Optional[str] = None
    name: Optional[str] = None


@attr.s(auto_attribs=True)
class Hazmat:
    number: int
    phone: str


@attr.s(auto_attribs=True)
class Parcel:
    quantity: int
    parcelType: str

    id: Optional[int] = None
    weight: Optional[int] = None
    length: Optional[int] = None
    depth: Optional[int] = None
    width: Optional[int] = None
    note: Optional[str] = None
    status: Optional[int] = None
    FCA_Class: Optional[str] = None
    hazmat: Optional[Hazmat] = JStruct[Hazmat]
    requestReturnLabel: Optional[bool] = None
    returnWaybill: Optional[str] = None


@attr.s(auto_attribs=True)
class PromoCode:
    code: Optional[str] = None


@attr.s(auto_attribs=True)
class Surcharge:
    type: str
    id: Optional[int] = None
    value: Optional[str] = None
    name: Optional[str] = None
    amount: Optional[int] = None


@attr.s(auto_attribs=True)
class RateRequest:
    category: str
    paymentType: str
    deliveryType: str
    unitOfMeasurement: str
    sender: Address = JStruct[Address, REQUIRED]
    consignee: Address = JStruct[Address, REQUIRED]
    parcels: List[Parcel] = JList[Parcel, REQUIRED]

    billing: Optional[int] = None
    promoCodes: Optional[List[PromoCode]] = JList[PromoCode]
    surcharges: Optional[List[Surcharge]] = JList[Surcharge]
    appointment: Optional[Appointment] = JStruct[Appointment]


@attr.s(auto_attribs=True)
class TaxesDetail:
    type: Optional[str] = None
    amount: Optional[str] = None
    name: Optional[str] = None


@attr.s(auto_attribs=True)
class Rate:
    grossAmount: Optional[int] = None
    discountAmount: Optional[int] = None
    otherCharge: Optional[int] = None
    fuelChargePercentage: Optional[int] = None
    accountType: Optional[str] = None
    rateType: Optional[str] = None
    cubicWeight: Optional[float] = None
    basicCharge: Optional[float] = None
    weightCharge: Optional[float] = None
    surcharges: List[Surcharge] = JList[Surcharge]
    subTotal: Optional[float] = None
    unitOfMeasurement: Optional[str] = None
    taxesDetails: List[TaxesDetail] = JList[TaxesDetail]
    taxes: Optional[float] = None
    fuelCharge: Optional[float] = None
    zoneCharge: Optional[float] = None
    total: Optional[float] = None


@attr.s(auto_attribs=True)
class Reference:
    code: Optional[int] = None
    type: Optional[str] = None


@attr.s(auto_attribs=True)
class RateResponse:
    delay: Optional[int] = None
    terminalLimit: Optional[int] = None
    singleShipmentCost: Optional[int] = None
    quantity: Optional[int] = None
    rates: List[Rate] = JList[Rate]
    references: List[Reference] = JList[Reference]
    unitOfMeasurement: Optional[str] = None
    parcelType: Optional[str] = None
    weight: Optional[str] = None
    postalCodeDelivery: Optional[str] = None
    postalCodePickup: Optional[str] = None
    creator: Optional[str] = None
    date: Optional[str] = None
    warning: Optional[str] = None
