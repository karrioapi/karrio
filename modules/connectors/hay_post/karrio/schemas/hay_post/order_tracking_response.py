import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AdditionalServiceType:
    id: typing.Optional[int] = None
    name: typing.Optional[str] = None
    fee: typing.Optional[int] = None
    key: typing.Optional[str] = None
    relationIndexId: typing.Optional[int] = None
    isActive: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class LegalTypeObjectType:
    id: typing.Optional[int] = None
    name: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomerType:
    customerId: typing.Optional[int] = None
    firstName: typing.Optional[str] = None
    lastName: typing.Optional[str] = None
    phone: typing.Any = None
    legalType: typing.Optional[LegalTypeObjectType] = jstruct.JStruct[LegalTypeObjectType]
    documents: typing.Optional[typing.List[typing.Any]] = None
    companyName: typing.Any = None


@attr.s(auto_attribs=True)
class OrderType:
    id: typing.Optional[int] = None
    customerId: typing.Optional[int] = None
    trackingId: typing.Optional[str] = None
    amount: typing.Optional[int] = None
    weight: typing.Optional[int] = None
    stateId: typing.Optional[int] = None
    comment: typing.Optional[str] = None
    service: typing.Optional[LegalTypeObjectType] = jstruct.JStruct[LegalTypeObjectType]
    category: typing.Optional[LegalTypeObjectType] = jstruct.JStruct[LegalTypeObjectType]
    transactionId: typing.Any = None
    bundle: typing.Any = None
    shipment: typing.Any = None
    createDate: typing.Optional[str] = None
    isVerified: typing.Optional[bool] = None
    recaddress: typing.Any = None
    locationId: typing.Any = None
    codAmount: typing.Any = None
    paymentMethodId: typing.Optional[int] = None
    isInternational: typing.Optional[bool] = None
    partner: typing.Any = None


@attr.s(auto_attribs=True)
class ReceiverInfoType:
    companyName: typing.Optional[str] = None
    firstName: typing.Optional[str] = None
    lastName: typing.Optional[str] = None
    phoneNumber: typing.Optional[str] = None
    email: typing.Optional[str] = None
    nickname: typing.Any = None


@attr.s(auto_attribs=True)
class NAddressType:
    country: typing.Optional[LegalTypeObjectType] = jstruct.JStruct[LegalTypeObjectType]
    provinceState: typing.Optional[LegalTypeObjectType] = jstruct.JStruct[LegalTypeObjectType]
    cityVillage: typing.Optional[LegalTypeObjectType] = jstruct.JStruct[LegalTypeObjectType]
    street: typing.Optional[LegalTypeObjectType] = jstruct.JStruct[LegalTypeObjectType]
    building: typing.Optional[LegalTypeObjectType] = jstruct.JStruct[LegalTypeObjectType]
    apartment: typing.Optional[LegalTypeObjectType] = jstruct.JStruct[LegalTypeObjectType]
    postalCode: typing.Optional[str] = None
    address: typing.Any = None
    isHomeDelivery: typing.Optional[bool] = None
    isDeliveryPaid: typing.Optional[bool] = None
    deliveryDate: typing.Optional[str] = None
    receiverInfo: typing.Optional[ReceiverInfoType] = jstruct.JStruct[ReceiverInfoType]
    factreceiverInfo: typing.Any = None


@attr.s(auto_attribs=True)
class OrderStateHistoryType:
    id: typing.Optional[int] = None
    orderId: typing.Optional[int] = None
    stateId: typing.Optional[int] = None
    createDate: typing.Optional[str] = None
    userId: typing.Optional[int] = None
    isActive: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class OrderTrackingResponseType:
    order: typing.Optional[OrderType] = jstruct.JStruct[OrderType]
    info: typing.Any = None
    orderDestinationAddress: typing.Optional[NAddressType] = jstruct.JStruct[NAddressType]
    returnAddress: typing.Optional[NAddressType] = jstruct.JStruct[NAddressType]
    customer: typing.Optional[CustomerType] = jstruct.JStruct[CustomerType]
    orderStateHistories: typing.Optional[typing.List[OrderStateHistoryType]] = jstruct.JList[OrderStateHistoryType]
    additionalServices: typing.Optional[typing.List[AdditionalServiceType]] = jstruct.JList[AdditionalServiceType]
    rejectedOrders: typing.Optional[typing.List[typing.Any]] = None
