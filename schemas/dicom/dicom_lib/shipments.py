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
class Contact:
    fullName: str
    extension: Optional[int] = None
    language: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    telephone: Optional[str] = None


@attr.s(auto_attribs=True)
class Address:
    city: str
    provinceCode: str
    postalCode: str
    countryCode: str
    customerName: str
    streetNumber: Optional[int] = None
    suite: Optional[int] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    streetType: Optional[str] = None
    streetName: Optional[str] = None
    streetDirection: Optional[str] = None
    customerNickName: Optional[str] = None
    contact: Contact = JStruct[Contact]


@attr.s(auto_attribs=True)
class Broker:
    id: int
    CSA_BusinessNumber: Optional[int] = None
    href: Optional[str] = None
    otherBroker: Optional[str] = None


@attr.s(auto_attribs=True)
class Product:
    id: int
    Quantity: int


@attr.s(auto_attribs=True)
class InternationalDetails:
    isDicomBroker: bool
    descriptionOfGoods: str
    totalRetailValue: Optional[int] = None
    currency: Optional[str] = None
    exchangeRate: Optional[int] = None
    dutyBilling: Optional[str] = None
    importerOfRecord: Optional[Address] = JStruct[Address]
    broker: Optional[Broker] = JStruct[Broker]
    purpose: Optional[str] = None
    products: Optional[List[Product]] = JList[Product]
    borderStatus: Optional[str] = None


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
    FCAClass: Optional[str] = None
    hazmat: Optional[Hazmat] = JStruct[Hazmat]
    requestReturnLabel: Optional[bool] = None
    returnWaybill: Optional[str] = None


@attr.s(auto_attribs=True)
class PromoCode:
    code: str


@attr.s(auto_attribs=True)
class Reference:
    code: int
    type: str


@attr.s(auto_attribs=True)
class Surcharge:
    type: str
    id: Optional[int] = None
    value: Optional[str] = None
    name: Optional[str] = None
    amount: Optional[int] = None


@attr.s(auto_attribs=True)
class ShipmentRequest:
    paymentType: str
    billingAccount: int
    sender: Address = JStruct[Address, REQUIRED]
    consignee: Address = JStruct[Address, REQUIRED]
    parcels: List[Parcel] = JList[Parcel, REQUIRED]

    note: Optional[str] = None
    category: Optional[str] = None
    pickupDate: Optional[str] = None
    deliveryType: Optional[str] = None
    trackingNumber: Optional[str] = None
    unitOfMeasurement: Optional[str] = None
    surcharges: Optional[List[Surcharge]] = JList[Surcharge]
    promoCodes: Optional[List[PromoCode]] = JList[PromoCode]
    references: Optional[List[Reference]] = JList[Reference]
    returnAddress: Optional[Address] = JStruct[Address]
    appointment: Optional[Appointment] = JStruct[Appointment]
    internationalDetails: Optional[InternationalDetails] = JStruct[InternationalDetails]


@attr.s(auto_attribs=True)
class ShipmentResponse:
    parcelTrackingNumbers: List[str] = JList[str]
    ID: Optional[str] = None
    trackingNumber: Optional[str] = None
