from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class Weight:
    value: Optional[int] = None
    unitOfMeasure: Optional[str] = None


@s(auto_attribs=True)
class PackageDetail:
    orderNumber: Optional[int] = None
    authorizationNumber: Optional[int] = None
    returnReason: Optional[str] = None
    weight: Optional[Weight] = JStruct[Weight]


@s(auto_attribs=True)
class Address:
    name: Optional[str] = None
    companyName: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    address3: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postalCode: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None


@s(auto_attribs=True)
class CreateReturnRequest:
    pickup: Optional[str] = None
    orderedProductId: Optional[str] = None
    merchantId: Optional[str] = None
    shipperAddress: Optional[Address] = JStruct[Address]
    returnAddress: Optional[Address] = JStruct[Address]
    packageDetail: Optional[PackageDetail] = JStruct[PackageDetail]
