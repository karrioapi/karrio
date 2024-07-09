from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ReceiverInfoType:
    companyName: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    phoneNumber: Optional[str] = None
    email: Optional[str] = None
    nickname: Optional[str] = None


@s(auto_attribs=True)
class NAddressType:
    countryId: Optional[int] = None
    provinceStateId: Optional[int] = None
    provinceState: Optional[str] = None
    cityVillageId: Optional[int] = None
    cityVillage: Optional[str] = None
    streetId: Optional[int] = None
    street: Optional[str] = None
    buildingId: Optional[int] = None
    building: Optional[str] = None
    apartment: Optional[str] = None
    apartmentId: Optional[int] = None
    address: Optional[str] = None
    postalCode: Optional[str] = None
    deliveryDate: Optional[str] = None
    receiverInfo: Optional[ReceiverInfoType] = JStruct[ReceiverInfoType]


@s(auto_attribs=True)
class CodType:
    amount: Optional[int] = None
    bank: Optional[str] = None
    accountNumber: Optional[str] = None


@s(auto_attribs=True)
class EnclosureEnclosureType:
    description: Optional[str] = None
    hsCode: Optional[str] = None
    quantity: Optional[int] = None
    weight: Optional[int] = None
    amount: Optional[int] = None
    countryOfOrigin: Optional[str] = None


@s(auto_attribs=True)
class OrderInfoEnclosureType:
    enclosures: List[EnclosureEnclosureType] = JList[EnclosureEnclosureType]
    enclosureTypeId: Optional[int] = None


@s(auto_attribs=True)
class OrderInfoType:
    valuedAmount: Optional[int] = None
    valuedAmountCurrency: Optional[int] = None
    enclosure: List[OrderInfoEnclosureType] = JList[OrderInfoEnclosureType]
    cod: Optional[CodType] = JStruct[CodType]


@s(auto_attribs=True)
class TariffRequestElementType:
    customerId: Optional[int] = None
    serviceCategoryDirectionId: Optional[int] = None
    weight: Optional[int] = None
    totalPrice: Optional[int] = None
    currencyId: Optional[int] = None
    comment: Optional[str] = None
    returnRegisteredAddress: Optional[bool] = None
    partner: Optional[int] = None
    externalId: Optional[str] = None
    destinationAddress: Optional[NAddressType] = JStruct[NAddressType]
    returnAddress: Optional[NAddressType] = JStruct[NAddressType]
    orderInfo: Optional[OrderInfoType] = JStruct[OrderInfoType]
    additionalServices: List[int] = []
