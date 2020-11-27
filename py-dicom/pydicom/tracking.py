import attr
from jstruct import JStruct, JList
from typing import Optional, List


@attr.s(auto_attribs=True)
class Activity:
    parcelId: Optional[int] = None
    activityDate: Optional[str] = None
    createDate: Optional[str] = None
    status: Optional[str] = None
    statusDetail: Optional[str] = None
    code: Optional[str] = None
    codeDetail: Optional[str] = None
    group: Optional[str] = None
    additionalInformation: Optional[str] = None
    terminal: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    width: Optional[str] = None
    length: Optional[str] = None


@attr.s(auto_attribs=True)
class ActivityImage:
    imageDate: Optional[str] = None
    url: Optional[str] = None
    clientName: Optional[str] = None
    imageType: Optional[str] = None


@attr.s(auto_attribs=True)
class Appointment:
    ID: Optional[str] = None
    type: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    phone: Optional[str] = None


@attr.s(auto_attribs=True)
class Contact:
    extension: Optional[int] = None
    language: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    telephone: Optional[str] = None
    fullName: Optional[str] = None


@attr.s(auto_attribs=True)
class Address:
    id: Optional[int] = None
    streetNumber: Optional[int] = None
    suite: Optional[int] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    streetType: Optional[str] = None
    streetName: Optional[str] = None
    streetDirection: Optional[str] = None
    city: Optional[str] = None
    provinceCode: Optional[str] = None
    postalCode: Optional[str] = None
    countryCode: Optional[str] = None
    customerName: Optional[str] = None
    customerNickName: Optional[str] = None
    contact: Optional[Contact] = JStruct[Contact]


@attr.s(auto_attribs=True)
class Broker:
    id: Optional[int] = None
    CSABusinessNumber: Optional[int] = None
    href: Optional[str] = None
    otherBroker: Optional[str] = None


@attr.s(auto_attribs=True)
class Product:
    id: Optional[int] = None
    Quantity: Optional[int] = None


@attr.s(auto_attribs=True)
class InternationalDetails:
    totalRetailValue: Optional[int] = None
    currency: Optional[str] = None
    exchangeRate: Optional[int] = None
    dutyBilling: Optional[str] = None
    descriptionOfGoods: Optional[str] = None
    importerOfRecord: Optional[Address] = JStruct[Address]
    broker: Optional[Broker] = None
    purpose: Optional[str] = None
    products: List[Product] = JList[Product]
    borderStatus: Optional[str] = None
    isDicomBroker: Optional[bool] = None


@attr.s(auto_attribs=True)
class Hazmat:
    number: Optional[int] = None
    phone: Optional[str] = None


@attr.s(auto_attribs=True)
class Parcel:
    id: Optional[int] = None
    parcelType: Optional[str] = None
    quantity: Optional[int] = None
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
    code: Optional[str] = None


@attr.s(auto_attribs=True)
class Reference:
    code: Optional[int] = None
    type: Optional[str] = None


@attr.s(auto_attribs=True)
class Surcharge:
    id: Optional[int] = None
    value: Optional[str] = None
    type: Optional[str] = None
    name: Optional[str] = None
    amount: Optional[int] = None


@attr.s(auto_attribs=True)
class TrackingResponse:
    id: Optional[int] = None
    billingAccount: Optional[int] = None
    status: Optional[int] = None
    custRefNum: Optional[str] = None
    activities: List[Activity] = JList[Activity]
    activityImages: List[ActivityImage] = JList[ActivityImage]
    isAuthorized: Optional[bool] = None
    trackingNumber: Optional[str] = None
    category: Optional[str] = None
    paymentType: Optional[str] = None
    note: Optional[str] = None
    direction: Optional[str] = None
    sender: Optional[Address] = JStruct[Address]
    consignee: Optional[Address] = JStruct[Address]
    unitOfMeasurement: Optional[str] = None
    parcels: List[Parcel] = JList[Parcel]
    surcharges: List[Surcharge] = JList[Surcharge]
    createDate: Optional[str] = None
    updateDate: Optional[str] = None
    deliveryType: Optional[str] = None
    references: List[Reference] = JList[Reference]
    returnAddress: Optional[Address] = JStruct[Address]
    appointment: Optional[Appointment] = JStruct[Appointment]
    promoCodes: List[PromoCode] = JList[PromoCode]
    internationalDetails: Optional[InternationalDetails] = JStruct[InternationalDetails]
    pickupDate: Optional[str] = None
