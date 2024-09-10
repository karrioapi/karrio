from attr import s
from typing import Optional, Any, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AdditionalServiceType:
    id: Optional[int] = None
    name: Optional[str] = None
    fee: Optional[int] = None
    key: Optional[str] = None
    relationIndexId: Optional[int] = None
    isActive: Optional[bool] = None


@s(auto_attribs=True)
class LegalTypeType:
    id: Optional[int] = None
    name: Optional[str] = None


@s(auto_attribs=True)
class CustomerType:
    customerId: Optional[int] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    phone: Any = None
    legalType: Optional[LegalTypeType] = JStruct[LegalTypeType]
    documents: List[Any] = []
    companyName: Any = None


@s(auto_attribs=True)
class OrderType:
    id: Optional[int] = None
    customerId: Optional[int] = None
    trackingId: Optional[str] = None
    amount: Optional[int] = None
    weight: Optional[int] = None
    stateId: Optional[int] = None
    comment: Optional[str] = None
    service: Optional[LegalTypeType] = JStruct[LegalTypeType]
    category: Optional[LegalTypeType] = JStruct[LegalTypeType]
    transactionId: Any = None
    bundle: Any = None
    shipment: Any = None
    createDate: Optional[str] = None
    isVerified: Optional[bool] = None
    recaddress: Any = None
    locationId: Any = None
    codAmount: Any = None
    paymentMethodId: Optional[int] = None
    isInternational: Optional[bool] = None
    partner: Any = None


@s(auto_attribs=True)
class ReceiverInfoType:
    companyName: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    phoneNumber: Optional[str] = None
    email: Optional[str] = None
    nickname: Any = None


@s(auto_attribs=True)
class NAddressType:
    country: Optional[LegalTypeType] = JStruct[LegalTypeType]
    provinceState: Optional[LegalTypeType] = JStruct[LegalTypeType]
    cityVillage: Optional[LegalTypeType] = JStruct[LegalTypeType]
    street: Optional[LegalTypeType] = JStruct[LegalTypeType]
    building: Optional[LegalTypeType] = JStruct[LegalTypeType]
    apartment: Optional[LegalTypeType] = JStruct[LegalTypeType]
    postalCode: Optional[str] = None
    address: Any = None
    isHomeDelivery: Optional[bool] = None
    isDeliveryPaid: Optional[bool] = None
    deliveryDate: Optional[str] = None
    receiverInfo: Optional[ReceiverInfoType] = JStruct[ReceiverInfoType]
    factreceiverInfo: Any = None


@s(auto_attribs=True)
class OrderStateHistoryType:
    id: Optional[int] = None
    orderId: Optional[int] = None
    stateId: Optional[int] = None
    createDate: Optional[str] = None
    userId: Optional[int] = None
    isActive: Optional[bool] = None


@s(auto_attribs=True)
class OrderTrackingResponseType:
    order: Optional[OrderType] = JStruct[OrderType]
    info: Any = None
    orderDestinationAddress: Optional[NAddressType] = JStruct[NAddressType]
    returnAddress: Optional[NAddressType] = JStruct[NAddressType]
    customer: Optional[CustomerType] = JStruct[CustomerType]
    orderStateHistories: List[OrderStateHistoryType] = JList[OrderStateHistoryType]
    additionalServices: List[AdditionalServiceType] = JList[AdditionalServiceType]
    rejectedOrders: List[Any] = []
