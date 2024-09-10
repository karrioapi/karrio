from attr import s
from typing import Optional, List
from jstruct import JStruct


@s(auto_attribs=True)
class ReceiverInfoType:
    companyName: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    phoneNumber: Optional[str] = None
    email: Optional[str] = None


@s(auto_attribs=True)
class NAddressType:
    countryId: Optional[int] = None
    provinceStateId: Optional[int] = None
    cityVillage: Optional[str] = None
    street: Optional[str] = None
    building: Optional[int] = None
    apartment: Optional[int] = None
    postalCode: Optional[str] = None
    receiverInfo: Optional[ReceiverInfoType] = JStruct[ReceiverInfoType]


@s(auto_attribs=True)
class OrderCreateRequestType:
    customerId: Optional[int] = None
    serviceCategoryDirectionId: Optional[int] = None
    weight: Optional[int] = None
    comment: Optional[str] = None
    returnRegisteredAddress: Optional[bool] = None
    destinationAddress: Optional[NAddressType] = JStruct[NAddressType]
    returnAddress: Optional[NAddressType] = JStruct[NAddressType]
    additionalServices: List[int] = []
